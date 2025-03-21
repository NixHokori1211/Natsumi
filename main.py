"""
Entry point for the Discord bot.
Handles bot initialization and startup.
Includes a web server for uptime monitoring with HTTPS support.
"""
import os
import logging
import threading
import ssl
from http.server import HTTPServer, BaseHTTPRequestHandler
from dotenv import load_dotenv
from bot import DiscordBot

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("discord_bot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# HTTPS server for uptime monitoring
class UptimeServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Server', 'Discord Bot HTTPS Server')
        self.end_headers()
        
        # Create simple HTML response with bot status
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Discord Bot Status</title>
            <style>
                body {{ font-family: Arial, sans-serif; text-align: center; margin-top: 50px; }}
                .status {{ color: green; font-weight: bold; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Discord Bot Status</h1>
                <p class="status">✅ Bot is online!</p>
                <p>Server Time: {logging.Formatter().converter().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p>This page is served over HTTPS for secure monitoring.</p>
            </div>
        </body>
        </html>
        """
        self.wfile.write(html.encode('utf-8'))
    
    def log_message(self, format, *args):
        # Suppress default logging to avoid spam
        return

def run_server():
    """Run a HTTPS server for uptime monitoring"""
    # Replit exposes port 5000 by default for web services
    port = int(os.environ.get('PORT', 5000))
    server_address = ('0.0.0.0', port)  # Use 0.0.0.0 to accept connections from any IP
    httpd = HTTPServer(server_address, UptimeServer)
    
    # Check if certificate files exist, if not generate them
    cert_file = 'cert.pem'
    key_file = 'key.pem'
    if not (os.path.exists(cert_file) and os.path.exists(key_file)):
        logger.info("Certificate files not found, generating...")
        try:
            import generate_cert
            generate_cert.generate_self_signed_cert()
        except Exception as e:
            logger.error(f"Failed to generate certificates: {e}")
            logger.info("Falling back to HTTP")
            logger.info(f"Starting HTTP uptime server on port {port}")
            httpd.serve_forever()
            return
    
    # Wrap the socket with SSL/TLS
    try:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(certfile=cert_file, keyfile=key_file)
        httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
        logger.info(f"Starting HTTPS uptime server on port {port}")
    except Exception as e:
        logger.error(f"Failed to configure HTTPS: {e}")
        logger.info("Falling back to HTTP")
        logger.info(f"Starting HTTP uptime server on port {port}")
    
    httpd.serve_forever()

if __name__ == "__main__":
    if not TOKEN:
        logger.error("No Discord token found. Please set the DISCORD_TOKEN environment variable.")
        exit(1)
    
    try:
        # Start the HTTPS server in a separate thread
        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()
        logger.info("HTTPS uptime monitoring server started in background")
        
        # Initialize and run the bot
        bot = DiscordBot("!")  # "!" is the command prefix
        logger.info("Starting Discord bot...")
        bot.run(TOKEN)
    except Exception as e:
        logger.error(f"Failed to start the bot: {e}")
        exit(1)

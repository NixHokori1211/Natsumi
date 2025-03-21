#!/usr/bin/env python
"""
Development script to run the Discord bot with additional logging and debugging options.
"""
import os
import logging
import sys
from dotenv import load_dotenv
from bot import DiscordBot

def setup_logging(debug_mode=False):
    """Configure logging with appropriate level based on debug mode"""
    log_level = logging.DEBUG if debug_mode else logging.INFO
    
    # Configure root logger
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("discord_bot.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Make discord.py logging less verbose in non-debug mode
    if not debug_mode:
        logging.getLogger('discord').setLevel(logging.WARNING)
        logging.getLogger('discord.http').setLevel(logging.WARNING)
        logging.getLogger('discord.gateway').setLevel(logging.WARNING)
    
    return logging.getLogger(__name__)

if __name__ == "__main__":
    # Parse command line arguments
    debug_mode = "--debug" in sys.argv
    
    # Set up logging
    logger = setup_logging(debug_mode)
    
    # Load environment variables
    load_dotenv()
    TOKEN = os.getenv("DISCORD_TOKEN")
    
    if not TOKEN:
        logger.error("No Discord token found. Please set the DISCORD_TOKEN environment variable.")
        sys.exit(1)
    
    try:
        # Initialize the bot
        prefix = "!!"  # Use different prefix for development to avoid conflicts
        bot = DiscordBot(prefix)
        
        logger.info(f"Starting Discord bot in {'DEBUG' if debug_mode else 'NORMAL'} mode...")
        logger.info(f"Using command prefix: {prefix}")
        
        # Run the bot
        bot.run(TOKEN)
    except Exception as e:
        logger.error(f"Failed to start the bot: {e}", exc_info=debug_mode)
        sys.exit(1)
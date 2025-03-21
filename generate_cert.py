"""
Script to generate self-signed SSL certificates for HTTPS
"""
import os
from OpenSSL import crypto

def generate_self_signed_cert(cert_file="cert.pem", key_file="key.pem"):
    """Generate a self-signed certificate and key pair"""
    # Create a key pair
    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, 2048)
    
    # Create a self-signed certificate
    cert = crypto.X509()
    cert.get_subject().C = "US"
    cert.get_subject().ST = "California"
    cert.get_subject().L = "San Francisco"
    cert.get_subject().O = "DiscordBot"
    cert.get_subject().OU = "Discord Bot Uptime Server"
    cert.get_subject().CN = "localhost"
    cert.set_serial_number(1000)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(10*365*24*60*60)  # 10 years validity
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(k)
    cert.sign(k, 'sha256')
    
    # Write certificate and key to files
    with open(cert_file, "wb") as f:
        f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
    
    with open(key_file, "wb") as f:
        f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k))
    
    print(f"Self-signed certificate generated: {cert_file}, {key_file}")
    return cert_file, key_file

if __name__ == "__main__":
    generate_self_signed_cert()
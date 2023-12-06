from urllib.parse import urlparse, parse_qs
from cryptography.fernet import Fernet


def extract_video_id(youtube_url):
    """
    Extracts the YouTube video ID from a YouTube URL.
    """
    url_data = urlparse(youtube_url)
    query_params = parse_qs(url_data.query)

    if 'v' in query_params:
        return query_params['v'][0]
    elif 'youtu.be' in url_data.netloc:
        return url_data.path[1:]  # Remove leading '/'
    else:
        return None
    

def encrypt_link(original_link, encryption_key):
    cipher_suite = Fernet(encryption_key)
    encrypted_link = cipher_suite.encrypt(original_link.encode('utf-8'))
    return encrypted_link

def decrypt_link(encrypted_link, encryption_key):
    cipher_suite = Fernet(encryption_key)
    decrypted_link = cipher_suite.decrypt(encrypted_link).decode('utf-8')
    return decrypted_link


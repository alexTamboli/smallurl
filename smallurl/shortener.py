import random
import string
import hashlib
import base64

class Shortener:
    token_size = 5
    
    def __init__(self, token_size=None) -> None:
        self.token_size = token_size if token_size is not None else 5
        
    def issue_token(self):
        letters = string.ascii_letters
        return ''.join(random.choice(letters) for i in range(self.token_size))
    
    def shorten_url(self, long_url):
        sha256_hash = hashlib.sha256(long_url.encode()).digest()

        hash_bytes = sha256_hash[:(self.token_size+1)]

        base64_encoded = base64.b64encode(hash_bytes).decode()

        token = base64_encoded.replace('/', '_').replace('+', '-')

        short_token = token[:self.token_size]

        return short_token
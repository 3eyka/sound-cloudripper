import requests
import re
import sys
from colorama import Fore, Back, Style
from urllib.parse import urlparse, urlunparse
import random
import string

def check():
    while(True):
        characters = string.ascii_letters + string.digits  # Uppercase letters, lowercase letters, and digits
        rand = ''.join(random.choice(characters) for _ in range(5))
        short_url = "https://on.soundcloud.com/" + rand
        # Send Boobs
        response = requests.get(short_url, allow_redirects=False)

        if response.status_code == 302:
            #Get Redirect, get URL
            full_url = response.headers.get('Location', '')
            parsed_url = urlparse(full_url)
            url_final = urlunparse(parsed_url._replace(query=''))

            # Regex pour verifier presence de code private
            match = re.search(r's-[a-zA-Z0-9]{11}', url_final)

            if match:
                print(Fore.GREEN + "[+]", url_final)
            
        check()

check()

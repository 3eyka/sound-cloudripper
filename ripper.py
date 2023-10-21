import os
import asyncio
import requests
import re
import warnings
from colorama import Fore
from urllib.parse import urlparse, urlunparse
import random
import string

# Ignore RuntimeWarning
warnings.simplefilter('ignore', RuntimeWarning)

async def check_single_url(short_url, valid_urls, hits_file):
    response = await asyncio.to_thread(requests.get, short_url, allow_redirects=False)

    if response.status_code == 302:
        full_url = response.headers.get('Location', '')
        parsed_url = urlparse(full_url)
        url_final = urlunparse(parsed_url._replace(query=''))

        match = re.search(r's-[a-zA-Z0-9]{11}', url_final)

        if match:
            if short_url not in valid_urls:
                valid_urls.add(short_url)  # Add URL to set
                print(Fore.GREEN + "[+] Valid URL : ", short_url)
                hits_file.write(short_url + "\n")
            else:
                print(Fore.RED + "[-] Invalid URL : ", short_url)
        else:
            print(Fore.RED + "[-] Invalid URL : ", short_url)
    else:
        print(Fore.RED + "[-] Invalid URL : ", short_url)

async def check(num_urls_to_generate):
    valid_urls = set()  # Use a set to store unique URLs

    folder_name = input("\nFolder name : ")
    file_name = input("File name (e.g. hits.txt) : ")

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    with open(os.path.join(folder_name, file_name), "w") as hits_file:
        tasks = []  # Tasks list

        print("\n\n< Checking... >\n")  # Checking message

        for _ in range(num_urls_to_generate):
            characters = string.ascii_letters + string.digits
            rand = ''.join(random.choice(characters) for _ in range(5))
            short_url = "https://on.soundcloud.com/" + rand

            task = check_single_url(short_url, valid_urls, hits_file)
            tasks.append(task)

        await asyncio.gather(*tasks)  # Wait for every tasks to be done

    print(Fore.YELLOW + f"\n[!] Finished ! {len(valid_urls)} private tracks found on {num_urls_to_generate} generated URL <3\n")

if __name__ == "__main__":
    num_urls = int(input("\nNumber of Short URL : "))
    asyncio.run(check(num_urls))

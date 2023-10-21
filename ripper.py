import os
import asyncio
import requests
import re
import warnings
from colorama import Fore
from urllib.parse import urlparse, urlunparse
import random
import string
import xml.etree.ElementTree as ET

# Ignore RuntimeWarning
warnings.simplefilter('ignore', RuntimeWarning)

async def check_single_url(short_url, valid_urls, xml_root):
    response = await asyncio.to_thread(requests.get, short_url, allow_redirects=False)

    if response.status_code == 302:
        full_url = response.headers.get('Location', '')
        parsed_url = urlparse(full_url)
        url_final = urlunparse(parsed_url._replace(query=''))

        match = re.search(r's-[a-zA-Z0-9]{11}', url_final)

        if match:
            if short_url not in valid_urls:
                valid_urls.add(short_url)
                entry = ET.SubElement(xml_root, "track")
                entry.text = short_url + "\n"
                print(Fore.GREEN + "[+] Valid URL : ", short_url)
            else:
                print(Fore.YELLOW + "[*] URL already recorded : ", short_url)
        else:
            print(Fore.RED + "[-] Invalid URL : ", short_url)

async def check(num_urls_to_generate):
    valid_urls = set()

    folder_name = "Hits"
    file_name = "hits.xml"

    if os.path.exists(os.path.join(folder_name, file_name)):
        existing_tree = ET.parse(os.path.join(folder_name, file_name))
        existing_root = existing_tree.getroot()

        for track in existing_root:
            url = track.text.strip()
            valid_urls.add(url)

    xml_root = ET.Element("tracks")

    tasks = []

    print("\n\n< Checking... >\n")

    for _ in range(num_urls_to_generate):
        characters = string.ascii_letters + string.digits
        rand = ''.join(random.choice(characters) for _ in range(5))
        short_url = "https://on.soundcloud.com/" + rand

        task = check_single_url(short_url, valid_urls, xml_root)
        tasks.append(task)

    await asyncio.gather(*tasks)

    existing_root.extend(xml_root)

    with open(os.path.join(folder_name, file_name), "wb") as xml_file:
        xml_tree = ET.ElementTree(existing_root)
        xml_tree.write(xml_file, encoding="utf-8", xml_declaration=True)

    print(Fore.YELLOW + f"\n[!] Finished ! {len(valid_urls)} private tracks found on {num_urls_to_generate} generated URL <3\n")

if __name__ == "__main__":
    num_urls = int(input("\nNumber of Short URL : "))
    asyncio.run(check(num_urls))

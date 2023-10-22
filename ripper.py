#sound-cloudripper, [scalable update]
import argparse
import asyncio
import random
import string
import aiohttp
import re
import os
from colorama import Fore
import xml.etree.ElementTree as ET
from urllib.parse import urlparse, urlunparse

#=====================CORE=====================================>>
#==============================================================>>
async def fetch_url(session, url):
    async with session.get(url, allow_redirects=False) as response:
        return response, await response.text()

async def main(num_runs):
    #keep track of total requests
    total_requests = 0
    matched_urls = []
    print(Fore.LIGHTGREEN_EX + "[!] harvesting private tracks..." + Fore.RESET)
    for _ in range(num_runs):
        #random link gen
        urls = [f"https://on.soundcloud.com/{''.join(random.choice(string.ascii_letters + string.digits) for _ in range(5))}" for _ in range(100)]
        #aiohttp x async super multithread of doom
        async with aiohttp.ClientSession() as session:
            tasks = [fetch_url(session, url) for url in urls]
            responses = await asyncio.gather(*tasks)

            for url, (response, text) in zip(urls, responses):
                #intercept redirection code, extract Location URL
                if response.status == 302:
                    full_url = response.headers.get('Location', '')
                    url_final = urlunparse(urlparse(full_url)._replace(query=''))
                    #Regex to match private tokens
                    match = re.search(r'/s-[a-zA-Z0-9]{11}', url_final)

                    if match:
                        if(args.verbose or args.very_verbose):
                            print(Fore.LIGHTCYAN_EX + "[+] match : ", url_final)
                        total_requests += 1
                        matched_urls.append(url_final)
                    else:
                        if(args.very_verbose):
                            print(Fore.YELLOW + "[-] not private")
                        total_requests += 1
                else:
                    if(args.very_verbose):
                        print(Fore.RED + "[x] not found")
                    total_requests += 1
    #============================================================================================
    #===================ON PROGRAM FINISH========================================================

    print(Fore.LIGHTGREEN_EX + "[!] finished ! matched", len(matched_urls) ,"links, for a total of" , total_requests ,"requests <3")

    #END OF MAIN SECTION ===============================================================================

    if args.loop is None:
        print(Fore.LIGHTYELLOW_EX + "[?] use 'ripper.py -h' or '--help' to view commands")

    #export to xml if xml switch is true
    if (args.xml_export):
        xml_export(matched_urls)


#=======================additional functions=====================================================================
def xml_export(links):
    print(Fore.MAGENTA + "[+] XML export...")
    data = ET.Element("data")
    if not os.path.exists("output.xml"):
        print(Fore.MAGENTA + "[+] creating output.xml...")
        data = ET.Element("data")
    else:
        tree = ET.parse("output.xml")
        data = tree.getroot()

    for link in links:
        random_name = link.split("/")[-3]
        user_element = next((user for user in data.findall("user") if user.get("name") == random_name), None)

        if user_element is None:
            user_element = ET.Element("user")
            user_element.set("name", random_name)
            data.append(user_element)

        link_element = ET.Element("link")
        link_element.text = link
        user_element.append(link_element)
    ET.ElementTree(data).write("output.xml", encoding="utf-8", xml_declaration=True)
    print(Fore.GREEN + "[+] done !")




#ENTRY POINT
if __name__ == "__main__":
    print(Fore.LIGHTGREEN_EX + "------------------------------------------")
    print(Fore.LIGHTGREEN_EX + "/ / / / / " + Fore.LIGHTYELLOW_EX + "C L O U D R I P P E R" + Fore.LIGHTGREEN_EX + " / / / / /")
    print(Fore.LIGHTGREEN_EX + "------------------------------------------" + Fore.RESET)
    print(Fore.RESET + "created by " + Fore.MAGENTA + "yuuechka<3" + Fore.RESET + " & " + Fore.LIGHTRED_EX + "fancymalware(mk0)" + Fore.RESET)
    print(Fore.LIGHTGREEN_EX + "------------------------------------------" + Fore.RESET)
    #ARGS PARSER --------------------------------------------------------------------------------------------
    parser = argparse.ArgumentParser(description="-----manual-----")
    parser.add_argument('-l', '--loop', type=int, help="the program will loop n times")
    parser.add_argument('-x', '--xml_export', action='store_true', help="export found tracks in a XML file")
    parser.add_argument('-v', '--verbose', action='store_true', help="verbose mode, show more informations")
    parser.add_argument('-vv', '--very_verbose', action='store_true', help="very verbose mode, show ALL informations")
    #todo : -r <-> bruteforces private token
    #todo : -p <-> proxylist support ?
    #--------------------------------------------------------------------------------------------------------
    # take arguments in args
    args = parser.parse_args()
    
    #num_runs = int(input("how much cycles (need to to switchs instead)>"))
    if(args.loop is not None):
        runs = args.loop * 100
        print(Fore.LIGHTGREEN_EX + "[!] starting the script for approximately ", runs, " requests...")
        asyncio.run(main(args.loop))
    else:
        print(Fore.LIGHTGREEN_EX + "[!] starting the script with the default value (only one cycle)")
        asyncio.run(main(1))

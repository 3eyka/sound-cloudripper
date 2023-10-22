# sound-cloudripper

[![Python](https://img.shields.io/badge/Python-v3.11-yellow)]()

a tool whichs basically finds private soundcloud tracks by bruteforcing shareable links of on.soundcloud.com

---
##### Educationnal purposes only, use it at your own risk.
---

### Dependencies
- aiohttp
- asyncio
- argparse
- colorama

---
### CLI Arguments
- -h  |  print out the possible commands
---
- -r  |  base number of requests
- -t  |  number of simultaneous threads **(multiplies the number of requests)**
---
- -x  |  exports the positive results in a xml file (output.xml), *and updates it if it already exists.*
---
- -v   |  prompts positive results in real time
- -vv |  prompts positive and negative results in real time

---
### Usage
you can run the script without any arguments, the default values are enough for testing (25 requests, 1 thread, verbose mode).

##### Example usage with arguments
```
python3 ripper.py -r 5 -t 5 -x
(run cloudripper for 25(5*5) requests, and export positive results in xml)
```
---
### why python ?
bc we're dumb af lol

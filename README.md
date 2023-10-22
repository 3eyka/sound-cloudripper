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
- -h will print out the possible commands
- -x will output the positive results in a xml file
- -l <int> will make the program run for n times (*one run[default] is ~100 requests*)
- -v will prompt positive results in real time
- -vv will prompt positive and negative results in real time

---
### Typical usage
```
python3 ripper.py -x -l <int>
(run ripper for n times and outputs positive results in xml file)
```
---
### why python ?
bc we're dumb af lol

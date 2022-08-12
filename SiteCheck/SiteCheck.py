"""
/***************************************************************************\
| SiteCheck                  Python version 3.10                            |
| (c) GamerGun               https://t.me/GamerGun                          |
|---------------------------------------------------------------------------|
| Site: https://it-project.ga/                                              |
| Github: https://github.com/IT-PROJECT-HUB/IT-PROJECT                      |
\***************************************************************************/
"""

import requests as r
from sys import argv
from datetime import datetime as d

START_MODE = True if len(argv[1:]) else False
if START_MODE: SAVE_LOGS = True if "-l" in argv[1:] else False
else: SAVE_LOGS = False
LOGS = ""

# Список сайтов для проверки
IT_PROJECT = ['https://it-project.ga/',
              'https://it-project.ga/about',
              'https://it-project.ga/projects',
              'https://it-project.ga/products',
              'https://it-project.ga/news',
              'https://it-project.ga/faq',
              'https://it-project.ga/profile',
              'https://it-project.ga/chat',
              'https://it-project.ga/profile?name=Neor',
              'https://it-project.ga/profile?name=GamerGun',
              'https://it-project.ga/profile?name=dreadhorse',
              'https://it-project.ga/profile?name=LordAdwond',
              'https://it-project.ga/profile?name=innxrmxst',
              'https://it-project.ga/profile?name=ertadan',
              'https://it-project.ga/profile?name=BraveSpirit',
              'https://it-project.ga/profile?name=meltinmilk',
              'https://it-project.ga/profile?name=SHELESTDM']

for site in IT_PROJECT:
    print(f"| PROCESS | {site}", end="")
    try: status_code = r.request("get", site).status_code
    except: status_code = 404
    match f"{status_code}"[0]:
        case '1': print(f"\r| \033[33;1;1m{status_code}\033[0m | {site}{' ' * (len(f'| PROCESS | {site}') - len(f'|     | {site}'))}")
        case '2': print(f"\r| \033[32;1;1m{status_code}\033[0m | {site}{' ' * (len(f'| PROCESS | {site}') - len(f'|     | {site}'))}")
        case '3': print(f"\r| \033[35;1;1m{status_code}\033[0m | {site}{' ' * (len(f'| PROCESS | {site}') - len(f'|     | {site}'))}")
        case '4': print(f"\r| \033[31;1;1m{status_code}\033[0m | {site}{' ' * (len(f'| PROCESS | {site}') - len(f'|     | {site}'))}")
        case '5': print(f"\r| \033[31;1;1m{status_code}\033[0m | {site}{' ' * (len(f'| PROCESS | {site}') - len(f'|     | {site}'))}")
        case _: print(f"\r| \033[34;1;1m{status_code}\033[0m | {site}{' ' * (len(f'| PROCESS | {site}') - len(f'|     | {site}'))}")
    LOGS += f"| {status_code} | {site}\n"

if SAVE_LOGS: __f = open(f"C:/Users/User/Desktop/site_check_log_{str(d.timestamp(d.utcnow())).split('.')[0]}.txt", 'w', encoding='utf-8'); __f.write(LOGS); __f.close()

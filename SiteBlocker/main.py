import time
from datetime import datetime

hosts = r"C:\Windows\System32\drivers\etc\hosts"  # Linux − etc/hosts
redirect = "0.0.0.0"

websites = ["www.facebook.com", "facebook.com",
            "www.youtube.com", "youtube.com",
            "twitter.com", "www.twitter.com"]

while True:
    if datetime.now().hour >= 8 and datetime.now().hour < 18:
        print("Access Denied")
        file = open(hosts, "r+")
        content = file.read()

        for website in websites:
            if website not in content:
                file.write(redirect + " " + website + "\n")
    else:
        print("Access Allowed")
        file = open(hosts, 'r+')
        content = file.readlines()
        file.seek(0)

        for line in content:
            if not any(website in line for website in websites):
                file.write(line)
            file.truncate()

    time.sleep(5)

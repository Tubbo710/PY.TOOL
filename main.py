import os
import requests
import json
from pathlib import Path
import time 
Is_running = True

logo = """"
\033[1;30m██████╗ ██╗   ██╗████████╗ ██████╗  ██████╗ ██╗     
\033[1;30m██╔══██╗╚██╗ ██╔╝╚══██╔══╝██╔═══██╗██╔═══██╗██║     
\033[1;30m██████╔╝ ╚████╔╝    ██║   ██║   ██║██║   ██║██║     
\033[1;30m██╔═══╝   ╚██╔╝     ██║   ██║   ██║██║   ██║██║     
\033[1;30m██║        ██║██╗   ██║   ╚██████╔╝╚██████╔╝███████╗
\033[1;30m╚═╝        ╚═╝╚═╝   ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝\033[92m
                                                    """


while Is_running:
    os.system("title PY.TOOL")
    os.system("cls")
    print(logo)
    print("[1] : IP Lookup     ")
    print("[2] : IP Scanner    ")
    print("[3] : Process Hacker")
    print("[4] : Wireshark     ")
    print("")
    choice=input("Option: ")
    match choice:
        case "1":
            os.system("cls")
            print("IP LOOKUP \n")
            ip = input("Enter IP: ")
            os.system("cls")
            r = requests.get(f"http://ip-api.com/json/{ip}")
            data = r.json()
            while data.get("status") != "success":
                print("Please enter a valid IP address!")
                ip = input("Enter IP: ")
                r = requests.get(f"http://ip-api.com/json/{ip}")
                data = r.json()
            time.sleep(2)
            print("---------IP RESULTS---------\n")
            print(f"IP : {data["query"]}")
            print(f"Country: {data["country"]}")
            print(f"Country Code: {data["countryCode"]}")
            print(f"Region: {data["region"]}")
            print(f"Region Name: {data["regionName"]}")
            print(f"City: {data["city"]}")
            print(f"Latitude: {data["lat"]}")
            print(f"Longitude: {data["lon"]}")
            print(f"ISP: {data["isp"]}")
            print(f"ORG : {data["org"]}")
            Is_running = False
        case "2":
            os.system("cls")
            folder = Path(__file__).resolve().parent
            exe = Path(fr"{folder}\Functions\Angry IP scanner\ipscan.exe")
            if exe.exists():
                os.startfile(exe)
                print("IP scanner has successfully been launched...")
                time.sleep(5)
            else:
                print(f"Not found: ", exe)
                Is_running = False
        case "3":
            os.system("cls")
            folder = Path(__file__).resolve().parent
            exe = Path(fr"{folder}\Functions\ProcessHacker\ProcessHacker.exe")
            if exe.exists():
                os.startfile(exe)
                print("Process Hacker has successfully been launched...")
                time.sleep(5)
            else:
                print(f"Not found: ", exe)
                Is_running = False

        case "4":
            os.system("cls")
            folder = Path(__file__).resolve().parent
            exe = Path(fr"{folder}\Functions\Wireshark\Wireshark.exe")
            if exe.exists():
                os.startfile(exe)
                print("Wireshark has successfully been launched...")
                time.sleep(5)
            else:
                print(f"Not found: ", exe)
                Is_running = False

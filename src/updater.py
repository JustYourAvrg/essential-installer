import requests
import json
import os
import subprocess
import platform

from .message import Message
from .version import __VERSION__

local_version = __VERSION__ 

def check_version():
    try:
        response = requests.get(url="https://api.github.com/repos/justyouravrg/essential-installer/releases/latest")
        response_json = json.loads(response.text)
        fetched_version = response_json['tag_name']

        if fetched_version != local_version:
            return fetched_version
        
        return True

    except Exception as e:
        Message.showmsg("ERROR", e)


def check_git_installed():
    try:
        # Check if git is installed
        subprocess.run(['git', '--version'])
        return True
    except Exception as e:
        Message.showmsg("ERROR", e)
        return False
    

def run_uninstaller():
    # Check if git is installed
    if check_git_installed():
        return True
    else:
        operation_system = platform.system().lower()

        val = Message.askyesno(title="Git not installed", message="Git has not been found on this system, to update you need to install git, would you like to install git?")
        if val:
            if operation_system == "windows":
                subprocess.run([f"{os.getcwd()}\\git\\windows\\Git-2.46.0-64-bit.exe"])
                return True
            else:
                Message.showmsg(title="Non-windows machine", message="It appears you aren't on a windows machine, please manually install git")
                return False
        
        return False


def check_git_installed():
    try:
        # Check if git is installed
        subprocess.run(['git', '--version'])
        return True
    except Exception as e:
        Message.showmsg("ERROR", e)
        return False

    

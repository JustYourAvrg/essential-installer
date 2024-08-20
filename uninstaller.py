import os
import requests
import json
import shutil
import tempfile
import subprocess

def uninstall_old_files():
    try:
        cur_dir = os.getcwd()
        temp_dir = tempfile.mkdtemp()

        response = requests.get(url="https://api.github.com/repos/justyouravrg/essential-installer/releases/latest")
        response_json = json.loads(response.text)
        ver = response_json['tag_name']

        shutil.move(src=f"{cur_dir}\\main.exe", dst=temp_dir)
        shutil.move(src=f"{cur_dir}\\uninstaller.py", dst=temp_dir)

        try:
            for item in os.listdir(cur_dir):
                if item == ".git":
                    continue

                try:
                    os.remove(item)
                except PermissionError:
                    shutil.rmtree(item, ignore_errors=True)
        except Exception as e:
            print(item, e)

        repo = "https://github.com/JustYourAvrg/essential-installer.git"
        subprocess.run(["git", "clone", "--branch", ver, repo, f"{cur_dir}\\new_code"])

        for item in os.listdir(f"{cur_dir}\\new_code\\"):
            if item == '.git':
                continue

            shutil.move(src=f"{cur_dir}\\new_code\\{item}", dst=cur_dir)

        os.system(f"rmdir /s /q {cur_dir}\\new_code\\.git")
        os.rmdir(f"{cur_dir}\\new_code")

    except Exception as e:  
        print("ERROR", ":", e)


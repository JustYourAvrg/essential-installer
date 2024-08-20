from src.gui import App
from src.message import Message
from src.updater import check_version, run_uninstaller
from uninstaller import uninstall_old_files

if __name__ == "__main__":
    ver = check_version()
    if ver != True:
        res = Message.askyesno(title="Install Update", message="A new update has been found would you like to update to the latest version?")

        Message.showmsg("WARNING", "D0 NOT CANCEL OR CLOSE THE COMMAND PROMPT WHILE UPDATING")
        if res:
            uninstall = run_uninstaller()
            if uninstall == True:
                uninstall_old_files()
                Message.showmsg("Update", "Updated successfully")

    else:
        app = App()


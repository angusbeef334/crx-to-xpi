import os
import sys
import threading
import requests
import shutil
import urllib.request
import stat
if sys.platform == 'win32': import winreg
else: winreg = None
import json
import tkinter
import tkinter.ttk
import tkinter.scrolledtext

root = tkinter.Tk()
frm = tkinter.ttk.Frame(root, padding=10)
textbox = tkinter.scrolledtext.ScrolledText(root, wrap=tkinter.WORD, width=60, height=20, state="normal")
textbox.pack(padx=10, pady=10, fill=tkinter.BOTH, expand=True)

manifest = {
    "name": "crx_to_xpi",
    "description": "Native app for converting crx to xpi",
    "path": "",
    "type": "stdio",
    "allowed_extensions": [ "crx-to-xpi@angusbeef334.github.io" ]
}

def log(msg):
    print(msg)
    textbox.insert(tkinter.END, f"{msg}\n")

def setup():
    log("Creating directories")
    cwd = os.getcwd()
    if os.path.exists(os.path.join(cwd, 'crx-to-xpi')):
        shutil.rmtree(os.path.join(cwd, 'crx-to-xpi'))
    os.mkdir(os.path.join(cwd, 'crx-to-xpi'))
    log("Successfully created directories")

def install(platform):
    log("Downloading binaries")
    filename = f"crx-to-xpi-{platform + ('.exe' if platform == 'win32' else '')}"
    output = os.path.join(os.getcwd(), 'crx-to-xpi', filename)

    url = 'https://api.github.com/repos/angusbeef334/crx-to-xpi/releases'
    log(f"GET {url}")
    res = requests.get(url).json()
    for asset in res[0]['assets']:
        if asset['name'] == filename:
            url = asset['browser_download_url']
            log(f"GET {url}")
            urllib.request.urlretrieve(url, output)

            st = os.stat(output)
            os.chmod(output, st.st_mode | stat.S_IEXEC)
            manifest['path'] = output
            log("Succesfully downloaded binaries")

def register(platform):
    log("Creating native manifest")
    match platform:
        case 'linux':
            directory = f'{os.path.expanduser('~')}/.mozilla/native-messaging-hosts/'
            os.makedirs(directory, exist_ok=True)
            with open(os.path.join(directory, 'crx_to_xpi.json'), 'w') as f:
                json.dump(manifest, f, indent=4)
        case 'darwin':
            directory = f'{os.path.expanduser('~')}/Library/Application Support/Mozilla/NativeMessagingHosts/'
            os.makedirs(directory, exist_ok=True)
            with open(os.path.join(directory, 'crx_to_xpi.json'), 'w') as f:
                json.dump(manifest, f, indent=4)
        case 'win32':
            manifest_path = os.path.join(os.getcwd(), 'crx-to-xpi', 'crx-to-xpi.json')
            with open(manifest_path, 'w') as f:
                json.dump(manifest, f, indent=4)

            reg_path = r"SOFTWARE\Mozilla\NativeMessagingHosts\crx-to-xpi"
            key = winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, None, 0, winreg.REG_SZ, manifest_path)

            winreg.CloseKey(key)
        case _:
            log('os not supported')
    log("Created native manifest")

def run_install():
    setup()
    install(sys.platform)
    register(sys.platform)
    log("Finished.")

if __name__ == "__main__":
    button = tkinter.ttk.Button(root, text="Install", 
        command=lambda: threading.Thread(target=run_install, daemon=True).start())
    button.pack(pady=5)

    button1 = tkinter.ttk.Button(root, text="Close", command=lambda: exit())
    button1.pack(pady=10)

    root.mainloop()
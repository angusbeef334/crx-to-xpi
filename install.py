import os
import sys
import requests
import shutil
import urllib.request
import stat
if sys.platform == 'win32': import winreg
else: winreg = None
import json

manifest = {
    "name": "crx_to_xpi",
    "description": "Native app for converting crx to xpi",
    "path": "",
    "type": "stdio",
    "allowed_extensions": [ "crx-to-xpi@angusbeef334.github.io" ]
}

def setup():
    cwd = os.getcwd()
    if os.path.exists(os.path.join(cwd, 'crx-to-xpi')):
        shutil.rmtree(os.path.join(cwd, 'crx-to-xpi'))
    os.mkdir(os.path.join(cwd, 'crx-to-xpi'))

def install(platform):
    filename = f"crx-to-xpi-{platform + ('.exe' if platform == 'win32' else '')}"
    output = os.path.join(os.getcwd(), 'crx-to-xpi', filename)

    url = 'https://api.github.com/repos/angusbeef334/crx-to-xpi/releases'
    res = requests.get(url).json()
    for asset in res[0]['assets']:
        if asset['name'] == filename:
            url = asset['browser_download_url']
            urllib.request.urlretrieve(url, output)

            st = os.stat(output)
            os.chmod(output, st.st_mode | stat.S_IEXEC)
            manifest['path'] = output

def register(platform):
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
            print('os not supported')

if __name__ == "__main__":
    setup()
    install(sys.platform)
    register(sys.platform)
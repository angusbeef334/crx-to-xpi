import os
import sys
import requests
import shutil
import urllib.request
import stat

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
                f.write(str(manifest).replace("'", '"'))
        case 'darwin':
            directory = f'{os.path.expanduser('~')}/Library/Application Support/Mozilla/NativeMessagingHosts/'
            os.makedirs(directory, exist_ok=True)
            with open(os.path.join(directory, 'crx_to_xpi.json'), 'w') as f:
                f.write(str(manifest))
        case 'win32':
            pass
        case _:
            print('os not supported')

if __name__ == "__main__":
    setup()
    install(sys.platform)
    register(sys.platform)
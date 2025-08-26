import os
import sys
import tempfile
import random
import requests
import shutil
import zipfile
import json

def validate_url(url):
    return url.startswith('http://') or url.startswith('https://')

def convert(file, out):
    is_url = validate_url(file)
    if not file.endswith('.crx') and not is_url:
        print('error: input file must be crx or url download')
        return
    if not out.endswith('.xpi'):
        out += ".xpi"
    if not is_url and not os.path.exists(file):
        print('error: input file does not exist')
        return
    if (is_url):
        try:
            fd, path = tempfile.mkstemp()
            print(f'downloading {file} to {path}')
            with os.fdopen(fd, 'wb') as tmpfile:
                res = requests.get(file)
                res.raise_for_status()
                tmpfile.write(res.content)
            file = path
        except Exception as e:
            print(f'error: could not download file: {e}')
            return
    
    with zipfile.ZipFile(file, 'r') as crx:
        extract_path = 'crx_temp_' + str(random.randint(0, 1000000))
        try:
            print(f'extracting crx to {os.path.join(tempfile.gettempdir(), extract_path)}')
            crx.extractall(path=os.path.join(tempfile.gettempdir(), extract_path))
        except Exception as e:
            print(f'error: could not extract crx file: {e}')
            return
        
        print('updating manifest.json')
        try:
            manifest_path = os.path.join(tempfile.gettempdir(), extract_path, 'manifest.json')
            with open(manifest_path, 'r') as f:
                manifest = f.read()

            manifest_content = json.loads(manifest)
            package_name = manifest_content.get('name', 'unknown')
            manifest_content.update({
                'browser_specific_settings': {
                    'gecko': {
                        'id': f'{package_name.lower().replace(" ", "_")}@example.com'
                    }
                }
            })

            with open(manifest_path, 'w') as f:
                f.write(json.dumps(manifest_content, indent=2))
        except Exception as e:
            print(f'error: could not update manifest.json: {e}')
            return

        try:
            print(f'creating xpi at {out}')
            shutil.make_archive(out, 'zip', os.path.join(tempfile.gettempdir(), extract_path))
            shutil.move(out + '.zip', out)
        except Exception as e:
            print(f'error: could not create xpi file: {e}')
            return

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print('command format: crx_to_xpi [filein] [fileout]')
        sys.exit()

    file_in = sys.argv[1]
    file_out = sys.argv[2]
    convert(file_in, file_out)
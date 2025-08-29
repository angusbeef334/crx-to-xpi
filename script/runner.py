import os
import sys
import tempfile
import random
import threading
import requests
import shutil
import zipfile
import time
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = 8000
filename = "out.xpi"

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ('/', f'/{filename}'):
            try:
                with open(filename, 'rb') as f:
                    self.send_response(200)
                    self.send_header("Content-Type", "application/x-xpinstall")
                    fs = os.fstat(f.fileno())
                    self.send_header("Content-Length", str(fs.st_size))
                    self.end_headers()
                    chunk_size = 64 * 1024  # 64KB
                    while True:
                        chunk = f.read(chunk_size)
                        if not chunk:
                            break
                        self.wfile.write(chunk)
            except FileNotFoundError:
                self.send_error(404, "File not found")
        else:
            self.send_error(404, "File not found")
        threading.Thread(target=lambda: (time.sleep(10), self.server.shutdown()), daemon=True).start()

class Converter:
    def validate_url(self, url):
        return url.startswith('http://') or url.startswith('https://')

    def convert(self, file, out):
        is_url = self.validate_url(file)
        if not file.endswith('.crx') and not is_url:
            print('error: input file must be crx or url download')
            return False
        if not out.endswith('.xpi'):
            out += ".xpi"
        if not is_url and not os.path.exists(file):
            print('error: input file does not exist')
            return False
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
                return False
        
        with zipfile.ZipFile(file, 'r') as crx:
            extract_path = 'crx_temp_' + str(random.randint(0, 1000000))
            try:
                print(f'extracting crx to {os.path.join(tempfile.gettempdir(), extract_path)}')
                crx.extractall(path=os.path.join(tempfile.gettempdir(), extract_path))
            except Exception as e:
                print(f'error: could not extract crx file: {e}')
                return False
            
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

                background = manifest_content.get('background')
                if background and 'service_worker' in background:
                    manifest_content['background'] = {
                        "scripts": [background['service_worker']]
                    }


                with open(manifest_path, 'w') as f:
                    f.write(json.dumps(manifest_content, indent=2))
            except Exception as e:
                print(f'error: could not update manifest.json: {e}')
                return False

            try:
                print(f'creating xpi at {out}')
                shutil.make_archive(out, 'zip', os.path.join(tempfile.gettempdir(), extract_path))
                shutil.move(out + '.zip', out)
            except Exception as e:
                print(f'error: could not create xpi file: {e}')
                return False
        return True

class Browser:
    def serve_file(self):
        server = HTTPServer(('', PORT), SimpleHandler)
        server.serve_forever()

    def install_extension(self, path):
        self.serve_file()
        return True

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print('command format: crx_to_xpi [filein] [fileout]')
        sys.exit()

    file_in = sys.argv[1]
    file_out = sys.argv[2]
    converter = Converter()
    converter.convert(file_in, file_out)
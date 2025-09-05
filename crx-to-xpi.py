#!/home/benjamin/coding/crx-to-xpi/.venv/bin/python3
import sys
import json
import struct
import os
import re
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
                        try:
                            self.wfile.write(chunk)
                        except ConnectionResetError:
                            break
            except FileNotFoundError:
                self.send_error(404, "File not found")
        else:
            self.send_error(404, "File not found")
        threading.Thread(target=lambda: (time.sleep(0.1), self.server.shutdown()), daemon=True).start()

class Converter:
    def validate_url(self, url):
        return url.startswith('http://') or url.startswith('https://')

    def convert(self, file, out):
        is_url = self.validate_url(file)
        if not file.endswith('.crx') and not is_url:
            print('error: input file must be crx or url download')
            return 'invalid-input-file'
        if not out.endswith('.xpi'):
            out += ".xpi"
        if not is_url and not os.path.exists(file):
            print('error: input file does not exist')
            return 'input-file-not-exists'
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
                return f'download-file: {e}'
        
        with zipfile.ZipFile(file, 'r') as crx:
            extract_path = 'crx_temp_' + str(random.randint(0, 1000000))
            try:
                print(f'extracting crx to {os.path.join(tempfile.gettempdir(), extract_path)}')
                crx.extractall(path=os.path.join(tempfile.gettempdir(), extract_path))
            except Exception as e:
                print(f'error: could not extract crx file: {e}')
                return f'crx-extract: {e}'
            
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
                            'id': f'{re.sub(r"[^a-z0-9\-._]", "_", package_name.lower())}@example.com'
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
                return f'update-manifest-error: {e}'

            try:
                print(f'creating xpi at {out}')
                shutil.make_archive(out, 'zip', os.path.join(tempfile.gettempdir(), extract_path))
                shutil.move(out + '.zip', out)
            except Exception as e:
                print(f'error: could not create xpi file: {e}')
                return f'create-xpi-error: {e}'
        return 'success'

class Browser:
    def serve_file(self):
        server = HTTPServer(('', PORT), SimpleHandler)
        server.serve_forever()

    def install_extension(self, path):
        thread = threading.Thread(target=self.serve_file)
        thread.start()
        return True

version = "136.0.0.0"

def getMessage():
    rawLength = sys.stdin.buffer.read(4)
    if len(rawLength) < 4:
        sys.exit(0)
    messageLength = struct.unpack('<I', rawLength)[0]
    remaining = messageLength
    chunks = []
    while remaining > 0:
        chunk = sys.stdin.buffer.read(remaining)
        if not chunk:
            sys.exit(0)
        chunks.append(chunk)
        remaining -= len(chunk)
    message = b''.join(chunks).decode('utf-8')
    return json.loads(message)

def encodeMessage(messageContent):
    encodedContent = json.dumps(messageContent).encode('utf-8')
    encodedLength = struct.pack('<I', len(encodedContent))
    return encodedLength + encodedContent

def sendMessage(encodedBytes):
    sys.stdout.buffer.write(encodedBytes)
    sys.stdout.buffer.flush()

def main():
    while True:
        received = getMessage()
        if isinstance(received, dict) and received.get("action") == "install":
            id = received.get("message")
            converter = Converter()
            browser = Browser()
            res = converter.convert(f'https://clients2.google.com/service/update2/crx?response=redirect&prodversion={version}&acceptformat=crx2,crx3&x=id%3D{id}%26uc', 'out.xpi')
            sendMessage(encodeMessage({
                "action": "convert",
                "result": "success" if res == 'success' else "failure",
                "reason": res,
            }))
            res1 = browser.install_extension('out.xpi')
            sendMessage(encodeMessage({
                "action": "install",
                "result": "success" if res1 == 'success' else "failure",
                "reason": res,
            }))

if __name__ == '__main__':
    main()
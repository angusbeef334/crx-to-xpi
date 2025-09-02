#!/home/benjamin/coding/crx-to-xpi/.venv/bin/python3
import sys
import json
import struct
from runner import Browser, Converter

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
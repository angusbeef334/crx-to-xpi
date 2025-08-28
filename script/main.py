#!/Users/benjamin/crx_to_xpi/script/.venv/bin/python3
import sys
import json
import struct
from runner import Browser, Converter

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
            converter = Converter()
            browser = Browser()
            res = converter.convert('https://clients2.google.com/service/update2/crx?response=redirect&prodversion=136.0.0.0&acceptformat=crx2,crx3&x=id%3Dfnjlfdbkccdjdimfeodmflindgceoadi%26uc', 'out.xpi')
            res1 = browser.install_extension('', 'out.xpi')
            sendMessage(encodeMessage({
                "result": "success" if res else "failure",
                "reason": "success" if res else "failure"
            }))
if __name__ == '__main__':
    main()
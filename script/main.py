#!/usr/bin/env python3
import sys
import json
import struct

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
            sendMessage(encodeMessage({"result": "success", "reason": "success"}))

if __name__ == '__main__':
    main()
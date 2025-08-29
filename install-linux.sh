#!/bin/sh

if !(command -v "python3"); then
	if !(command -v "python"); then
		echo "python not found, install to continue"
		exit
	else
		echo "fatty"
	fi
fi

if !(command -v "sed"); then
	echo "sed not found, install to continue"
	exit
fi

echo "Creating venv"
cd script
if !(python3 -m venv .venv); then
	echo "Failed to create venv"
	exit
fi

echo "Installing requests"
.venv/bin/python3 -m pip install requests

echo "Installing files"
sed -i "1 c\
#!${PWD}/.venv/bin/python3" main.py

sed -i '4 c\
	"path": "'"${PWD}"'/main.py",' crx_to_xpi.json

if !(mkdir -p ~/.mozilla/native-messaging-hosts/); then
	echo "Failed to create native messaging hosts directory"
	exit
fi
if !(cp crx_to_xpi.json ~/.mozilla/native-messaging-hosts/crx_to_xpi.json); then
	echo "Failed to install native messaging manifest"
	exit
fi

echo "Successfully installed files."
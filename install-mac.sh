#!/bin/sh

python_install() {
	if command -v "brew"; then
		echo "python not found, homebrew detected, install python3 with homebrew? [y/N] "
		read install
		if [ "$install" = "y" ] || [ "$install" = "Y" ]; then
			if brew install python3; then
				echo "successful install"
			else
				echo "failed to install python3 with homebrew"
				exit
			fi
		else
			echo "abort"
			exit
		fi
	else 
		echo "python not found, no supported package manager detected, install to continue"
		exit
	fi
}

sed_install() {
	if command -v "brew"; then
		echo "sed not found, homebrew detected, install sed with homebrew? [y/N] "
		read install
		if [ "$install" = "y" ] || [ "$install" = "Y" ]; then
			if brew install sed; then
				echo "successful install"
			else
				echo "failed to install sed with homebrew"
				exit
			fi
		else
			echo "abort"
			exit
		fi
	else 
		echo "sed not found, no supported package manager detected, install to continue"
		exit
	fi
}

if !(command -v "python3"); then
	if !(command -v "python"); then
		python_install
	else
		version=$(python --version)
		if [[ $version != "Python 3"* ]]; then
			python_install
		fi
	fi
fi

if !(command -v "sed"); then
	sed_install
fi

echo "Creating venv"
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

if !(mkdir -p "~/Library/Application Support/Mozilla/NativeMessagingHosts"); then
	echo "Failed to create native messaging hosts directory"
	exit
fi
if !(cp crx_to_xpi.json "~/Library/Application Support/Mozilla/NativeMessagingHosts/crx_to_xpi.json"); then
	echo "Failed to install native messaging manifest"
	exit
fi

echo "Successfully installed files."
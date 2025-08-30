#!/bin/sh

python_install() {
	if command -v "pacman"; then
		echo "python not found, pacman detected, install python3 with pacman? [y/N] "
		read install
		if [ "$install" = "y" ] || [ "$install" = "Y" ]; then
			if sudo pacman -S python3; then
				echo "successful install"
			else
				echo "failed to install python3 with pacman"
				exit
			fi
		else
			echo "abort"
			exit
		fi
	elif command -v "apt-get"; then
		echo "python not found, apt-get detected, install python3 with apt-get? [y/N] "
		read install
		if [ "$install" = "y" ] || [ "$install" = "Y" ]; then
			if sudo apt-get install python3; then
				echo "successful install"
			else
				echo "failed to install python3 with apt-get"
				exit
			fi
		else
			echo "abort"
			exit
		fi
	elif command -v "dnf"; then
		echo "python not found, dnf detected, install python3 with dnf? [y/N] "
		read install
		read install
		if [ "$install" = "y" ] || [ "$install" = "Y" ]; then
			if sudo dnf install python3; then
				echo "successful install"
			else
				echo "failed to install python3 with dnf"
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
	if command -v "pacman"; then
		echo "sed not found, pacman detected, install sed with pacman? [y/N] "
		read install
		if [ "$install" = "y" ] || [ "$install" = "Y" ]; then
			if sudo pacman -S sed; then
				echo "successful install"
			else
				echo "failed to install sed with pacman"
				exit
			fi
		else
			echo "abort"
			exit
		fi
	elif command -v "apt-get"; then
		echo "sed not found, apt-get detected, install sed with apt-get? [y/N] "
		read install
		if [ "$install" = "y" ] || [ "$install" = "Y" ]; then
			if sudo apt-get install sed; then
				echo "successful install"
			else
				echo "failed to install sed with apt-get"
				exit
			fi
		else
			echo "abort"
			exit
		fi
	elif command -v "dnf"; then
		echo "sed not found, dnf detected, install sed with dnf? [y/N] "
		read install
		read install
		if [ "$install" = "y" ] || [ "$install" = "Y" ]; then
			if sudo dnf install sed; then
				echo "successful install"
			else
				echo "failed to install sed with dnf"
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

if !(mkdir -p ~/.mozilla/native-messaging-hosts/); then
	echo "Failed to create native messaging hosts directory"
	exit
fi
if !(cp crx_to_xpi.json ~/.mozilla/native-messaging-hosts/crx_to_xpi.json); then
	echo "Failed to install native messaging manifest"
	exit
fi

echo "Successfully installed files."
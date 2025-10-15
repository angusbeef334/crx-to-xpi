# crx-to-xpi
Chrome extensions and Web Store for Firefox
Note: due to extension signing requirements from Mozilla, this extension can only work with Firefox ESR, Nightly, and Developer editions.
Note: While installing extensions in the Chrome Web Store, you will need to confirm installation after the file has been converted for Firefox use. This is a security requirement in Firefox.

## Prerequisites
* Firefox Developer/Nightly/ESR (normal version has strict extension signing requirements)
* Set `xpinstall.signatures.required` to `false` in `about:config`.
* Download `crx-to-xpi.xpi` from the Releases page. This will trigger an install automatically in Firefox.

## Installation
1. Download the install script corresponding to your platform from Releases.
2. For Linux and Mac systems, in the directory that the install file is located, run `chmod +x install-linux-x64` for linux, or `chmod +x install-darwin-universal`
3. Move the file to an installation directory (warning, if there is a directory named `crx-to-xpi` in the install script's working directory, it will be deleted)
4. Run the install script. It will download the native app and register it with Firefox.
5. Restart Firefox.
6. Navigate to the Chrome Web Store to test installing of an extension.

## Troubleshooting
### Installation
When running the install script, an error may be thrown such as the following:
`urllib.error.URLError: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1032)>`

To fix this, you must install the ca-certificates package for your OS.

Arch:
```
# pacman -S ca-certificates
# update-ca-trust
```

Debian: 
```
# apt install ca-certificates
# update-ca-certificates
```
Fedora: 
```
# sudo dnf install ca-certificates
# update-ca-trust
```

Mac (Homebrew):
```
$ brew install certifi
```
Then:

`$ export SSL_CERT_FILE=$(python -m certifi)`\
and rerun the script.

On Mac, even after adding executable permissions to the file, you may be denied permission by the system to run the file. To fix this, navigate to System Settings -> Privacy and Security, scroll down, then allow the app to run.

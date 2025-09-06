# crx-to-xpi
Chrome extensions and Web Store for Firefox
Note: due to extension signing requirements from Mozilla, this extension can only work with Firefox ESR, Nightly, and Developer editions.
Note: While installing extensions in the Chrome Web Store, you will need to confirm installation after the file has been converted for Firefox use. This is a security requirement in Firefox.

## Prerequisites
* Firefox Developer/Nightly/ESR (normal version has strict extension signing requirements)
* Set `xpinstall.signatures.required` to `false` in `about:config`.
* Download `crx-to-xpi.xpi` from the Releases page. This will trigger an install automatically in Firefox.

## Installation
1. Download the install script corresponding to your platform from Releases, and `chmod +x` for Linux and Mac.
2. Move the file to an installation directory (warning, if there is a directory named `crx-to-xpi` in the install script's working directory, it will be deleted)
3. Run the install script. It will download the native app and register it with Firefox.
4. Restart Firefox.
5. Navigate to the Chrome Web Store to test.

## Troubleshooting
### Installation
On Linux, when running the install script, an error may be thrown such as the following:
`urllib.error.URLError: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1032)>`

To fix this, you must install the ca-certificates package for your distro.\

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

Then restart your terminal.

If it still does not work, try:\
`python -m certifi`\
and if that outputs a location:\
`export SSL_CERT_FILE=$(python -m certifi)`\
and rerun the script.
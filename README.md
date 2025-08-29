# crx-to-xpi
Chrome extensions and Web Store for Firefox
Note: due to extension signing requirements from Mozilla, this extension can only work with Firefox ESR, Nightly, and Developer editions.
Note: some large extension files (currently) may fail silently with a connection reset error in the browser console.

## Installation
1. Open `about:config` and search for xpinstall.signatures.required
2. Set it to false (this is important, installs will fail silently without)
3. Download crx-to-xpi.xpi from Releases, and install it by dragging into a window open with `about:addons`
4. Run the correct install script for your platform (`install_linux.sh` `install_mac.sh` `install_win.bat`)

## Usage
Find an extension in the Chrome Web Store, and if the crx-to-xpi extension is set up correctly, a button 'Add to Firefox' will appear on the extension page. Click to begin the conversion and installation process.

## How it works
There are two components in this app - the python script and the browser extension. The extension uses Firefox Native Messaging to send extension data to the script, which downloads, extracts, modifies, and repackages the extension to work in Firefox. This is then hosted on localhost port 8000 (make sure it is open), and a message is sent back to the extension, which will open a new window pointing to localhost:8000 and install the converted extension. Then, the web server is closed.

Currently the app uses localhost:8000 to host and open the extension, as this appears to be the most user-friendly method to have the extension installed after conversion. Due to the security of Firefox, there must be a user prompt before installing an extension, and the extension cannot come from a loose file.
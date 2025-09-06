# crx-to-xpi
Chrome extensions and Web Store for Firefox
Note: due to extension signing requirements from Mozilla, this extension can only work with Firefox ESR, Nightly, and Developer editions.

## Installation
1. Open `about:config` and search for xpinstall.signatures.required
2. Set it to false (this is important, installs will fail silently without)
3. Download crx-to-xpi.xpi from Releases, and install it by dragging into a window open with `about:addons`
4. Clone the repo (Code -> Download ZIP then extract), or `git clone`
4. Run the correct install script for your platform (`install_linux.sh` `install_mac.sh` `install_win.bat`)
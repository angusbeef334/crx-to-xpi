# crx-to-xpi
A tool for converting Google Chrome .crx extension files to .xpi files for use in Firefox.

Usage:
`python3 main.py [source] [out]`
`source` can be a URL or local file.
`out` is the output location of the converted xpi file.

Please note: You must be using Firefox Nightly, Developer, or ESR versions, and set `xpinstall.signatures.required` to false in about:config in order to use the xpi files outputted from this tool.

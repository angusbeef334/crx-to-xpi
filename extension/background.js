var port = browser.runtime.connectNative("crx_to_xpi");

port.onMessage.addListener((response) => {
  console.log("Received: " + response);
});

browser.browserAction.onClicked.addListener(() => {
  console.log("Sending:  ping");
  port.postMessage("ping");
});
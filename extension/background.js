function onResponse(response) {
  const res = JSON.stringify(response);
  console.log(`[crx-to-xpi] received from native: ${res}`);
}

function onError(error) {
  console.log(`[crx-to-xpi] err from native: ${error}`);
}

browser.runtime.onMessage.addListener(async (message, sender) => {
  console.log(`[crx-to-xpi] sending to native (from ${JSON.stringify(sender)}): ${JSON.stringify(message)}`);
  let sending = browser.runtime.sendNativeMessage("crx_to_xpi", message);
  sending.then(onResponse, onError);
  console.log(`[crx-to-xpi] received from native: ${JSON.stringify(await sending)}`)
  return JSON.stringify(await sending);
});
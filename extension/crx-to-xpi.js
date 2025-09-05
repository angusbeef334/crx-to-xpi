let installing = false;
let timeout = null;

function add(button) {
  installing = true;
  button.textContent = "Converting...";
  const split = location.href.split('/');
  const id = split[split.length - 1].split('?')[0];
  browser.runtime.sendMessage({ action: "install", message: id })
    .then(() => {
      button.removeEventListener('click', add);
      button.addEventListener('click', install);
      button.textContent = "Install";
      timeout = setTimeout(() => {
        installing = false;
      }, 5000);
    })
    .catch((error) => {
      console.log(`Failed to install extension: ${error}`);
      alert(`Failed to install extension: ${error}`);
      document.getElementById('crx-to-xpi-install').textContent = "Add to Firefox";
    });
}

function install() {
  if (timeout) {
    clearTimeout(timeout);
    timeout = null;
  }
  installing = false;
  window.location.href = ('http://localhost:8000');
}

function replace() {
  if (installing) return;
  const btn = document.getElementsByClassName('UywwFc-LgbsSe UywwFc-LgbsSe-OWXEXe-dgl2Hf UywwFc-StrnGf-YYd4I-VtOx3e UywwFc-kSE8rc-FoKg4d-sLO9V-YoZ4jf')[0] || document.getElementById('crx-to-xpi-install');
  const newbtn = document.createElement("button");
  newbtn.id = "crx-to-xpi-install";
  newbtn.textContent = "Add to Firefox";
  newbtn.addEventListener('click', (e) => add(e.target));
  if (btn && newbtn) btn.replaceWith(newbtn);
}

setInterval(replace, 1000);

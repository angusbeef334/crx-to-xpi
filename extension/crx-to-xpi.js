let installing = false;

function add() {
  let button = document.getElementById('crx-to-xpi-install');
  button.innerText = "Converting...";
  const split = location.href.split('/');
  const id = split[split.length - 1].split('?')[0];
  browser.runtime.sendMessage({ action: "install", message: id })
    .then(() => {
      installing = true;
      button.removeEventListener('click', add);
      button.addEventListener('click', install);
      button.innerText = "Install";
    })
    .catch((error) => {
      console.log(`Failed to install extension: ${error}`);
      alert(`Failed to install extension: ${error}`);
      document.getElementById('crx-to-xpi-install').innerText = "Add to Firefox";
    });
}

function install() {
  window.open('http://localhost:8000');
  location.reload();
}

function replace() {
  if (installing) return;
  const btn = document.getElementsByClassName('UywwFc-LgbsSe UywwFc-LgbsSe-OWXEXe-dgl2Hf UywwFc-StrnGf-YYd4I-VtOx3e UywwFc-kSE8rc-FoKg4d-sLO9V-YoZ4jf')[0];
  const newbtn = document.createElement("button");
  newbtn.id = "crx-to-xpi-install";
  newbtn.textContent = "Add to Firefox";
  newbtn.addEventListener('click', () => add());
  if (btn && newbtn) btn.replaceWith(newbtn);
}

setInterval(replace, 1000);

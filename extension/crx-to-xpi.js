function callback(ret) {
  window.open('http://localhost:8000');
}

function add() {
  //browser.management.install("/Users/benjamin/crx_to_xpi/script/out.xpi"); 
  const split = location.href.split('/');
  const id = split[split.length - 1].split('?')[0];
  browser.runtime.sendMessage({ action: "install", message: id }).then(callback);
}

const btn = document.getElementsByClassName('UywwFc-LgbsSe UywwFc-LgbsSe-OWXEXe-dgl2Hf UywwFc-StrnGf-YYd4I-VtOx3e UywwFc-kSE8rc-FoKg4d-sLO9V-YoZ4jf')[0];
const newbtn = document.createElement("button");
newbtn.textContent = "Add to Firefox";
newbtn.addEventListener('click', () => add());
btn.replaceWith(newbtn);
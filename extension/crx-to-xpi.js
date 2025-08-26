function add() {
  const split = location.href.split('/');
  alert(split[split.length - 1]);
}

const btn = document.getElementsByClassName('UywwFc-LgbsSe UywwFc-LgbsSe-OWXEXe-dgl2Hf UywwFc-StrnGf-YYd4I-VtOx3e UywwFc-kSE8rc-FoKg4d-sLO9V-YoZ4jf')[0];
const newbtn = document.createElement("button");
newbtn.textContent = "Add to Firefox";
btn.replaceWith(newbtn);
newbtn.addEventListener('click', () => add());
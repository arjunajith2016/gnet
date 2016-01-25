var navbar = document.getElementById('navbar');
var myDiv = document.getElementById("output");
var chatbox = document.getElementById("chatbox");

var brightness = 255;

function onScroll(e) {
  window.scrollY >= 335 ? navbar.classList.add('foo') : navbar.classList.remove('foo');
  //window.scrollY >= 335 ? navbar.style.backgroundColor='rgb($brightness--,$brightness,$brightness)' : navbar.style.backgroundColor='rgb(brightness++brightness,brightness)';
}

function onClick(e) {

myDiv.scrollTop = myDiv.scrollHeight;
chatbox.value='';
}

document.addEventListener('scroll', onScroll);
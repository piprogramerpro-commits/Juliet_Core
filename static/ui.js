let mode = "general";

function setMode(m){ mode = m; }

async function send(){
let input = document.getElementById("input");
let msg = input.value;
input.value="";

add(msg,"user");

let res = await fetch("/chat",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({message:msg,mode:mode})
});

let reader = res.body.getReader();
let decoder = new TextDecoder();

let full="";
let box = add("", "bot");

while(true){
const {done,value}=await reader.read();
if(done) break;

full+=decoder.decode(value);
box.innerText=full;
}
}

function add(text,type){
let chat=document.getElementById("chat");
let div=document.createElement("div");
div.className=type;
div.innerText=text;
chat.appendChild(div);
return div;
}

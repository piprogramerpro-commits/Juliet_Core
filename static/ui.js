async function send(){
    let input = document.getElementById("input");
    let msg = input.value;
    input.value="";

    addUser(msg);

    let res = await fetch("/chat",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({message:msg})
    });

    let data = await res.json();
    renderBot(data.response);
}

function addUser(text){
    chat.innerHTML += `<div class="msg"><div class="bubble">${text}</div></div>`;
}

function renderBot(text){
    let container = document.createElement("div");
    container.className="msg";

    let avatar = `<div class="avatar">⭐👑</div>`;
    let bubble = document.createElement("div");
    bubble.className="bubble";

    container.innerHTML = avatar;
    container.appendChild(bubble);
    chat.appendChild(container);

    let parts = text.split("\n\n");

    parts.forEach(p=>{
        if(p.includes("```")){
            let code = p.replace(/```/g,"");
            bubble.innerHTML += `
            <div class="code">
                <div class="copy" onclick="navigator.clipboard.writeText(\`${code}\`)">📋</div>
                <pre>${code}</pre>
            </div>`;
        } else {
            bubble.innerHTML += `<p>${p.replace(/\*\*(.*?)\*\*/g,"<b>$1</b>")}</p>`;
        }
    });
}

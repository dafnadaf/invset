if(!sessionStorage.getItem("auth"))location.href="index.html";
const list=document.getElementById("list");
let store=JSON.parse(localStorage.getItem("stream")||"[]");
function render(){
  list.innerHTML="";
  store.forEach((m,i)=>{
    const tr=document.createElement("tr");
    tr.innerHTML=`<td>${m.ts}</td><td>${m.txt}</td><td><button class="secondary" data-i=${i}>🗑</button></td>`;
    list.appendChild(tr);
  });
}
render();
document.getElementById("add").addEventListener("click",()=>{
  const txt=document.getElementById("json").value.trim();
  if(!txt)return;
  store.unshift({ts:new Date().toLocaleString(),txt});
  localStorage.setItem("stream",JSON.stringify(store.slice(0,20)));
  render();
});
list.addEventListener("click",e=>{
  if(e.target.dataset.i!==undefined){
    store.splice(e.target.dataset.i,1);
    localStorage.setItem("stream",JSON.stringify(store));
    render();
  }
});

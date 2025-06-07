if(!sessionStorage.getItem("auth"))location.href="index.html";
const sliders=document.querySelectorAll("input[type=range]");
const result=document.getElementById("result");
const ctx=document.getElementById("hist").getContext("2d");
let chart = new Chart(ctx,{
  type:"bar",
  data:{labels:[],datasets:[{label:"freq",data:[],backgroundColor:"#60a5fa"}]},
  options:{scales:{y:{beginAtZero:true}}}
});
function simulate(){
  const vals=[...sliders].map(s=>Number(s.value));
  let score=80+vals.reduce((s,v)=>s+v*5,0);
  score=Math.max(0,Math.min(100,score));
  result.textContent= score>85?"AAA": score>70?"AA": score>55?"A":"BBB";
  const bins=15, arr=[];
  for(let i=0;i<500;i++){let sc=score+Math.random()*10-5;arr.push(Math.round(sc));}
  const hist=Array(bins).fill(0), step=100/bins;
  arr.forEach(v=>{const idx=Math.min(bins-1,Math.floor(v/step));hist[idx]++;});
  chart.data.labels=[...Array(bins)].map((_,i)=>Math.round(i*step));
  chart.data.datasets[0].data=hist; chart.update();
}
sliders.forEach(s=>{s.addEventListener("input",()=>{s.nextElementSibling.textContent=`${s.value}%`});});
document.getElementById("run").addEventListener("click",simulate);
simulate();

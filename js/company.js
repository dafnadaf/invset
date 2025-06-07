if(!sessionStorage.getItem("auth"))location.href="index.html";
const params=new URLSearchParams(location.search);
const name=params.get("c")||"X Company";
document.getElementById("cname").textContent=name;
const shapLabels=["Driver","Debt","Profit Margin","Expenses","Liquidity"];
const shapVals=[0.8,-0.4,0.32,0.2,0.12];
new Chart(document.getElementById("shap"),{
  type:"bar",
  data:{labels:shapLabels,
        datasets:[{data:shapVals,
                   backgroundColor:shapVals.map(v=>v>0?"#3b82f6":"#ef4444")}]},
  options:{indexAxis:"y",plugins:{legend:{display:false}}}
});
new Chart(document.getElementById("fin"),{
  type:"line",
  data:{labels:["Q1","Q2","Q3","Q4"],
        datasets:[{label:"Revenue",data:[120,180,160,220],borderColor:"#60a5fa",tension:.3},
                 {label:"Net Income",data:[60,30,100,80],borderColor:"#10b981",tension:.3}]},
  options:{plugins:{legend:{display:false}}}
});

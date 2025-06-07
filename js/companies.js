if(!sessionStorage.getItem("auth"))location.href="index.html";
const tbody = document.querySelector("#tbl");
const demo = [
  {name:"Alpha Corp", sector:"Industrials", rating:"AAA", prob:"98.6%"},
  {name:"Beta Industries", sector:"Consumer Goods", rating:"AA", prob:"90.1%"},
  {name:"Gamma PLC", sector:"Financials", rating:"A", prob:"78.4%"},
  {name:"Delta Ltd", sector:"Technology", rating:"BBB", prob:"65.2%"},
  {name:"Epsilon Inc", sector:"Healthcare", rating:"BBB", prob:"61.8%"}
];

demo.forEach(c=>{
  const tr=document.createElement("tr");
  tr.innerHTML=`<td><a href="company.html?c=${encodeURIComponent(c.name)}">${c.name}</a></td>
                <td>${c.sector}</td><td>${c.rating}</td><td>${c.prob}</td>`;
  tbody.appendChild(tr);
});

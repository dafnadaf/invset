const here = location.pathname.split("/").pop();
document.querySelectorAll("nav a").forEach(a=>{
  if(a.getAttribute("href")===here){a.classList.add("active")}
});

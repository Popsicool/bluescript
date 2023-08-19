const tg = document.querySelector("#tg")
tg.addEventListener("click", toggle)
const nv = document.querySelector("#nv")

function toggle(){
    if (tg.classList.contains("fa-bars")){
        nv.classList.add("navBars2")
        tg.classList.remove('fa-bars');
        tg.classList.add('fa-window-close');
    }
    else{
        nv.classList.remove("navBars2")
        tg.classList.remove('fa-window-close');
        tg.classList.add('fa-bars');
    }
}
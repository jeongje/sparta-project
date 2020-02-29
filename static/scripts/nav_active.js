const navUi = document.querySelector(".nav-pills")
const navAs = navUi.querySelectorAll(".nav-link")
const current = document.querySelectorAll(".active");


// function navClick () {
//     current[0].className = current[0].className.replace(" activate", "");
//     this.className += " active";
//     console.log('test');
// }


// for (let i = 0; i < navAs.length; i++) {    
//     navAs[i].addEventListener("click", navClick.bind())
// }


navAs[1].addEventListener("click", function() {
    current[0].className = current[0].className.replace(" activate", "");
    console.log('c')
});
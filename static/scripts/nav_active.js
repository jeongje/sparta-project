const navUi = document.querySelector(".nav-pills")
const navHref = navUi.querySelectorAll("a[href='" + location.pathname + "']")

// 그냥 active를 바꿨을 때 서버쪽에서 새로고침이 되는 문제가 있었음
// jquery의 ready기능을 이용해 모든 DOM이 다 로드된 뒤 바꾸면 문제 해결
// ready대신에 vanilla JS 이용
// https://stackoverflow.com/questions/24514717/bootstrap-navbar-active-state-not-working
// https://stackoverflow.com/questions/9899372/pure-javascript-equivalent-of-jquerys-ready-how-to-call-a-function-when-t

document.addEventListener('DOMContentLoaded', function() {
    navHref[0].className = "nav-link active"
}, false);


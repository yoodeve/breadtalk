$(document).ready(function () {
    checkCookie();
});

function checkCookie() {
    let cookieArr = document.cookie.split(";");
    try {
        for (let i = 0; i < cookieArr.length; i++) {
            let logIn = cookieArr[i].match('mytoken')

            if (logIn) { // 로그인 상태 //
                let loginBtn = document.querySelector(".btn-login");
                loginBtn.innerHTML = "LOGOUT";
                loginBtn.addEventListener("click", logOut);

                let mypgBtn = document.querySelector(".btn-mypg");
                mypgBtn.innerHTML = "MyPage";
                mypgBtn.addEventListener("click", MyPage);

            } else {
                let loginBtn = document.querySelector(".btn-rvw").style.visibility = "hidden";
                return;
            }
        }
    } catch (e) {
        console.log(e);
    }
}

function logOut() {
    document.cookie = "mytoken=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    window.location.href = "/"
}


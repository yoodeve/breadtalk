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

function listing() {
            $.ajax({
                type: 'GET',
                url: '/api/read',
                data: {},
                success: function (response) {
                    let rows = response['reviews']
                    for (let i = 0; i < rows.length; i++) {
                        let store = rows[i]['store']
                        let city = rows[i]['city']
                        let city2 = rows[i]['city2']
                        let bread_name = rows[i]['bread_name']
                        let comment = rows[i]['comment']
                        let star = rows[i]['star']
                        let file = rows[i]['file']
                        let mytime1 = rows[i]['mytime1']

                        let star_image = '⭐'.repeat(star)

                        console.log(store, city, city2, bread_name, comment, file, star_image)
                        let temp_html = ` <div class="card" style="width: 18rem;">
                                                <img src="../static/${file}" class="card-img-top" alt="...">
                                                <div class="card-body">
                                                    <h5 class="card-title">${store}</h5>
                                                    <p class="card-text">${comment}</p>
                                                </div>
                                                <ul class="list-group list-group-flush">
                                                    <li class="list-group-item">${bread_name}</li>
                                                    <li class="list-group-item">${city}${city2}</li>
                                                    <li class="list-group-item">${star_image}</li>
                                                </ul>
                                                <div class="card-body" style="display: flex; justify-content: space-around;">
                                                    <h8>작성자 : 닉네임</h8>
                                                    <h8>${mytime1}</h8>
                                                </div>
                                            </div>`
                        $('#cards-box').append(temp_html)
                    }
                }
            })
        }
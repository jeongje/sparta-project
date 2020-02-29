const tenantNameInput = document.querySelector('#tenant_name')
const testUl = document.querySelector('.test')


function namelistGet() {
    // console.log('Click')
    var request = new XMLHttpRequest();
    request.open('GET', '/tenants/name_list', true);

    request.onload = function () {
        if (this.status >= 200 && this.status < 400) {
            // Success!
            const resp = this.response;
            const obj = JSON.parse(resp) //Json이 string으로 넘어오는데 이를 변경해주려면 Json.parse를 이용
            const nameList = obj.name_list
            const li = document.createElement("li")
            // li.appendChild(resp)
            // testUl.appendChild(li)
       
            console.log(JSON.parse(resp))

            for(let i = 0 ; i < nameList.length; i++) {
                let name = nameList[i];
                console.log(name);
            }
        } else {
            // We reached our target server, but it returned an error

        }
    };

    request.onerror = function () {
        // There was a connection error of some sort
    };

    request.send();
}


function init() {
    console.log('Hello')
    tenantNameInput.addEventListener("click", namelistGet);
}

init();
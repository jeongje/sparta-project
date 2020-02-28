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
            const nameList = resp['name_list']
            const li = document.createElement("li")
            // li.appendChild(resp)
            // testUl.appendChild(li)
            // console.log(nameList)
            console.log(resp)
            console.log(resp["name_list"])            
            console.log(resp.name_list)
            // console.log(resp[0])
            // console.log(resp[1])
            // for(let i = 0 ; i < nameList.length; i++) {
            //     let name = nameList[i];
            //     console.log(name);
            // }
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
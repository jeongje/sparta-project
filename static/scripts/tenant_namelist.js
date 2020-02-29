const tenantNameSelect = document.querySelector('#tenant_name')


function namelistGet() {
    var request = new XMLHttpRequest();
    request.open('GET', '/tenants/name_list', true);
    request.onload = function () {
        if (this.status >= 200 && this.status < 400) {
            // Success!
            const resp = this.response;
            const obj = JSON.parse(resp) //Json이 string으로 넘어오는데 이를 변경해주려면 Json.parse를 이용
            const nameList = obj.name_list
            
            for(let i = 0 ; i < nameList.length; i++) {
                let option = document.createElement("option")
                let name = nameList[i];
                option.value = name;
                option.text = name;
                tenantNameSelect.appendChild(option);
            }
        } else {
            // We reached our target server, but it returned an error
            "We reached our target server, but it returned an error"

        }
    };

    request.onerror = function () {
        // There was a connection error of some sort
        "There was a connection error of some sort"
    };

    request.send();
}


function init() {
    namelistGet();
}

init();
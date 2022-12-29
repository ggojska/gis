const api_url = "/api/v1/";

function addCar() {
    if (document.getElementsByClassName("carform")[0].style.display  === 'none') {
        document.getElementsByClassName("carform")[0].style.display = '';
    }
    else
    {
        document.getElementsByClassName("carform")[0].style.display = 'none';
    }
}

function deleteCar(carId) {
    var request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 201) {
            document.getElementsByName(carId)[0].style.display = 'none';
        }
    };
    request_url = api_url + "cars/" + carId
    request.open('DELETE', request_url);
    request.send();
}
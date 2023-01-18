function addCar() {
    if (document.getElementsByClassName("carform")[0].style.display  === 'none') {
        document.getElementsByClassName("carform")[0].style.display = '';
        document.getElementById("show-car-up").style.display = '';
        document.getElementById("show-car-down").style.display = 'none';
    }
    else
    {
        document.getElementsByClassName("carform")[0].style.display = 'none';
        document.getElementById("show-car-up").style.display = 'none';
        document.getElementById("show-car-down").style.display = '';
    }
}
function addCar() {
    if (document.getElementsByClassName("carform")[0].style.display  === 'none') {
        document.getElementsByClassName("carform")[0].style.display = '';
    }
    else
    {
        document.getElementsByClassName("carform")[0].style.display = 'none';
    }
}
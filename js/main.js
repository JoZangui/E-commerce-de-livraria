let logoText = document.querySelector('#logo-text');

function changeLogo(window) {
    if (window.innerWidth < 913) {
        logoText.innerHTML = 'Di';
    } else {
        logoText.innerHTML = 'Dissertare';
    }
}

window.addEventListener('resize', function() {
    changeLogo(this);
});

window.addEventListener('load', function() {
    changeLogo(this); 
});
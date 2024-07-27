function pagina_anterior() {

    var previousUrl=document.referrer;

    if (previousUrl) {
        window.location.href = previousUrl;
    } else {
        window.history.back();
    }
}
$(document).ready(function() {
    var homepage_height = window.innerHeight
|| document.documentElement.clientHeight
|| document.body.clientHeight;
    $("#homepage").css("height", homepage_height - 56);
});
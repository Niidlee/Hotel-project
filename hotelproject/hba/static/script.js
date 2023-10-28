document.addEventListener("DOMContentLoaded", function() {
    var loginIcon = document.getElementById("loginIcon");
    var loginPopup = document.getElementById("loginPopup");

    loginIcon.addEventListener("click", function() {
        loginPopup.style.display = "block";
    });

    loginPopup.addEventListener("click", function(event) {
        if (event.target === loginPopup) {
            loginPopup.style.display = "none";
        }
    });
});
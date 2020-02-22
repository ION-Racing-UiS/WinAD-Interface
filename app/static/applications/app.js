/* global $ */
// Init function
$(document).ready(function () {
    var resizeBg = function () {
        if (window.matchMedia('(min-width: 768px)').matches) {
            var remHeight = $(window).height() - $('#headarea').height();
            //$('.heading').css("padding-top", parseInt($('.heading').css("padding-top"), 10) + remHeight);
        } else {
            //$('.heading').css("padding-top", "1em");
        }
    };
    resizeBg();
    var compBtn = document.getElementById("comp_issue");
    var messBtn = document.getElementById("message");
    var regiBtn = document.getElementById("registration");
    compBtn.addEventListener("click", function () { formSelect(compBtn.id) });
    messBtn.addEventListener("click", function () { formSelect(messBtn.id) });
    regiBtn.addEventListener("click", function () { formSelect(regiBtn.id) });
    $(window).resize(function () { resizeBg(); });
});

// Easter egg
var ion_keys = [73, 79, 78];
var ion_index = 0;
$(document).keydown(function (e) {
    //console.log(e.keyCode);
    if (e.keyCode === ion_keys[ion_index++]) {
        if (ion_index === ion_keys.length) {
            $('#headarea').css('background-image', 'linear-gradient(rgba(0, 0, 0, 0), rgba(0, 0, 0, 1)), url(/static/images/ION_CODE.png)');
        }
    } else {
        ion_index = 0;
    }
})

// Handles form buttons and returns the form with an AJAX request
function formSelect(e) {
    $.ajax({
        url: "/contact/" + e,
        type: "POST",
        success: function (resp) {
            $("#ajaxNode").empty();
            $("#ajaxNode").append(resp);
        }
    });
}

// Sets the username for a new users
function setUsername() {
    let fname = document.getElementById("fname").value;
    let lname = document.getElementById("lname").value;
    let username = fname.toLowerCase().replace(" ", ".") + "." + lname.toLowerCase().replace(" ", "."); // Creates the username
    let fullname = fname + " " + lname; // Creates the full name of the user
    document.getElementById("fname").value = fname[0].toUpperCase() + fname.substring(1, fname.length); // Capitalization check
    document.getElementById("lname").value = lname[0].toUpperCase() + lname.substring(1, lname.length); // Capitalization check
    document.getElementById("username").value = username;
    document.getElementById("fullname").value = fullname;
}
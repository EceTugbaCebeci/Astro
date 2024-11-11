// Script to show/hide back to top button
var backToTopBtn = document.getElementById("backToTopBtn");

window.onscroll = function () {
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        backToTopBtn.style.display = "block";
    } else {
        backToTopBtn.style.display = "none";
    }
};

// Scroll to top when the button is clicked
backToTopBtn.onclick = function () {
    document.body.scrollTop = 0; // For Safari
    document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE, and Opera
};




// ScrollReveal.js code
document.addEventListener('DOMContentLoaded', function () {
    ScrollReveal().reveal('.scroll-reveal', {
        delay: 200,
        distance: '30px',
        origin: 'bottom',
        opacity: 0,
        duration: 800,
        easing: 'ease-in-out',
        reset: false,
    });
});



var swiper = new Swiper(".mySwiper", {
    navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
    },
});
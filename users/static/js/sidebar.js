document.addEventListener("DOMContentLoaded", function () {
    const toggleBtn = document.getElementById("menu-toggle");
    const wrapper = document.getElementById("wrapper");

    toggleBtn.addEventListener("click", function () {
        wrapper.classList.toggle("toggled");
    });
});

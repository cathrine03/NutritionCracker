document.addEventListener("DOMContentLoaded", () => {
    const toggleBtn = document.getElementById("theme-toggle");
    const htmlEl = document.documentElement;

    // Load from local storage
    const savedTheme = localStorage.getItem("theme");
    if (savedTheme) {
        htmlEl.setAttribute("data-theme", savedTheme);
    }

    toggleBtn.addEventListener("click", () => {
        const currentTheme = htmlEl.getAttribute("data-theme");
        const newTheme = currentTheme === "dark" ? "light" : "dark";
        htmlEl.setAttribute("data-theme", newTheme);
        localStorage.setItem("theme", newTheme);
    });
});

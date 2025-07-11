document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.getElementById("student-search");
    const roleFilter = document.getElementById("role-filter");
    const rows = document.querySelectorAll("#student-table tbody tr");

    function filterTable() {
        const search = searchInput.value.toLowerCase();
        const role = roleFilter.value.toLowerCase();

        rows.forEach(row => {
            const username = row.querySelector(".username").textContent.toLowerCase();
            // const fullname = row.querySelector(".full_name").textContent.toLowerCase();
            // const email = row.querySelector(".email").textContent.toLowerCase();
            const userRole = row.querySelector(".role").textContent.toLowerCase();

            const matchesSearch = username.includes(search);
            const matchesRole = !role || userRole === role;

            row.style.display = matchesSearch && matchesRole ? "" : "none";
        });
    }
});
    
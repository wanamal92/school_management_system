document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.getElementById("audit-search");
    const actionFilter = document.getElementById("action-filter");
    const rows = document.querySelectorAll("#audit-table tbody tr");

    function filterTable() {
        const search = searchInput.value.toLowerCase();
        const action = actionFilter.value.toLowerCase();

        rows.forEach(row => {
            const by = row.querySelector(".by").textContent.toLowerCase();
            const target = row.querySelector(".target").textContent.toLowerCase();
            const rowAction = row.querySelector(".action").textContent.toLowerCase();

            const matchesSearch = by.includes(search) || target.includes(search);
            const matchesAction = !action || rowAction === action;

            row.style.display = matchesSearch && matchesAction ? "" : "none";
        });
    }

    searchInput.addEventListener("input", filterTable);
    actionFilter.addEventListener("change", filterTable);
});

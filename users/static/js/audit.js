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

                // Check if search term matches performed by or target username
                const matchesSearch = by.includes(search) || target.includes(search);
                // Check if action filter matches the action text in the row
                const matchesAction = !action || rowAction.includes(action);

                row.style.display = matchesSearch && matchesAction ? "" : "none";
            });
        }

        searchInput.addEventListener("input", filterTable);
        actionFilter.addEventListener("change", filterTable);
    });
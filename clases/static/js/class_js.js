document.addEventListener("DOMContentLoaded", () => {
        const searchInput = document.getElementById("class-search");
        const rows = document.querySelectorAll("#class-table tbody tr");

        function filterTable() {
            const search = searchInput.value.toLowerCase();

            rows.forEach(row => {
                const class_name = row.querySelector(".class_name").textContent.toLowerCase();
                const class_code = row.querySelector(".class_code").textContent.toLowerCase();
                const section = row.querySelector(".section").textContent.toLowerCase();
                const class_in_charge = row.querySelector(".class_in_charge").textContent.toLowerCase();

                // Check if the search term matches class name, class code, or section
                const matchesSearch = class_name.includes(search) || class_code.includes(search) || section.includes(search);



                // Toggle row visibility based on filter conditions
                row.style.display = matchesSearch ? "" : "none";
            });
        }

        // Trigger filter on search or role change
        searchInput.addEventListener("input", filterTable);
    });
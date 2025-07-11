document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.getElementById("user-search");
    const roleFilter = document.getElementById("role-filter");
    const rows = document.querySelectorAll("#user-table tbody tr");

    function filterTable() {
        const search = searchInput.value.toLowerCase();
        const role = roleFilter.value.toLowerCase();

        rows.forEach(row => {
            const username = row.querySelector(".username").textContent.toLowerCase();
            const fullname = row.querySelector(".full_name").textContent.toLowerCase();
            const email = row.querySelector(".email").textContent.toLowerCase();
            const userRole = row.querySelector(".role").textContent.toLowerCase();

            const matchesSearch = username.includes(search) || email.includes(search) || fullname.includes(search);
            const matchesRole = !role || userRole === role;

            row.style.display = matchesSearch && matchesRole ? "" : "none";
        });
    }
    
    

    searchInput.addEventListener("input", filterTable);
    roleFilter.addEventListener("change", filterTable);

    // CSV Export
    document.getElementById("export-csv").addEventListener("click", () => {
        const visibleRows = Array.from(rows).filter(row => row.style.display !== "none");
        let csvContent = "Username,Email,Role\n";

        visibleRows.forEach(row => {
            const username = row.querySelector(".username").textContent;
            const email = row.querySelector(".email").textContent;
            const role = row.querySelector(".role").textContent;
            csvContent += `${username},${email},${role}\n`;
        });

        const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "user_list.csv";
        a.click();
    });

    // PDF Export
    document.getElementById("export-pdf").addEventListener("click", () => {
        const visibleRows = Array.from(rows).filter(row => row.style.display !== "none");
        const win = window.open('', '', 'width=900,height=700');
        win.document.write('<html><head><title>User List</title>');
        win.document.write('<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">');
        win.document.write('</head><body><h3 class="text-center my-3">User List</h3><table class="table table-bordered"><thead><tr><th>Username</th><th>Email</th><th>Role</th></tr></thead><tbody>');

        visibleRows.forEach(row => {
            const username = row.querySelector(".username").textContent;
            const email = row.querySelector(".email").textContent;
            const role = row.querySelector(".role").textContent;
            win.document.write(`<tr><td>${username}</td><td>${email}</td><td>${role}</td></tr>`);
        });

        win.document.write('</tbody></table></body></html>');
        win.document.close();
        win.print();
    });
});

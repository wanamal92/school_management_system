

document.addEventListener('DOMContentLoaded', function () {
    const modal = document.getElementById('confirmModal');
    const userNameElement = document.getElementById('userName');
    const deleteForm = document.getElementById('deleteForm');
    const confirmBtn = document.querySelector('.confirm-btn');
    const cancelBtn = document.querySelector('.cancel-btn');
    const closeBtn = document.querySelector('.close-btn');

    // Show modal
    function showModal() {
        modal.style.display = 'flex';
        document.body.style.overflow = 'hidden';
    }

    // Hide modal
    function hideModal() {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
    }

    // Handle delete button clicks
    document.querySelectorAll('.delete-btn').forEach(button => {
        button.addEventListener('click', function () {
            const userId = this.getAttribute('data-user-id');
            const userName = this.getAttribute('data-user-name');

            // Update modal content
            userNameElement.textContent = userName;

            // Update form action
            deleteForm.action = "{% url 'delete_user' 0 %}".replace('0', userId);

            // Show modal
            showModal();
        });
    });

    // Handle confirm delete
    confirmBtn.addEventListener('click', function () {
        deleteForm.submit();
    });

    // Handle cancel/close
    cancelBtn.addEventListener('click', hideModal);
    closeBtn.addEventListener('click', hideModal);

    // Close when clicking outside modal
    modal.addEventListener('click', function (e) {
        if (e.target === modal) {
            hideModal();
        }
    });

    // Close with Escape key
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && modal.style.display === 'flex') {
            hideModal();
        }
    });
});

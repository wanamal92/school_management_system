document.addEventListener('DOMContentLoaded', function () {
    const modal = document.getElementById('confirmModal');
    const userNameElement = document.getElementById('confirm-message');  // This is where the message will appear
    const deleteForm = document.getElementById('deleteForm'); // Assuming you have a hidden form for deletion
    const confirmBtn = document.querySelector('.confirm-btn');
    const cancelBtn = document.querySelector('.cancel-btn');
    const closeBtn = document.querySelector('.close-btn');

    // Show modal
    function showModal(message, deleteUrl) {
        userNameElement.textContent = message;  // Set the dynamic message in the modal
        deleteForm.action = deleteUrl; // Set the form action dynamically
        modal.style.display = 'flex'; // Show modal
        document.body.style.overflow = 'hidden'; // Disable body scroll
    }

    // Hide modal
    function hideModal() {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto'; // Enable body scroll
    }

    // Handle delete button clicks
    document.querySelectorAll('.delete-btn').forEach(button => {
        button.addEventListener('click', function () {
            const itemId = this.getAttribute('data-item-id'); // Get the item ID dynamically
            const itemName = this.getAttribute('data-item-name'); // Get the item name dynamically
            const deleteUrl = this.getAttribute('data-delete-url'); // Get the dynamic delete URL

            // Update the modal with the dynamic message
            const message = `Are you sure you want to delete "${itemName}"?`;  // Add the item name to the message

            // Show the modal with the appropriate message and URL
            showModal(message, deleteUrl);
        });
    });

    // Handle confirm delete (Submit the form to delete)
    confirmBtn.addEventListener('click', function () {
        deleteForm.submit(); // Submit the form to delete the item
    });

    // Handle cancel/close
    cancelBtn.addEventListener('click', hideModal);
    closeBtn.addEventListener('click', hideModal);

    // Close modal when clicking outside
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

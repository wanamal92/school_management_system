    document.addEventListener('DOMContentLoaded', function() {
        const prefectTypeSelect = document.querySelector('[name="prefect_type"]');
        const classLevelContainer = document.getElementById('class-level-container');
        const classLevelField = document.querySelector('[name="class_level"]');

        // Function to toggle visibility based on prefect type
        function toggleClassLevelField() {
            // Check if "Class Monitor" is selected and toggle class level field visibility
            if (prefectTypeSelect.value === 'Class Monitor') {
                classLevelContainer.style.display = 'block';
                classLevelField.required = true;
            } else {
                classLevelContainer.style.display = 'none';
                classLevelField.required = false;
                classLevelField.value = ''; // Clear the value when hidden
            }
        }

        // Trigger on page load and when prefect type changes
        toggleClassLevelField();
        prefectTypeSelect.addEventListener('change', toggleClassLevelField);
    });
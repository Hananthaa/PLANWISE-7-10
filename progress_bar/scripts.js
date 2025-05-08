const checkboxes = document.querySelectorAll('.task-checkbox');
const progressFill = document.getElementById('progressFill');
const progressText = document.getElementById('progressText');
const totalCheckboxes = checkboxes.length;

checkboxes.forEach(checkbox => {
    checkbox.addEventListener('change', updateProgressBar);
});

function updateProgressBar() {
    console.log ("Bar updated...")
    const checkedCount = document.querySelectorAll('.task-checkbox:checked').length;
    const progressPercentage = (checkedCount / totalCheckboxes) * 100;

    progressFill.style.width = progressPercentage + '%';
    progressText.textContent = Math.round(progressPercentage) + '%';
}
// Tab switching
function openTab(tabName) {
  const tabs = document.querySelectorAll('.tab-content');
  tabs.forEach(tab => tab.style.display = 'none');
  document.getElementById(tabName).style.display = 'block';
}

// Form validation
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', (e) => {
      let isValid = true;
      form.querySelectorAll('[required]').forEach(input => {
        if (!input.value.trim()) {
          input.style.borderColor = '#e63946';
          isValid = false;
        } else {
          input.style.borderColor = '#ddd';
        }
      });
      if (!isValid) {
        e.preventDefault();
        alert('Please fill all required fields!');
      }
    });
  });
});

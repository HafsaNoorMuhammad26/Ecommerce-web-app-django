// Auto-hide alerts after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(function() {
        let alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            let bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
});

// Quantity input validation
document.querySelectorAll('input[type="number"]').forEach(function(input) {
    input.addEventListener('change', function() {
        let min = parseInt(this.getAttribute('min'));
        let max = parseInt(this.getAttribute('max'));
        let value = parseInt(this.value);
        
        if (isNaN(value)) {
            this.value = min || 1;
        } else if (value < min) {
            this.value = min;
        } else if (value > max) {
            this.value = max;
        }
    });
});

// Add loading state to form submit buttons - FIXED to prevent infinite loading
document.querySelectorAll('form button[type="submit"]').forEach(function(button) {
    button.addEventListener('click', function(e) {
        // Only show loading if form is valid
        if (this.form && this.form.checkValidity()) {
            // Don't change button text, just let it submit normally
            // This prevents the "Loading..." stuck issue
            return true;
        }
    });
});
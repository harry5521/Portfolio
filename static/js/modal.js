// ==================== MODAL FUNCTIONALITY ====================

function openModal(id) {
    const modal = document.getElementById(`modal-${id}`);
    if (modal) {
        modal.classList.remove('hidden');
        document.body.style.overflow = 'hidden';
        
        // Close on overlay click
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                closeModal(id);
            }
        }, { once: true });
        
        // Close on escape key
        document.addEventListener('keydown', function handler(e) {
            if (e.key === 'Escape') {
                closeModal(id);
                document.removeEventListener('keydown', handler);
            }
        });
    }
}

function closeModal(id) {
    const modal = document.getElementById(`modal-${id}`);
    if (modal) {
        modal.classList.add('hidden');
        document.body.style.overflow = '';
    }
}

// Close all modals on page load (safety)
document.addEventListener('DOMContentLoaded', function() {
    const modals = document.querySelectorAll('[id^="modal-"]');
    modals.forEach(modal => {
        modal.classList.add('hidden');
    });
});
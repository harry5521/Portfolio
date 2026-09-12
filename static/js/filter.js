// ==================== PROJECT FILTER BY TECHNOLOGY ====================

document.addEventListener('DOMContentLoaded', function() {
    const filterBtns = document.querySelectorAll('.filter-btn');
    const projectCards = document.querySelectorAll('.project-card');
    
    if (filterBtns.length > 0 && projectCards.length > 0) {
        filterBtns.forEach(btn => {
            btn.addEventListener('click', function() {
                // Update active button
                filterBtns.forEach(b => b.classList.remove('active'));
                this.classList.add('active');
                
                const filterValue = this.getAttribute('data-filter');
                
                // Filter projects
                projectCards.forEach(card => {
                    const techs = card.getAttribute('data-techs').toLowerCase();
                    
                    if (filterValue === 'all' || techs.includes(filterValue.toLowerCase())) {
                        card.classList.remove('hidden-card');
                        card.style.animation = 'fadeInUp 0.5s ease-out forwards';
                    } else {
                        card.classList.add('hidden-card');
                    }
                });
            });
        });
    }
});
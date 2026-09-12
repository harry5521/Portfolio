// ==================== SCROLL TO TOP BUTTON ====================

document.addEventListener('DOMContentLoaded', function() {
    const scrollTopBtn = document.getElementById('scrollTopBtn');
    
    if (scrollTopBtn) {
        // Show/hide button based on scroll position
        window.addEventListener('scroll', function() {
            if (window.scrollY > 300) {
                scrollTopBtn.classList.remove('hidden');
            } else {
                scrollTopBtn.classList.add('hidden');
            }
        });
        
        // Scroll to top on click
        scrollTopBtn.addEventListener('click', function() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
});

// ==================== TOAST NOTIFICATION ====================

function showToast(message, type = 'success') {
    // Remove existing toasts
    const existingToasts = document.querySelectorAll('.toast');
    existingToasts.forEach(toast => toast.remove());
    
    // Create toast element
    const toast = document.createElement('div');
    toast.className = `toast show`;
    
    const bgColor = type === 'success' ? 'bg-green-600' : 
                    type === 'error' ? 'bg-red-600' : 'bg-blue-600';
    
    toast.innerHTML = `
        <div class="${bgColor} text-white px-6 py-4 rounded-lg shadow-2xl flex items-center justify-between min-w-[300px] max-w-md">
            <span class="flex items-center">
                <i class="fas ${type === 'success' ? 'fa-check-circle' : type === 'error' ? 'fa-exclamation-circle' : 'fa-info-circle'} mr-3"></i>
                ${message}
            </span>
            <button onclick="this.closest('.toast').remove()" class="ml-4 text-white hover:text-slate-200 text-xl">&times;</button>
        </div>
    `;
    
    document.body.appendChild(toast);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        toast.classList.remove('show');
        toast.classList.add('hide');
        setTimeout(() => toast.remove(), 500);
    }, 5000);
}

// ==================== SCROLL ANIMATIONS ====================

document.addEventListener('DOMContentLoaded', function() {
    // Animate elements when they come into view
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade-in-up');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Observe elements with data-animate attribute
    const animateElements = document.querySelectorAll('[data-animate]');
    animateElements.forEach(el => observer.observe(el));
});

// ==================== SKILL CHART ANIMATION ====================

document.addEventListener('DOMContentLoaded', function() {
    const skillSection = document.getElementById('skills-section');
    
    if (skillSection) {
        const skillObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const paths = entry.target.querySelectorAll('.progress-path');
                    paths.forEach(path => {
                        const percent = path.getAttribute('data-percent');
                        setTimeout(() => {
                            path.setAttribute('stroke-dasharray', `${percent}, 100`);
                        }, 200);
                    });
                    skillObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.3 });
        
        skillObserver.observe(skillSection);
    }
});

// ==================== ACTIVE NAV LINK HIGHLIGHT ====================

document.addEventListener('DOMContentLoaded', function() {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link');
    
    window.addEventListener('scroll', () => {
        let current = '';
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop - 100;
            const sectionHeight = section.clientHeight;
            
            if (window.scrollY >= sectionTop && window.scrollY < sectionTop + sectionHeight) {
                current = section.getAttribute('id');
            }
        });
        
        navLinks.forEach(link => {
            link.classList.remove('text-teal-400');
            link.classList.add('text-slate-400');
            
            if (link.getAttribute('href') === `#${current}`) {
                link.classList.remove('text-slate-400');
                link.classList.add('text-teal-400');
            }
        });
    });
});
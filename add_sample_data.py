"""
Sample Data Generator for Portfolio
Run: python manage.py shell < add_sample_data.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio.settings')
django.setup()

from django.utils.text import slugify
from django.core.files.base import ContentFile
from django.utils import timezone
from datetime import date, timedelta
from landing.models import (
    Profile, Technology, Skill, Experience, 
    ExperienceProject, Certification, Project
)

print("=" * 60)
print("🚀 Starting Sample Data Generation...")
print("=" * 60)

# ==================== 1. PROFILE ====================
print("\n📝 Creating Profile...")
profile, created = Profile.objects.get_or_create(
    email="hurairagulfaraz4@gmail.com",
    defaults={
        'phone1': "+92 315 0101057",
        'phone2': "+92 320 2256255",
        'github_url': "https://github.com/harry5521",
        'linkedin_url': "https://www.linkedin.com/in/abu-huraira-gulfaraz-95266b269",
    }
)

if created:
    print("✅ Profile created (add images via admin)")
else:
    print("ℹ️ Profile already exists")

# ==================== 2. TECHNOLOGIES ====================
print("\n🛠️ Creating Technologies...")
tech_data = [
    "Python", "Django", "Django REST Framework", "PostgreSQL",
    "MySQL", "Redis", "Docker", "Git", "Linux", "Nginx",
    "JavaScript", "React", "HTML", "CSS", "Tailwind CSS", "Flask",
    "Stripe", "FastAPI", "Kubernetes" 
]

for tech_name in tech_data:
    tech, created = Technology.objects.get_or_create(
        name=tech_name,
        defaults={'slug': slugify(tech_name)}
    )
    if created:
        print(f"  ✓ {tech_name}")

# Get all technologies for easy reference
tech_dict = {t.name: t for t in Technology.objects.all()}

# ==================== 3. SKILLS ====================
print("\n📊 Creating Skills...")
skills_data = [
    ("Python", 95, 1),
    ("Django", 90, 2),
    ("Django REST Framework", 85, 3),
    ("PostgreSQL", 80, 4),
    ("MySQL", 85, 5),
    ("Redis", 75, 6),
    ("Docker", 70, 7),
    ("Git", 90, 8),
    ("JavaScript", 60, 9),
    ("Linux", 75, 10),
    ("React", 50, 11),
    ("REST APIs", 92, 12),
]

for skill_name, percentage, order in skills_data:
    skill, created = Skill.objects.get_or_create(
        skill_name=skill_name,
        defaults={'percentage': percentage, 'order': order}
    )
    if created:
        print(f"  ✓ {skill_name} - {percentage}%")

# ==================== 4. EXPERIENCES ====================
print("\n💼 Creating Experiences...")

# Experience 1: Current Company
exp1, created = Experience.objects.get_or_create(
    company_name="TechCorp Pvt Ltd",
    position="Backend Developer",
    defaults={
        'start_date': date(2024, 1, 15),
        'end_date': None,
        'is_current': True,
        'description': """Led backend development for multiple client projects. Designed and implemented scalable REST APIs, optimized database queries resulting in 60% performance improvement. Mentored junior developers and established coding standards.""",
        'order': 1,
    }
)

if created:
    exp1.technologies_used.set([
        tech_dict['Python'],
        tech_dict['Django'],
        tech_dict['PostgreSQL'],
        tech_dict['Redis'],
        tech_dict['Docker'],
    ])
    print("  ✓ TechCorp Pvt Ltd - Backend Developer (Current)")
else:
    print("  ℹ️ TechCorp Pvt Ltd already exists")

# Projects for Experience 1
if created or exp1.projects.count() == 0:
    project1 = ExperienceProject.objects.create(
        experience=exp1,
        title="E-commerce REST API",
        description="""• Built comprehensive REST API handling 100K+ products\n• Implemented JWT authentication and role-based access control\n• Integrated Redis caching reducing response time by 50%\n• Designed microservices architecture using Docker""",
        order=1,
    )
    project1.technologies.set([
        tech_dict['Django'],
        tech_dict['Django REST Framework'],
        tech_dict['PostgreSQL'],
        tech_dict['Redis'],
    ])
    print("    - E-commerce REST API (added)")
    
    project2 = ExperienceProject.objects.create(
        experience=exp1,
        title="Payment Gateway Integration",
        description="""• Integrated Stripe and PayPal payment systems\n• Implemented webhook handling for payment notifications\n• Reduced payment failures by 40% through retry logic\n• Ensured PCI DSS compliance""",
        order=2,
    )
    project2.technologies.set([
        tech_dict['Python'],
        tech_dict['Stripe'],  # Will need to add this
        tech_dict['Django'],
    ])
    print("    - Payment Gateway Integration (added)")
    
    project3 = ExperienceProject.objects.create(
        experience=exp1,
        title="Admin Dashboard API",
        description="""• Developed APIs for admin panel with CRUD operations\n• Implemented advanced filtering, sorting, and pagination\n• Built real-time notifications using Django Channels\n• Optimized queries reducing load time by 70%""",
        order=3,
    )
    project3.technologies.set([
        tech_dict['Django'],
        tech_dict['Django REST Framework'],
        tech_dict['PostgreSQL'],
        tech_dict['Redis'],
        tech_dict['Docker'],
    ])
    print("    - Admin Dashboard API (added)")

# Experience 2: Previous Company
exp2, created = Experience.objects.get_or_create(
    company_name="StartupXYZ",
    position="Junior Python Developer",
    defaults={
        'start_date': date(2023, 6, 1),
        'end_date': date(2023, 12, 15),
        'is_current': False,
        'description': """Developed and maintained backend services for SaaS platform. Implemented new features, fixed bugs, and optimized existing code. Collaborated with frontend team on API integration.""",
        'order': 2,
    }
)

if created:
    exp2.technologies_used.set([
        tech_dict['Python'],
        tech_dict['Django'],
        tech_dict['MySQL'],
        tech_dict['JavaScript'],
    ])
    print("  ✓ StartupXYZ - Junior Python Developer (Jun 2023 - Dec 2023)")
else:
    print("  ℹ️ StartupXYZ already exists")

# Projects for Experience 2
if created or exp2.projects.count() == 0:
    project4 = ExperienceProject.objects.create(
        experience=exp2,
        title="Task Management System",
        description="""• Developed task management APIs with user authentication\n• Implemented file upload functionality for task attachments\n• Built notification system for task deadlines\n• Integrated with frontend React application""",
        order=1,
    )
    project4.technologies.set([
        tech_dict['Django'],
        tech_dict['Django REST Framework'],
        tech_dict['MySQL'],
        tech_dict['JavaScript'],
    ])
    print("    - Task Management System (added)")

# Experience 3: Freelance
exp3, created = Experience.objects.get_or_create(
    company_name="Freelance Projects",
    position="Full Stack Developer",
    defaults={
        'start_date': date(2023, 1, 1),
        'end_date': date(2023, 5, 31),
        'is_current': False,
        'description': """Completed multiple freelance projects for international clients. Developed web applications, APIs, and automation scripts. Managed project timelines and client communications.""",
        'order': 3,
    }
)

if created:
    exp3.technologies_used.set([
        tech_dict['Python'],
        tech_dict['Flask'],
        tech_dict['JavaScript'],
        tech_dict['HTML'],
        tech_dict['CSS'],
    ])
    print("  ✓ Freelance Projects - Full Stack Developer (Jan 2023 - May 2023)")
else:
    print("  ℹ️ Freelance Projects already exists")

# Projects for Experience 3
if created or exp3.projects.count() == 0:
    project5 = ExperienceProject.objects.create(
        experience=exp3,
        title="Blog Platform",
        description="""• Developed full-stack blog application using Flask\n• Implemented user authentication and role-based access\n• Built comment system with moderation\n• Deployed on VPS using Nginx and Gunicorn""",
        order=1,
    )
    project5.technologies.set([
        tech_dict['Python'],
        tech_dict['Flask'],
        tech_dict['HTML'],
        tech_dict['CSS'],
        tech_dict['JavaScript'],
        tech_dict['Nginx'],
    ])
    print("    - Blog Platform (added)")

# ==================== 5. CERTIFICATIONS ====================
print("\n📜 Creating Certifications...")

cert1, created = Certification.objects.get_or_create(
    name="Google AI Essentials",
    defaults={
        'issuing_organization': "Coursera.org",
        'credential_url': "https://coursera.org/verify/ZN56PR75X1XW",
        'issue_date': date(2024, 3, 15),
        'description': "Learned fundamentals of AI, machine learning, and responsible AI practices.",
        'order': 1,
    }
)
if created:
    print("  ✓ Google AI Essentials")

cert2, created = Certification.objects.get_or_create(
    name="Python for Data Science",
    defaults={
        'issuing_organization': "Coursera.org",
        'issue_date': date(2023, 8, 20),
        'description': "Comprehensive course covering Python libraries for data analysis and visualization.",
        'order': 2,
    }
)
if created:
    print("  ✓ Python for Data Science")

cert3, created = Certification.objects.get_or_create(
    name="Django Web Framework",
    defaults={
        'issuing_organization': "Udemy",
        'issue_date': date(2023, 4, 10),
        'description': "In-depth course on Django fundamentals, advanced topics, and best practices.",
        'order': 3,
    }
)
if created:
    print("  ✓ Django Web Framework")

# ==================== 6. PROJECTS ====================
print("\n🚀 Creating Projects...")

projects_data = [
    {
        'title': 'E-commerce REST API',
        'slug': 'ecommerce-rest-api',
        'short': 'Scalable REST API for e-commerce platform with 100K+ products',
        'detailed': """A comprehensive REST API for e-commerce platform built with Django and DRF.

## Features:
- Product management with categories and filters
- User authentication and authorization
- Shopping cart and checkout
- Order management
- Payment integration (Stripe, PayPal)
- Inventory management
- Admin dashboard APIs
- Rate limiting and caching
- API documentation with Swagger

## Tech Stack:
- Backend: Django, DRF, PostgreSQL
- Caching: Redis
- Authentication: JWT
- Deployment: Docker, Nginx

## Performance:
- 60% faster query responses
- Handles 1000+ concurrent requests
- 99.9% uptime achieved

## Code Quality:
- Follows PEP 8 standards
- 90% test coverage
- Type hints throughout
- Comprehensive documentation""",
        'github_link': 'https://github.com/harry5521/ecommerce-api',
        'live_link': 'https://ecommerce-api-demo.vercel.app',
        'tech_stack': ['Python', 'Django', 'Django REST Framework', 'PostgreSQL', 'Redis', 'Docker'],
        'is_featured': True,
        'order': 1,
    },
    {
        'title': 'Blog Platform API',
        'slug': 'blog-platform-api',
        'short': 'Full-stack blog platform with user authentication and real-time comments',
        'detailed': """A modern blog platform API with advanced features.

## Features:
- Blog post CRUD operations
- Rich text editor support
- User profiles and authentication
- Comment system with moderation
- Like and bookmark posts
- Tag-based categorization
- Search functionality
- Email notifications
- Real-time updates using WebSockets

## Tech Stack:
- Backend: Django, DRF
- Database: PostgreSQL
- Caching: Redis
- Real-time: Django Channels
- Frontend: React

## Highlights:
- WebSocket-based real-time comments
- Advanced search with full-text search
- Email digest system
- SEO-friendly URLs""",
        'github_link': 'https://github.com/harry5521/blog-api',
        'tech_stack': ['Python', 'Django', 'Django REST Framework', 'PostgreSQL', 'Redis', 'JavaScript', 'React'],
        'is_featured': True,
        'order': 2,
    },
    {
        'title': 'Task Management System',
        'slug': 'task-management-system',
        'short': 'Collaborative task management app with team features',
        'detailed': """A task management application for teams.

## Features:
- Task creation and assignment
- Due dates and reminders
- Priority levels
- Team member collaboration
- File attachments
- Activity logging
- Kanban board view
- Dashboard with analytics
- Export to PDF/Excel

## Tech Stack:
- Backend: Django, DRF
- Database: MySQL
- Frontend: JavaScript, HTML, CSS
- Deployment: VPS, Nginx, Gunicorn

## Team Features:
- Role-based access control
- Team management
- Project organization
- Progress tracking
- Notification system""",
        'github_link': 'https://github.com/harry5521/task-mgmt',
        'tech_stack': ['Python', 'Django', 'Django REST Framework', 'MySQL', 'JavaScript'],
        'is_featured': True,
        'order': 3,
    },
    {
        'title': 'Authentication Microservice',
        'slug': 'auth-microservice',
        'short': 'Dedicated auth service with JWT and OAuth2 support',
        'detailed': """A microservice for handling authentication across multiple applications.

## Features:
- JWT token generation and validation
- OAuth2 integration (Google, GitHub)
- Refresh token rotation
- Password reset flow
- Email verification
- 2FA support
- Rate limiting
- User management API
- Audit logging

## Tech Stack:
- Backend: Python, FastAPI
- Database: PostgreSQL
- Auth: OAuth2, JWT
- Deployment: Docker, Kubernetes

## Security:
- OWASP compliance
- Secure token storage
- Encrypted passwords
- CSRF protection
- Input validation""",
        'github_link': 'https://github.com/harry5521/auth-service',
        'tech_stack': ['Python', 'FastAPI', 'PostgreSQL', 'Docker', 'Kubernetes'],
        'is_featured': True,
        'order': 4,
    },
    {
        'title': 'Real-time Chat Application',
        'slug': 'realtime-chat-app',
        'short': 'WebSocket-based chat with rooms and direct messaging',
        'detailed': """A real-time chat application.

## Features:
- Multiple chat rooms
- Direct messaging
- Online status indicators
- Typing indicators
- Read receipts
- Message search
- File sharing
- Voice messages
- Emoji reactions

## Tech Stack:
- Backend: Django, Django Channels
- Database: PostgreSQL, Redis
- Frontend: JavaScript, WebSocket
- Deployment: Docker, Nginx

## Performance:
- Handles 5000+ concurrent users
- Sub-100ms message delivery
- Auto-scaling enabled""",
        'github_link': 'https://github.com/harry5521/chat-app',
        'live_link': 'https://chat-demo.vercel.app',
        'tech_stack': ['Python', 'Django', 'Django Channels', 'PostgreSQL', 'Redis', 'JavaScript'],
        'is_featured': False,
        'order': 5,
    },
    {
        'title': 'API Rate Limiter',
        'slug': 'api-rate-limiter',
        'short': 'Redis-based rate limiting middleware for Django',
        'detailed': """A flexible rate limiting solution.

## Features:
- Configurable rate limits
- Multiple strategies (sliding window, token bucket)
- Whitelist/blacklist support
- Per-IP and per-user limits
- Customizable error responses
- Dashboard for monitoring
- Export logs to CSV
- Analytics and statistics

## Tech Stack:
- Backend: Python, Django
- Storage: Redis
- Monitoring: Custom dashboard
- Deployment: Docker

## Use Cases:
- API protection
- DDoS prevention
- Fair usage policies
- Subscription-based access""",
        'github_link': 'https://github.com/harry5521/rate-limiter',
        'tech_stack': ['Python', 'Django', 'Redis', 'Docker'],
        'is_featured': False,
        'order': 6,
    },
]

for proj_data in projects_data:
    project, created = Project.objects.get_or_create(
        slug=proj_data['slug'],
        defaults={
            'title': proj_data['title'],
            'short_description': proj_data['short'],
            'detailed_description': proj_data['detailed'],
            'github_link': proj_data.get('github_link'),
            'live_link': proj_data.get('live_link'),
            'is_featured': proj_data['is_featured'],
            'order': proj_data['order'],
        }
    )
    
    if created:
        # Set tech stack
        tech_list = [tech_dict[tech] for tech in proj_data['tech_stack'] if tech in tech_dict]
        project.tech_stack.set(tech_list)
        print(f"  ✓ {proj_data['title']} (Featured: {proj_data['is_featured']})")
    else:
        print(f"  ℹ️ {proj_data['title']} already exists")

print("\n" + "=" * 60)
print("✅ Sample Data Generation Complete!")
print("=" * 60)
print(f"\n📊 Summary:")
print(f"  • Profile: {Profile.objects.count()}")
print(f"  • Technologies: {Technology.objects.count()}")
print(f"  • Skills: {Skill.objects.count()}")
print(f"  • Experiences: {Experience.objects.count()}")
print(f"  • Experience Projects: {ExperienceProject.objects.count()}")
print(f"  • Certifications: {Certification.objects.count()}")
print(f"  • Projects: {Project.objects.count()}")
print(f"\n⚠️  Note: Add images via admin panel at:")
print(f"   → http://127.0.0.1:8000/admin/")
print("\n" + "=" * 60)
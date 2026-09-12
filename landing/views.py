from django.views.generic import FormView, TemplateView
from .models import Profile, Contact, Project, Skill, Experience, Certification, Technology, Education
from .forms import ContactForm
from django.contrib import messages
from django.core.mail import send_mail
from django.urls import reverse_lazy
import threading
import logging


logger = logging.getLogger(__name__)


class ContactEmailThread(threading.Thread):
    """Send one email in the background so the contact request is not blocked."""
    def __init__(self, *, subject, message, from_email, recipient_list):
        super().__init__(daemon=True)
        self.subject = subject
        self.message = message
        self.from_email = from_email
        self.recipient_list = recipient_list

    def run(self):
        try:
            send_mail(
                subject=self.subject,
                message=self.message,
                from_email=self.from_email,
                recipient_list=self.recipient_list,
                fail_silently=False,
            )
        except Exception:
            logger.exception(
                "Failed to send contact email: subject=%r recipients=%r",
                self.subject,
                self.recipient_list,
            )


class LandingView(FormView):
    """
    Main landing page - Single page portfolio.
    """
    template_name = 'landing.html'
    form_class = ContactForm
    success_url = reverse_lazy('landing:home')

    def form_valid(self, form):
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        subject = form.cleaned_data.get('subject') or 'Portfolio Contact'
        message = form.cleaned_data['message']

        # Save message in DB first.
        Contact.objects.create(
            name=name,
            email=email,
            message=message,
        )

        # Get profile email for development.
        # Deployment will move this credential/configuration to .env.
        try:
            profile = Profile.objects.first()
            sender_email = (
                profile.email
                if profile and profile.email
                else 'hurairagulfaraz4@gmail.com'
            )
        except Exception:
            sender_email = 'hurairagulfaraz4@gmail.com'

        # Email to portfolio owner.
        admin_subject = f"New Contact: {subject} from {name}"
        admin_message = f"""Name: {name}
Email: {email}
Subject: {subject}

Message:
{message}
"""
        ContactEmailThread(
            subject=admin_subject,
            message=admin_message,
            from_email=sender_email,
            recipient_list=[sender_email],
        ).start()

        # Confirmation email to visitor.
        user_subject = f"Thank you for contacting me, {name}!"
        user_message = f"""Hi {name},

Thank you for reaching out! I've received your message and will get back to you as soon as possible.

Your message:
Subject: {subject}
{message}

Best regards,
Abu Huraira
Backend Developer
"""
        ContactEmailThread(
            subject=user_subject,
            message=user_message,
            from_email=sender_email,
            recipient_list=[email],
        ).start()

        messages.success(
            self.request,
            "Your message has been sent successfully! I'll get back to you soon.",
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field.capitalize()}: {error}")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Featured projects for home page
        context['featured_projects'] = Project.objects.filter(
            is_featured=True
        ).order_by('order', '-created_at')[:6]

        # All skills for circular charts
        context['skills'] = Skill.objects.all().order_by('order')

        # All experiences
        context['experiences'] = Experience.objects.all().order_by('-order', '-start_date')

        # All certifications
        context['certifications'] = Certification.objects.all().order_by('-order', '-issue_date')[:6]

        # Education history
        context['educations'] = Education.objects.all().order_by(
            'order', '-end_date', '-start_date'
        )

        # All projects (for filter)
        context['all_projects'] = Project.objects.all().order_by('order', '-created_at')

        # All technologies (for filter buttons)
        context['technologies'] = Technology.objects.all().order_by('name')

        return context

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from slugify import slugify


class Profile(models.Model):
    """
    Single instance model for portfolio profile settings and about content.
    """
    logo_image = models.ImageField(upload_to="logo_image/")
    about_image = models.ImageField(upload_to="about_image/")
    resume = models.FileField(upload_to='resume/', blank=True, null=True)

    # About content - managed from Django admin.
    about_intro = models.TextField(
        default="I'm a final-year Software Engineering student with a passion for backend development, especially in Python and the Django ecosystem.",
        help_text="First paragraph of the About section."
    )
    about_journey = models.TextField(
        blank=True,
        help_text="Second paragraph of the About section."
    )
    about_technical = models.TextField(
        blank=True,
        help_text="Third paragraph of the About section."
    )
    about_closing = models.TextField(
        default="Backend-focused. Consistently evolving. Passionate about clean code and scalable systems. Let's build something meaningful.",
        help_text="Closing line shown below the About paragraphs."
    )

    github_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone1 = models.CharField(max_length=20, blank=True, null=True, verbose_name="Primary Phone")
    phone2 = models.CharField(max_length=20, blank=True, null=True, verbose_name="Secondary Phone")

    def __str__(self):
        return "Portfolio Profile"

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profile"


class Technology(models.Model):
    """Technologies/tags used in Projects and Experiences."""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Technologies'
        ordering = ['name']


class Skill(models.Model):
    """Skills with percentage for circular chart."""
    skill_name = models.CharField(max_length=50)
    percentage = models.PositiveIntegerField(
        default=60,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Enter value between 0-100"
    )
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.skill_name} ({self.percentage}%)"

    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Skills'


class Contact(models.Model):
    """Contact form messages from visitors."""
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    message = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.email}"

    class Meta:
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"
        ordering = ['-created_at']


class Project(models.Model):
    """Portfolio projects with tech stack."""
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    short_description = models.CharField(max_length=300)
    detailed_description = models.TextField()
    image = models.ImageField(upload_to='project_images/')
    github_link = models.URLField(blank=True, null=True)
    live_link = models.URLField(blank=True, null=True)
    tech_stack = models.ManyToManyField(Technology, related_name='projects', blank=True)
    is_featured = models.BooleanField(default=True, help_text="Show on home page")
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('project_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Projects'
        ordering = ['order', '-created_at']


class Experience(models.Model):
    """Work experience - company wise."""
    company_name = models.CharField(max_length=200)
    position = models.CharField(max_length=150, help_text="e.g., Backend Developer")
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True, help_text="Leave empty if currently working")
    is_current = models.BooleanField(default=False)
    description = models.TextField(help_text="Overall role description")
    technologies_used = models.ManyToManyField(
        Technology,
        related_name='experiences',
        blank=True,
        help_text="Technologies used in this role"
    )
    company_logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0, help_text="Lower number = higher priority")

    def __str__(self):
        if self.is_current or not self.end_date:
            end = "Present"
        else:
            end = self.end_date.strftime("%b %Y")
        return f"{self.position} at {self.company_name} ({self.start_date.strftime('%b %Y')} - {end})"

    class Meta:
        verbose_name = "Experience"
        verbose_name_plural = "Experiences"
        ordering = ['-order', '-start_date']


class ExperienceProject(models.Model):
    """Projects done within an experience/company."""
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=200)
    description = models.TextField(help_text="Use bullet points: • Point 1\n• Point 2")
    technologies = models.ManyToManyField(
        Technology,
        blank=True,
        related_name='experience_projects',
        help_text="Specific technologies for this project"
    )
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.title} - {self.experience.company_name}"

    class Meta:
        verbose_name = "Experience Project"
        verbose_name_plural = "Experience Projects"
        ordering = ['order']


class Certification(models.Model):
    """Certifications and courses."""
    name = models.CharField(max_length=200)
    issuing_organization = models.CharField(max_length=200)
    credential_url = models.URLField(blank=True, null=True, verbose_name="Credential/Verify URL")
    issue_date = models.DateField()
    expiration_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    badge_image = models.ImageField(upload_to='certifications/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} - {self.issuing_organization}"

    class Meta:
        verbose_name = "Certification"
        verbose_name_plural = "Certifications"
        ordering = ['-order', '-issue_date']


class Education(models.Model):
    """Education history displayed in the About section."""
    degree = models.CharField(max_length=200, help_text="e.g., Bachelor of Software Engineering")
    field_of_study = models.CharField(max_length=200, blank=True, help_text="e.g., Software Engineering")
    institution = models.CharField(max_length=200)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True, help_text="For ongoing education, optionally enter the expected end date")
    is_current = models.BooleanField(default=False, help_text="Show this as current/ongoing education")
    description = models.TextField(blank=True, help_text="Optional additional details")
    order = models.PositiveIntegerField(default=0, help_text="Lower number = higher priority")

    def __str__(self):
        return f"{self.degree} - {self.institution}"

    class Meta:
        verbose_name = "Education"
        verbose_name_plural = "Education"
        ordering = ['order', '-end_date', '-start_date']

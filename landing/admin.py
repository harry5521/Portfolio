from django.contrib import admin
from django.utils.html import format_html, format_html_join

from .models import (
    Profile,
    Technology,
    Skill,
    Contact,
    Project,
    Experience,
    ExperienceProject,
    Certification,
)


# ==================== INLINE ADMIN ====================

class ExperienceProjectInline(admin.TabularInline):
    model = ExperienceProject
    extra = 1
    fields = ('title', 'description', 'technologies', 'order')
    filter_horizontal = ('technologies',)
    ordering = ('order',)


# ==================== PROFILE ADMIN ====================

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Images & Resume', {
            'fields': ('logo_image', 'about_image', 'resume'),
            'description': 'Logo appears in navbar and About image appears in the About section.',
        }),
        ('Contact Information', {
            'fields': ('email', 'phone1', 'phone2'),
            'classes': ('wide',),
        }),
        ('Social Links', {
            'fields': ('github_url', 'linkedin_url'),
            'classes': ('wide',),
        }),
    )
    list_display = ('id', 'email', 'get_phone_display')
    readonly_fields = ('id',)

    def get_phone_display(self, obj):
        return obj.phone1 or 'Not set'
    get_phone_display.short_description = 'Primary Phone'

    def has_add_permission(self, request):
        if Profile.objects.exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        if obj and Profile.objects.count() <= 1:
            return False
        return super().has_delete_permission(request, obj)


# ==================== TECHNOLOGY ADMIN ====================

@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'projects_count', 'experiences_count')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 50
    ordering = ('name',)

    def projects_count(self, obj):
        return obj.projects.count()
    projects_count.short_description = 'Projects'

    def experiences_count(self, obj):
        return obj.experiences.count()
    experiences_count.short_description = 'Experiences'


# ==================== SKILL ADMIN ====================

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('skill_name', 'percentage', 'order', 'get_percentage_bar')
    list_editable = ('percentage', 'order')
    list_filter = ('percentage',)
    search_fields = ('skill_name',)
    ordering = ('order', 'skill_name')
    list_per_page = 50

    def get_percentage_bar(self, obj):
        width = min(max(obj.percentage, 0), 100)
        return format_html(
            '<div style="display:flex;align-items:center;gap:8px;min-width:150px;">'
            '<div style="width:100px;background:#e5e7eb;border-radius:5px;height:10px;overflow:hidden;">'
            '<div style="width:{}%;background:#10b981;border-radius:5px;height:10px;"></div>'
            '</div><span>{}%</span></div>',
            width,
            obj.percentage,
        )
    get_percentage_bar.short_description = 'Progress'


# ==================== CONTACT ADMIN ====================

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'is_read', 'created_at', 'short_message')
    list_filter = ('is_read',)
    search_fields = ('name', 'email', 'message')
    list_editable = ('is_read',)
    readonly_fields = ('created_at',)
    list_per_page = 25
    ordering = ('-created_at',)
    actions = ('mark_as_read', 'mark_as_unread')

    fieldsets = (
        ('Contact Info', {
            'fields': ('name', 'email', 'is_read', 'created_at'),
        }),
        ('Message', {
            'fields': ('message',),
        }),
    )

    def short_message(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    short_message.short_description = 'Message'

    @admin.action(description='Mark selected as Read')
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} message(s) marked as read.')

    @admin.action(description='Mark selected as Unread')
    def mark_as_unread(self, request, queryset):
        updated = queryset.update(is_read=False)
        self.message_user(request, f'{updated} message(s) marked as unread.')


# ==================== PROJECT ADMIN ====================

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'is_featured',
        'order',
        'tech_count',
        'created_at',
        'get_links',
    )
    list_filter = ('is_featured', 'tech_stack')
    search_fields = ('title', 'slug', 'short_description', 'detailed_description')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tech_stack',)
    list_editable = ('is_featured', 'order')
    readonly_fields = ('created_at',)
    list_per_page = 20
    ordering = ('order', '-created_at')

    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'slug', 'is_featured', 'order'),
        }),
        ('Descriptions', {
            'fields': ('short_description', 'detailed_description'),
            'classes': ('wide',),
        }),
        ('Media & Links', {
            'fields': ('image', 'github_link', 'live_link'),
        }),
        ('Tech Stack', {
            'fields': ('tech_stack',),
            'classes': ('wide',),
        }),
        ('Meta', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )

    def tech_count(self, obj):
        return obj.tech_stack.count()
    tech_count.short_description = 'Techs'

    def get_links(self, obj):
        links = []
        if obj.github_link:
            links.append((obj.github_link, 'GitHub'))
        if obj.live_link:
            links.append((obj.live_link, 'Live'))

        if not links:
            return '-'

        return format_html_join(
            ' | ',
            '<a href="{}" target="_blank" rel="noopener noreferrer">{}</a>',
            links,
        )
    get_links.short_description = 'Links'


# ==================== EXPERIENCE ADMIN ====================

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = (
        'company_name',
        'position',
        'duration',
        'is_current',
        'order',
        'projects_count',
    )
    list_filter = ('is_current', 'technologies_used')
    search_fields = ('company_name', 'position', 'description')
    filter_horizontal = ('technologies_used',)
    list_editable = ('is_current', 'order')
    readonly_fields = ('duration_display',)
    inlines = (ExperienceProjectInline,)
    list_per_page = 20
    ordering = ('-order', '-start_date')

    fieldsets = (
        ('Company & Position', {
            'fields': ('company_name', 'position', 'company_logo', 'order'),
        }),
        ('Duration', {
            'fields': ('start_date', 'end_date', 'is_current', 'duration_display'),
            'description': 'Leave end_date empty if currently working here.',
        }),
        ('Description', {
            'fields': ('description',),
            'classes': ('wide',),
        }),
        ('Technologies Used', {
            'fields': ('technologies_used',),
            'classes': ('wide',),
        }),
    )

    def duration(self, obj):
        return self._format_duration(obj)
    duration.short_description = 'Duration'

    def duration_display(self, obj):
        return self._format_duration(obj)
    duration_display.short_description = 'Duration'

    @staticmethod
    def _format_duration(obj):
        start = obj.start_date.strftime('%b %Y') if obj.start_date else '—'
        if obj.is_current:
            end = 'Present'
        elif obj.end_date:
            end = obj.end_date.strftime('%b %Y')
        else:
            end = '—'
        return f'{start} - {end}'

    def projects_count(self, obj):
        return obj.projects.count()
    projects_count.short_description = 'Projects'


# ==================== CERTIFICATION ADMIN ====================

@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'issuing_organization',
        'issue_date',
        'expiration_date',
        'has_credential',
        'order',
    )
    list_filter = ('issuing_organization',)
    search_fields = ('name', 'issuing_organization', 'description')
    list_editable = ('order',)
    list_per_page = 20
    ordering = ('-order', '-issue_date')

    fieldsets = (
        ('Certification Info', {
            'fields': ('name', 'issuing_organization', 'order'),
        }),
        ('Dates', {
            'fields': ('issue_date', 'expiration_date'),
            'description': 'Leave expiration_date empty if no expiry.',
        }),
        ('Credential & Badge', {
            'fields': ('credential_url', 'badge_image'),
        }),
        ('Description', {
            'fields': ('description',),
            'classes': ('wide',),
        }),
    )

    def has_credential(self, obj):
        if obj.credential_url:
            return format_html(
                '<a href="{}" target="_blank" rel="noopener noreferrer">✓ Verify</a>',
                obj.credential_url,
            )
        return '✗'
    has_credential.short_description = 'Credential'


# ==================== ADMIN SITE CUSTOMIZATION ====================

admin.site.site_header = 'Portfolio Admin Panel'
admin.site.site_title = 'Portfolio Admin'
admin.site.index_title = 'Welcome to Portfolio Dashboard'

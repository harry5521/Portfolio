from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Certification,
    Contact,
    Education,
    Experience,
    ExperienceProject,
    Profile,
    Project,
    Skill,
    Technology,
)


class ExperienceProjectInline(admin.TabularInline):
    model = ExperienceProject
    extra = 1
    fields = ('title', 'description', 'technologies', 'order')
    filter_horizontal = ('technologies',)
    ordering = ('order',)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Images & Resume', {
            'fields': ('logo_image', 'about_image', 'resume'),
            'description': 'Logo appears in navbar. About image is used in the hero/profile visual.'
        }),
        ('About Content', {
            'fields': ('about_intro', 'about_journey', 'about_technical', 'about_closing'),
            'classes': ('wide',),
            'description': 'These fields control the About section. Hero text remains fixed in the template.'
        }),
        ('Contact Information', {
            'fields': ('email', 'phone1', 'phone2'),
            'classes': ('wide',)
        }),
        ('Social Links', {
            'fields': ('github_url', 'linkedin_url'),
            'classes': ('wide',)
        }),
    )
    list_display = ('id', 'email', 'get_phone_display')
    readonly_fields = ('id',)

    @admin.display(description='Primary Phone')
    def get_phone_display(self, obj):
        return obj.phone1 or 'Not set'

    def has_add_permission(self, request):
        if Profile.objects.exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        if obj and Profile.objects.count() <= 1:
            return False
        return super().has_delete_permission(request, obj)


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('degree', 'institution', 'start_date', 'end_date_display', 'is_current', 'order')
    list_filter = ('is_current', 'institution')
    search_fields = ('degree', 'field_of_study', 'institution', 'description')
    list_editable = ('is_current', 'order')
    ordering = ('order', '-end_date', '-start_date')
    list_per_page = 20

    fieldsets = (
        ('Education', {
            'fields': ('degree', 'field_of_study', 'institution', 'order')
        }),
        ('Duration', {
            'fields': ('start_date', 'end_date', 'is_current'),
            'description': 'Leave end_date empty if this education is ongoing.'
        }),
        ('Additional Details', {
            'fields': ('description',),
            'classes': ('wide',)
        }),
    )

    @admin.display(description='End Date', ordering='end_date')
    def end_date_display(self, obj):
        if obj.is_current or not obj.end_date:
            return 'Present' if obj.is_current else '-'
        return obj.end_date.strftime('%b %Y')


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'projects_count', 'experiences_count')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 50

    @admin.display(description='Projects')
    def projects_count(self, obj):
        return obj.projects.count()

    @admin.display(description='Experiences')
    def experiences_count(self, obj):
        return obj.experiences.count()


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('skill_name', 'percentage', 'order', 'get_percentage_bar')
    list_editable = ('order', 'percentage')
    list_filter = ('percentage',)
    search_fields = ('skill_name',)
    ordering = ('order',)
    list_per_page = 50

    @admin.display(description='Progress')
    def get_percentage_bar(self, obj):
        width = min(obj.percentage, 100)
        return format_html(
            '<div style="display:flex;align-items:center;gap:8px;min-width:140px;">'
            '<div style="width:100px;background:#e5e7eb;border-radius:5px;height:10px;">'
            '<div style="width:{}%;background:{};border-radius:5px;height:10px;"></div>'
            '</div><span>{}%</span></div>',
            width,
            '#10b981' if width >= 70 else '#f59e0b' if width >= 40 else '#ef4444',
            obj.percentage,
        )


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'is_read', 'created_at', 'short_message')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'message')
    list_editable = ('is_read',)
    readonly_fields = ('created_at',)
    list_per_page = 25
    actions = ('mark_as_read', 'mark_as_unread')

    fieldsets = (
        ('Contact Info', {
            'fields': ('name', 'email', 'is_read', 'created_at')
        }),
        ('Message', {
            'fields': ('message',)
        }),
    )

    @admin.display(description='Message')
    def short_message(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message

    @admin.action(description='Mark selected as Read')
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} message(s) marked as read.')

    @admin.action(description='Mark selected as Unread')
    def mark_as_unread(self, request, queryset):
        updated = queryset.update(is_read=False)
        self.message_user(request, f'{updated} message(s) marked as unread.')



@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_featured', 'order', 'tech_count', 'created_at', 'get_links')
    list_filter = ('is_featured', 'tech_stack', 'created_at')
    search_fields = ('title', 'short_description', 'detailed_description')
    filter_horizontal = ('tech_stack',)
    list_editable = ('is_featured', 'order')
    readonly_fields = ('created_at',)
    list_per_page = 20

    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'is_featured', 'order')
        }),
        ('Descriptions', {
            'fields': ('short_description', 'detailed_description'),
            'classes': ('wide',)
        }),
        ('Media & Links', {
            'fields': ('image', 'github_link', 'live_link')
        }),
        ('Tech Stack', {
            'fields': ('tech_stack',),
            'classes': ('wide',)
        }),
        ('Meta', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    @admin.display(description='Techs')
    def tech_count(self, obj):
        return obj.tech_stack.count()

    @admin.display(description='Links')
    def get_links(self, obj):
        if obj.github_link and obj.live_link:
            return format_html(
                '<a href="{}" target="_blank" rel="noopener noreferrer">GitHub</a> | '
                '<a href="{}" target="_blank" rel="noopener noreferrer">Live</a>',
                obj.github_link,
                obj.live_link,
            )
        if obj.github_link:
            return format_html(
                '<a href="{}" target="_blank" rel="noopener noreferrer">GitHub</a>',
                obj.github_link,
            )
        if obj.live_link:
            return format_html(
                '<a href="{}" target="_blank" rel="noopener noreferrer">Live</a>',
                obj.live_link,
            )
        return '-'



@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'position', 'duration', 'is_current', 'order', 'projects_count')
    list_filter = ('is_current', 'technologies_used')
    search_fields = ('company_name', 'position', 'description')
    filter_horizontal = ('technologies_used',)
    list_editable = ('is_current', 'order')
    readonly_fields = ('get_duration_display',)
    inlines = [ExperienceProjectInline]
    list_per_page = 20

    fieldsets = (
        ('Company & Position', {
            'fields': ('company_name', 'position', 'company_logo', 'order')
        }),
        ('Duration', {
            'fields': ('start_date', 'end_date', 'is_current', 'get_duration_display'),
            'description': 'Leave end_date empty if currently working here.'
        }),
        ('Description', {
            'fields': ('description',),
            'classes': ('wide',)
        }),
        ('Technologies Used', {
            'fields': ('technologies_used',),
            'classes': ('wide',)
        }),
    )

    @admin.display(description='Duration')
    def duration(self, obj):
        return self._duration(obj)

    @admin.display(description='Duration')
    def get_duration_display(self, obj):
        return self._duration(obj)

    @staticmethod
    def _duration(obj):
        start = obj.start_date.strftime('%b %Y')
        end = 'Present' if obj.is_current or not obj.end_date else obj.end_date.strftime('%b %Y')
        return f'{start} - {end}'

    @admin.display(description='Projects')
    def projects_count(self, obj):
        return obj.projects.count()


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ('name', 'issuing_organization', 'issue_date', 'expiration_date', 'has_credential', 'order')
    list_filter = ('issuing_organization', 'issue_date')
    search_fields = ('name', 'issuing_organization', 'description')
    list_editable = ('order',)
    list_per_page = 20

    fieldsets = (
        ('Certification Info', {
            'fields': ('name', 'issuing_organization', 'order')
        }),
        ('Dates', {
            'fields': ('issue_date', 'expiration_date'),
            'description': 'Leave expiration_date empty if no expiry.'
        }),
        ('Credential & Badge', {
            'fields': ('credential_url', 'badge_image')
        }),
        ('Description', {
            'fields': ('description',),
            'classes': ('wide',)
        }),
    )

    @admin.display(description='Credential')
    def has_credential(self, obj):
        if not obj.credential_url:
            return '✗'
        return format_html(
            '<a href="{}" target="_blank" rel="noopener noreferrer">✓ Verify</a>',
            obj.credential_url
        )


admin.site.site_header = "Portfolio Admin Panel"
admin.site.site_title = "Portfolio Admin"
admin.site.index_title = "Welcome to Portfolio Dashboard"

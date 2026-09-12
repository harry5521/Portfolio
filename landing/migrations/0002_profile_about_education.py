from django.db import migrations, models


def create_initial_education(apps, schema_editor):
    Education = apps.get_model('landing', 'Education')
    if not Education.objects.exists():
        Education.objects.create(
            degree='Bachelors in Software Engineering',
            field_of_study='Software Engineering',
            institution='Sindh Madressatul Islam University (SMIU), Karachi',
            end_date='2026-12-31',
            is_current=True,
            order=0,
        )


def remove_initial_education(apps, schema_editor):
    Education = apps.get_model('landing', 'Education')
    Education.objects.filter(
        degree='Bachelors in Software Engineering',
        institution='Sindh Madressatul Islam University (SMIU), Karachi',
    ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('landing', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='about_intro',
            field=models.TextField(default="I'm a final-year Software Engineering student with a passion for backend development, especially in Python and the Django ecosystem.", help_text='First paragraph of the About section.'),
        ),
        migrations.AddField(
            model_name='profile',
            name='about_journey',
            field=models.TextField(default="My journey began with mastering Python's scripting and OOP capabilities, followed by a strong foundation in web fundamentals through Flask and then advancing to real-world development with Django and Django REST Framework.", help_text='Second paragraph of the About section.'),
        ),
        migrations.AddField(
            model_name='profile',
            name='about_technical',
            field=models.TextField(default="I've worked with MySQL and continue to strengthen my skills in PostgreSQL to deepen my database expertise. On the frontend, I'm familiar with HTML, CSS, Tailwind, and JavaScript, but my core focus remains on backend development.", help_text='Third paragraph of the About section.'),
        ),
        migrations.AddField(
            model_name='profile',
            name='about_closing',
            field=models.TextField(default="Backend-focused. Consistently evolving. Passionate about clean code and scalable systems. Let's build something meaningful.", help_text='Closing line shown below the About paragraphs.'),
        ),
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('degree', models.CharField(help_text='e.g., Bachelor of Software Engineering', max_length=200)),
                ('field_of_study', models.CharField(blank=True, help_text='e.g., Software Engineering', max_length=200)),
                ('institution', models.CharField(max_length=200)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, help_text='For ongoing education, optionally enter the expected end date', null=True)),
                ('is_current', models.BooleanField(default=False, help_text='Show this as current/ongoing education')),
                ('description', models.TextField(blank=True, help_text='Optional additional details')),
                ('order', models.PositiveIntegerField(default=0, help_text='Lower number = higher priority')),
            ],
            options={
                'verbose_name': 'Education',
                'verbose_name_plural': 'Education',
                'ordering': ['order', '-end_date', '-start_date'],
            },
        ),
        migrations.RunPython(create_initial_education, remove_initial_education),
    ]

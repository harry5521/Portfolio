from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("landing", "0003_alter_skill_percentage"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="about_journey",
            field=models.TextField(
                blank=True,
                default="My journey began with mastering Python's scripting and OOP capabilities, followed by a strong foundation in web fundamentals through Flask and then advancing to real-world development with Django and Django REST Framework.",
                help_text="Second paragraph of the About section. Optional.",
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="about_technical",
            field=models.TextField(
                blank=True,
                default="I've worked with MySQL and continue to strengthen my skills in PostgreSQL to deepen my database expertise. On the frontend, I'm familiar with HTML, CSS, Tailwind, and JavaScript, but my core focus remains on backend development.",
                help_text="Third paragraph of the About section. Optional.",
            ),
        ),
    ]

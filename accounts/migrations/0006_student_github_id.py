# Generated by Django 4.2.7 on 2024-05-12 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_student_linkedin_id_alter_student_profile_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='github_id',
            field=models.URLField(blank=True, null=True),
        ),
    ]

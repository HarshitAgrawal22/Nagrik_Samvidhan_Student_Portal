# Generated by Django 4.2.7 on 2024-06-21 04:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_scholarshiptest'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.TextField()),
                ('description', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='question_images/')),
                ('video', models.URLField(blank=True, null=True)),
                ('audio', models.URLField(blank=True, null=True)),
                ('option1', models.CharField(max_length=255)),
                ('option2', models.CharField(max_length=255)),
                ('option3', models.CharField(max_length=255)),
                ('option4', models.CharField(max_length=255)),
                ('correct_option', models.CharField(max_length=1)),
            ],
        ),
        migrations.RemoveField(
            model_name='scholarshiptest',
            name='contact_number',
        ),
        migrations.RemoveField(
            model_name='scholarshiptest',
            name='created_at',
        ),
        migrations.AlterField(
            model_name='scholarshiptest',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.CreateModel(
            name='StudentSubmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('mobile_number', models.CharField(max_length=15)),
                ('selected_option', models.CharField(max_length=1)),
                ('submission_time', models.DateTimeField(auto_now_add=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.question')),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.scholarshiptest'),
        ),
    ]

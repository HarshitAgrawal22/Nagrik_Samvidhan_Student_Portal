# Generated by Django 4.2.7 on 2024-05-16 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Flames',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('whatsapp_number', models.CharField(max_length=100)),
                ('contact_number', models.CharField(max_length=100)),
                ('college', models.CharField(max_length=100)),
                ('mode', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]

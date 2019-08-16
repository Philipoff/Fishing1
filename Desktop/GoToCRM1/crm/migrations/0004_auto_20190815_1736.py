# Generated by Django 2.2.4 on 2019-08-15 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0003_student_about'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='description',
        ),
        migrations.AddField(
            model_name='course',
            name='about',
            field=models.TextField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='about',
            field=models.TextField(max_length=255, null=True),
        ),
    ]
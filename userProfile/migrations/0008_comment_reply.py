# Generated by Django 4.0 on 2022-01-16 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userProfile', '0007_comment_mothercomment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='reply',
            field=models.ManyToManyField(blank=True, null=True, to='userProfile.Comment'),
        ),
    ]
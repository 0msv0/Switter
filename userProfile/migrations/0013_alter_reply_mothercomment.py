# Generated by Django 4.0 on 2022-01-16 09:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userProfile', '0012_remove_comment_mothercomment_remove_comment_replies_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reply',
            name='motherComment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='userProfile.comment'),
        ),
    ]

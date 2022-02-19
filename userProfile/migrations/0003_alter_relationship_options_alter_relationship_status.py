# Generated by Django 4.0 on 2022-01-11 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userProfile', '0002_alter_relationship_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='relationship',
            options={},
        ),
        migrations.AlterField(
            model_name='relationship',
            name='status',
            field=models.CharField(choices=[('send', 'send'), ('accepted', 'accepted'), ('remove', 'remove')], max_length=8),
        ),
    ]

# Generated by Django 4.0 on 2022-01-13 04:51

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('userProfile', '0004_alter_post_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('like', 'like'), ('dislike', 'dislike')], max_length=8)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userProfile.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userProfile.profile')),
            ],
        ),
        migrations.CreateModel(
            name='comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(help_text='Enter your comment: ', max_length=600)),
                ('createDate', models.DateTimeField(default=django.utils.timezone.now)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userProfile.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userProfile.profile')),
            ],
        ),
    ]
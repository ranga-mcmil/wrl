# Generated by Django 3.2.14 on 2022-07-21 22:05

from django.db import migrations, models
import django.db.models.deletion
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkSupervisor',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('accounts.user',),
        ),
        migrations.RemoveField(
            model_name='user',
            name='photo',
        ),
        migrations.AddField(
            model_name='user',
            name='pic',
            field=django_resized.forms.ResizedImageField(blank=True, crop=['top', 'left'], force_format='JPEG', keep_meta=True, null=True, quality=75, scale=0.5, size=[500, 500], upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='user',
            name='type',
            field=models.CharField(choices=[('STUDENT', 'Student'), ('SUPERVISOR', 'Supervisor'), ('WORK_SUPERVISOR', 'Work_Supervisor')], max_length=50, verbose_name='Type'),
        ),
        migrations.CreateModel(
            name='StudentProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('programme', models.CharField(blank=True, max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='accounts.student')),
            ],
        ),
    ]

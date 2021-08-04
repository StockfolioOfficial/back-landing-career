# Generated by Django 3.2.5 on 2021-08-04 05:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('applications', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recruit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('position', models.CharField(max_length=50)),
                ('description', models.TextField()),
            ],
            options={
                'db_table': 'recruits',
            },
        ),
        migrations.CreateModel(
            name='Stack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('hash_id', models.CharField(max_length=64, unique=True)),
            ],
            options={
                'db_table': 'stacks',
            },
        ),
        migrations.CreateModel(
            name='RecruitStack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recruit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recruits.recruit')),
                ('stack', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recruits.stack')),
            ],
            options={
                'db_table': 'recruits_stacks',
            },
        ),
        migrations.CreateModel(
            name='RecruitApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='applications.application')),
                ('recruit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recruits.recruit')),
            ],
            options={
                'db_table': 'recruits_applications',
            },
        ),
        migrations.AddField(
            model_name='recruit',
            name='applications',
            field=models.ManyToManyField(related_name='recruits', through='recruits.RecruitApplication', to='applications.Application'),
        ),
        migrations.AddField(
            model_name='recruit',
            name='stacks',
            field=models.ManyToManyField(related_name='recruits', through='recruits.RecruitStack', to='recruits.Stack'),
        ),
    ]

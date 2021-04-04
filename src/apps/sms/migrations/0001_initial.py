# Generated by Django 3.1.6 on 2021-04-04 15:58

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SMS',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('phone_num', models.CharField(max_length=32)),
                ('code', models.CharField(max_length=16)),
                ('purpose', models.CharField(max_length=32)),
                ('is_used', models.BooleanField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]

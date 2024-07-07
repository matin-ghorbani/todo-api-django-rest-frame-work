# Generated by Django 5.0.3 on 2024-07-04 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Todo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('content', models.TextField(blank=True)),
                ('priority', models.IntegerField(default=1)),
                ('is_done', models.BooleanField(default=False, verbose_name='is done?')),
            ],
            options={
                'db_table': 'todos',
            },
        ),
    ]
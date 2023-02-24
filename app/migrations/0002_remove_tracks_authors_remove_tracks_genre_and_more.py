# Generated by Django 4.1.7 on 2023-02-23 14:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tracks',
            name='authors',
        ),
        migrations.RemoveField(
            model_name='tracks',
            name='genre',
        ),
        migrations.AddField(
            model_name='tracks',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='app.authors'),
        ),
        migrations.AddField(
            model_name='tracks',
            name='genres',
            field=models.ManyToManyField(to='app.genres'),
        ),
    ]

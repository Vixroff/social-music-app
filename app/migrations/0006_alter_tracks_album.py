# Generated by Django 4.1.7 on 2023-02-26 12:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_rename_authors_artists'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tracks',
            name='album',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='app.albums'),
        ),
    ]

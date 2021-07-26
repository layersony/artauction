# Generated by Django 2.1 on 2021-07-26 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0002_auto_20210726_0851'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user_type',
            old_name='is_student',
            new_name='is_buyer',
        ),
        migrations.RenameField(
            model_name='user_type',
            old_name='is_teach',
            new_name='is_seller',
        ),
        migrations.AddField(
            model_name='profile',
            name='nickname',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]

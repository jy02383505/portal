# Generated by Django 2.2 on 2019-10-10 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_auto_20191010_1456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operatelog',
            name='user_type',
            field=models.CharField(db_index=True, default='', max_length=200, verbose_name='操作用户'),
        ),
    ]

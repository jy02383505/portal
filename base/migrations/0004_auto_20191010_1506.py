# Generated by Django 2.2 on 2019-10-10 15:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_auto_20191010_1504'),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name='operatelog',
            index_together={('user', 'add_time')},
        ),
    ]
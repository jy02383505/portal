# Generated by Django 2.2 on 2019-10-10 14:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name='operatelog',
            index_together={('user_type', 'user', 'add_time')},
        ),
    ]

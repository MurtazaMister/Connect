# Generated by Django 4.0 on 2022-01-07 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0007_privateroom_type_alter_privateroom_admin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='privateroom',
            name='type',
            field=models.CharField(choices=[('INDIV', 'indiv'), ('GROUP', 'group')], default='GROUP', max_length=5),
        ),
    ]

# Generated by Django 3.1.4 on 2022-06-10 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogpost', '0004_auto_20220610_0758'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='postcomment',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]

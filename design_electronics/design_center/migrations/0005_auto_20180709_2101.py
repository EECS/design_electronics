# Generated by Django 2.0.2 on 2018-07-10 04:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('design_center', '0004_auto_20180615_1416'),
    ]

    operations = [
        migrations.CreateModel(
            name='DesignParamChoices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('params', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='dcdc',
            name='description',
            field=models.TextField(default='1', help_text='Enter a description of the circuit to be modeled.'),
        ),
        migrations.AlterField(
            model_name='dcdc',
            name='url',
            field=models.CharField(default='1', help_text='Enter the url to be used to access this model.', max_length=200),
        ),
        migrations.AddField(
            model_name='dcdc',
            name='design_params',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='design_center.DesignParamChoices'),
        ),
    ]
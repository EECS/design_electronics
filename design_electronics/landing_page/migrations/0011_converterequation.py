# Generated by Django 2.0.2 on 2018-04-25 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('landing_page', '0010_auto_20180326_1723'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConverterEquation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter the name of this converter in the admin page.', max_length=200)),
                ('input_output_transfer', models.TextField(help_text='Enter the input to output transfer function of the converter.', max_length=5000)),
                ('input_impedance', models.TextField(help_text='Enter the input impedance of the converter.', max_length=5000)),
                ('output_impedance', models.TextField(help_text='Enter the output impedance of the converter.', max_length=5000)),
                ('duty_output_transfer', models.TextField(help_text='Enter the duty to output transfer function of the converter.', max_length=5000)),
            ],
        ),
    ]
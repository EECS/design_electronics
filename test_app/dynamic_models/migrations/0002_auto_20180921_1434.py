# Generated by Django 2.0.5 on 2018-09-21 21:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dynamic_models', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='openloopanalysisequations',
            options={'ordering': ['circuit_url'], 'verbose_name': 'Open-Loop Analysis Equation', 'verbose_name_plural': 'Open-Loop Analysis Equations'},
        ),
        migrations.AlterModelOptions(
            name='recommendedcomponents',
            options={'ordering': ['components'], 'verbose_name': 'component', 'verbose_name_plural': 'Recommended Components'},
        ),
    ]

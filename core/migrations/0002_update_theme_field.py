# Generated manually for theme field update

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='theme',
            field=models.CharField(choices=[('light', 'Light'), ('dark', 'Dark'), ('system', 'System')], default='light', max_length=10),
        ),
    ]

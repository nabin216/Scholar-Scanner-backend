from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('scholarships', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='country',
            options={'ordering': ['name'], 'verbose_name_plural': 'Countries'},
        ),
    ]
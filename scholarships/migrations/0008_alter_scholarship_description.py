from django.db import migrations
import ckeditor.fields

class Migration(migrations.Migration):
    dependencies = [
        ('scholarships', '0007_populate_country_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scholarship',
            name='description',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
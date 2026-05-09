from django.db import migrations, models
from django.utils.text import slugify


def generate_slugs(apps, schema_editor):
    Scholarship = apps.get_model('scholarships', 'Scholarship')
    for scholarship in Scholarship.objects.all():
        base_slug = slugify(scholarship.title)
        slug = base_slug
        counter = 1
        while Scholarship.objects.filter(slug=slug).exclude(pk=scholarship.pk).exists():
            slug = f'{base_slug}-{counter}'
            counter += 1
        scholarship.slug = slug
        scholarship.save()


class Migration(migrations.Migration):

    dependencies = [
        ('scholarships', '0014_remove_uuid'),
    ]

    operations = [
        # Add field without unique constraint first
        migrations.AddField(
            model_name='scholarship',
            name='slug',
            field=models.SlugField(blank=True, max_length=250),
        ),
        # Populate slugs for all existing records
        migrations.RunPython(generate_slugs, migrations.RunPython.noop),
        # Now add the unique constraint
        migrations.AlterField(
            model_name='scholarship',
            name='slug',
            field=models.SlugField(blank=True, max_length=250, unique=True),
        ),
    ]

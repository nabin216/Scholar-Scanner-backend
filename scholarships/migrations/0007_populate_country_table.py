from django.db import migrations

def populate_countries(apps, schema_editor):
    Country = apps.get_model('scholarships', 'Country')
    countries = [
        'United States', 'United Kingdom', 'Canada', 'Australia', 'Germany', 'France', 'Japan',
        'China', 'India', 'Netherlands', 'Sweden', 'Norway', 'Denmark', 'Finland', 'Ireland',
        'New Zealand', 'Singapore', 'South Korea', 'Spain', 'Italy', 'Switzerland', 'Belgium',
        'Austria', 'Portugal', 'Brazil', 'Mexico', 'Russia', 'South Africa', 'United Arab Emirates',
        'Israel', 'Poland', 'Czech Republic', 'Hungary', 'Greece', 'Turkey'
    ]
    for country_name in countries:
        Country.objects.create(name=country_name)

def reverse_countries(apps, schema_editor):
    Country = apps.get_model('scholarships', 'Country')
    Country.objects.all().delete()

class Migration(migrations.Migration):
    dependencies = [
        ('scholarships', '0006_country_data_migration'),
    ]

    operations = [
        migrations.RunPython(populate_countries, reverse_countries),
    ]
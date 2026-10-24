# Restores a migration that 0016_merge_20260509_2042 depends on but was never committed.
# Its change (image -> optional ImageField) is already applied by
# 0013_scholarship_uuid_alter_scholarship_image, so this is intentionally a no-op.

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scholarships', '0012_scholarship_amount'),
    ]

    operations = [
    ]

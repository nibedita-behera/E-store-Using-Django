from django.db import migrations
from api.user.models import CustomUser

class Migration(migrations.Migration):
    def seed_data(apps, Schema_edition):
        user= CustomUser(name="Kitu",
                          email="abc@gmail.com",
                          is_staff=True,
                          is_superuser=True,
                          phone="987654321",
                          gender="female"

        )
        user.set_password("12345")
        user.save()
    dependencies= [

    ]
    operations=[
        migrations.RunPython(seed_data),
    ]
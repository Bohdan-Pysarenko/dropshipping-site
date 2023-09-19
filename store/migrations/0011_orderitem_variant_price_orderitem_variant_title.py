# Generated by Django 4.0 on 2023-09-18 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_contactus_remove_product_attributes_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='variant_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='variant_title',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
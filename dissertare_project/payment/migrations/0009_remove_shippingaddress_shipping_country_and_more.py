# Generated by Django 4.2.16 on 2024-12-01 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0008_alter_invoices_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shippingaddress',
            name='shipping_country',
        ),
        migrations.RemoveField(
            model_name='shippingaddress',
            name='shipping_state',
        ),
        migrations.RemoveField(
            model_name='shippingaddress',
            name='shipping_zipcode',
        ),
        migrations.AddField(
            model_name='shippingaddress',
            name='shipping_mode',
            field=models.CharField(blank=True, choices=[('Home', 'Home'), ('Store', 'Store')], max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='shippingaddress',
            name='shipping_phone_number',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]

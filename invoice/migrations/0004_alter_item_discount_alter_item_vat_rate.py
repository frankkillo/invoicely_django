# Generated by Django 4.0.4 on 2022-05-14 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0003_alter_item_net_amount_alter_item_unit_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='discount',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='item',
            name='vat_rate',
            field=models.IntegerField(default=0),
        ),
    ]
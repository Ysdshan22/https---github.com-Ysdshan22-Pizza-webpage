from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_alter_order_status'),
    ]

    operations = [
        # Emoji fields
        migrations.AddField(
            model_name='pizza',
            name='emoji',
            field=models.CharField(default='🍕', max_length=10),
        ),
        migrations.AddField(
            model_name='drink',
            name='emoji',
            field=models.CharField(default='🥤', max_length=10),
        ),
        # available_toppings M2M on Pizza
        migrations.AddField(
            model_name='pizza',
            name='available_toppings',
            field=models.ManyToManyField(blank=True, related_name='pizzas', to='orders.Topping'),
        ),
        # Coupon fields on Order
        migrations.AddField(
            model_name='order',
            name='coupon_code',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
        migrations.AddField(
            model_name='order',
            name='discount_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
        # Updated status choices (add Ready for Pickup)
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(
                choices=[('P', 'Pending'), ('PR', 'Preparing'), ('R', 'Ready for Pickup'), ('D', 'Delivered')],
                default='P',
                max_length=2,
            ),
        ),
        # Coupon model
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20, unique=True)),
                ('discount_percent', models.PositiveIntegerField()),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        # Location model
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=20)),
                ('opening_hours', models.CharField(max_length=100)),
                ('map_embed_url', models.URLField(blank=True, max_length=500)),
            ],
        ),
    ]

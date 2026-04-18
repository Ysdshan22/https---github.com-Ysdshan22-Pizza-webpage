from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_side_pizza_allergens_pizza_category_pizza_image_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pizza',
            name='is_vegetarian',
        ),
        migrations.RemoveField(
            model_name='pizza',
            name='is_vegan',
        ),
        migrations.AddField(
            model_name='pizza',
            name='can_be_vegetarian',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='pizza',
            name='can_be_vegan',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='pizza',
            name='can_be_glutenfree',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='pizza',
            name='can_be_dairyfree',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='pizza',
            name='category',
            field=models.CharField(
                choices=[
                    ('bestseller', 'Best Seller'),
                    ('discount', 'Discount'),
                    ('classic', 'Classic'),
                ],
                default='classic',
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name='side',
            name='_side_type_salad',
            field=models.CharField(
                choices=[
                    ('nuggets', 'Chicken Nuggets'),
                    ('mozzarella', 'Mozzarella Sticks'),
                    ('churros', 'Churros'),
                    ('chilli', 'Chilli Poppers'),
                    ('dip', 'Dip Sauce'),
                    ('salad', 'Salad'),
                ],
                default='dip',
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='dietary',
            field=models.CharField(
                blank=True,
                choices=[
                    ('', 'Standard'),
                    ('vegetarian', 'Vegetarian'),
                    ('vegan', 'Vegan'),
                    ('glutenfree', 'Gluten-Free'),
                    ('dairyfree', 'Dairy-Free'),
                ],
                default='',
                max_length=20,
            ),
        ),
    ]

from django.db import migrations


def seed(apps, schema_editor):
    Side = apps.get_model('orders', 'Side')
    Drink = apps.get_model('orders', 'Drink')

    # Clear old sides/dips/drinks and re-seed cleanly
    Side.objects.all().delete()
    Drink.objects.all().delete()

    # Sides (food)
    sides = [
        ('Fish Nuggets', 'nuggets', 'Crispy battered fish nuggets, served with dip', 79),
        ('Chicken Nuggets', 'nuggets', 'Golden fried chicken nuggets, 8 pieces', 79),
        ('Mozzarella Sticks', 'mozzarella', 'Breaded mozzarella sticks with marinara dip', 89),
        ('Chilli Poppers', 'chilli', 'Jalapeño poppers stuffed with cream cheese', 79),
        ('Churros', 'churros', 'Cinnamon sugar churros with chocolate dipping sauce', 69),
        ('Caprese Salat', 'salad', 'Fresh mozzarella, ripe tomato, basil, and olive oil', 89),
    ]
    for name, side_type, desc, price in sides:
        Side.objects.create(name=name, side_type=side_type, description=desc, price=price)

    # Dips
    dips = [
        ('Truffle Dip', 'dip', 'Rich truffle aioli', 29),
        ('BBQ Dip', 'dip', 'Smoky classic BBQ sauce', 19),
        ('Spicy Dip', 'dip', 'Hot chilli sauce with a kick', 19),
        ('Classic Dip', 'dip', 'Creamy garlic mayo', 19),
        ('Spicy Cheddar Dip', 'dip', 'Melted cheddar with jalapeño', 29),
    ]
    for name, side_type, desc, price in dips:
        Side.objects.create(name=name, side_type=side_type, description=desc, price=price)

    # Drinks
    drinks = [
        ('Cola', 35),
        ('Fanta', 35),
        ('Pepsi', 35),
        ('Farris', 29),
        ('Solo', 35),
        ('Sprite', 35),
    ]
    for name, price in drinks:
        Drink.objects.create(name=name, price=price)


def reverse_seed(apps, schema_editor):
    Side = apps.get_model('orders', 'Side')
    Drink = apps.get_model('orders', 'Drink')
    Side.objects.all().delete()
    Drink.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0011_seed_new_pizzas_and_caprese'),
    ]

    operations = [
        migrations.RunPython(seed, reverse_seed),
    ]

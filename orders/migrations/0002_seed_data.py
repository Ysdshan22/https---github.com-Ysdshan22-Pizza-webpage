from django.db import migrations


def seed(apps, schema_editor):
    Pizza = apps.get_model('orders', 'Pizza')
    Side = apps.get_model('orders', 'Side')
    Drink = apps.get_model('orders', 'Drink')

    # Pizzas
    pizzas = [
        # Best sellers
        ('Pepperoni', 'Loaded with spicy pepperoni and melted cheese, a crowd favourite', 'bestseller', 139, 179, 219),
        ('Picante', 'Spicy salami, jalapeños, and chilli flakes on a rich tomato base', 'bestseller', 149, 189, 229),
        ('Beef', 'Seasoned beef mince, red onion, and mozzarella with BBQ drizzle', 'bestseller', 149, 189, 229),
        ('Margherita', 'A classic Norwegian favourite with fresh tomato and creamy mozzarella', 'bestseller', 119, 159, 199),
        # Classic
        ('Chicken', 'Grilled chicken, roasted peppers, and fresh mozzarella on white base', 'classic', 149, 189, 229),
        ('Nduja', 'Fiery spreadable Nduja sausage with buffalo mozzarella and basil', 'classic', 159, 199, 239),
        ('Truffle Salami', 'Premium salami with truffle oil, mushrooms, and aged parmesan', 'classic', 169, 209, 249),
        ('Tomat', 'Simple and fresh: San Marzano tomato, garlic, olive oil, and oregano', 'classic', 109, 149, 189),
        ("Devil's Playground", 'Double pepperoni, ghost chilli sauce, and habanero for the brave', 'classic', 159, 199, 239),
    ]
    for name, desc, cat, ps, pm, pl in pizzas:
        Pizza.objects.create(name=name, description=desc, category=cat,
                             price_small=ps, price_medium=pm, price_large=pl)

    # Sides
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
        ('Cola', 35), ('Fanta', 35), ('Pepsi', 35),
        ('Farris', 29), ('Solo', 35), ('Sprite', 35),
    ]
    for name, price in drinks:
        Drink.objects.create(name=name, price=price)


def reverse_seed(apps, schema_editor):
    Pizza = apps.get_model('orders', 'Pizza')
    Side = apps.get_model('orders', 'Side')
    Drink = apps.get_model('orders', 'Drink')
    Pizza.objects.all().delete()
    Side.objects.all().delete()
    Drink.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
    ('orders', '0001_initial'),
]

    operations = [
        migrations.RunPython(seed, reverse_seed),
    ]

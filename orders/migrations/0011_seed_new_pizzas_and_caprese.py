from django.db import migrations


def seed_data(apps, schema_editor):
    Pizza = apps.get_model('orders', 'Pizza')
    Side = apps.get_model('orders', 'Side')

    # Remove old vegan/vegetarian category pizzas
    Pizza.objects.filter(category__in=['vegan', 'vegetarian']).delete()

    new_pizzas = [
        # Best sellers
        dict(name='Pepperoni', description='Loaded with spicy pepperoni and melted cheese, a crowd favourite', category='bestseller', price_small=139, price_medium=179, price_large=219),
        dict(name='Picante', description='Spicy salami, jalapeños, and chilli flakes on a rich tomato base', category='bestseller', price_small=149, price_medium=189, price_large=229),
        dict(name='Beef', description='Seasoned beef mince, red onion, and mozzarella with BBQ drizzle', category='bestseller', price_small=149, price_medium=189, price_large=229),
        dict(name='Margherita', description='A classic Norwegian favourite with fresh tomato and creamy mozzarella', category='bestseller', price_small=119, price_medium=159, price_large=199),
        # Classic
        dict(name='Chicken', description='Grilled chicken, roasted peppers, and fresh mozzarella on white base', category='classic', price_small=149, price_medium=189, price_large=229),
        dict(name="Nduja", description="Fiery spreadable Nduja sausage with buffalo mozzarella and basil", category='classic', price_small=159, price_medium=199, price_large=239),
        dict(name='Truffle Salami', description='Premium salami with truffle oil, mushrooms, and aged parmesan', category='classic', price_small=169, price_medium=209, price_large=249),
        dict(name='Tomat', description='Simple and fresh — San Marzano tomato, garlic, olive oil, and oregano', category='classic', price_small=109, price_medium=149, price_large=189),
        dict(name="Devil's Playground", description='Double pepperoni, ghost chilli sauce, and habanero for the brave', category='classic', price_small=159, price_medium=199, price_large=239),
    ]

    for p in new_pizzas:
        if not Pizza.objects.filter(name=p['name']).exists():
            Pizza.objects.create(**p)

    # Add Caprese salad side
    if not Side.objects.filter(name='Caprese Salat').exists():
        Side.objects.create(
            name='Caprese Salat',
            side_type='salad',
            description='Fresh mozzarella, ripe tomato, basil, and extra virgin olive oil',
            price=89
        )


def reverse_seed(apps, schema_editor):
    Pizza = apps.get_model('orders', 'Pizza')
    Side = apps.get_model('orders', 'Side')
    names = ['Pepperoni', 'Picante', 'Beef', 'Margherita', 'Chicken', 'Nduja',
             'Truffle Salami', 'Tomat', "Devil's Playground"]
    Pizza.objects.filter(name__in=names).delete()
    Side.objects.filter(name='Caprese Salat').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0010_update_pizza_model'),
    ]

    operations = [
        migrations.RunPython(seed_data, reverse_seed),
    ]

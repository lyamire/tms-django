from django.core.management.base import BaseCommand, CommandError
from shop.models import Product, Category
import json

class Command(BaseCommand):
    help = 'filling the shop application database with initial data'

    def add_arguments(self, parser):
        parser.add_argument('--data_file_path', type=str, required=False, default='shop/data/data.json')
        parser.add_argument('--clean_database', type=bool, required=False, default=False, help='Clean DB before import')

    def handle(self, *args, **options):
        if options['clean_database']:
            print('Remove all products and categories')
            Product.objects.all().delete()
            Category.objects.all().delete()

        print(f'Import data from {options['data_file_path']}')
        with open(options['data_file_path']) as data_file:
            data = json.load(data_file)

            print('Import categories')
            for category in data['categories']:
                old = Category.objects.get(pk=category['id'])
                if not old:
                    Category.objects.create(**category)
                else:
                    print(f'Category already exists: [{category["id"]}] {category["name"]}')

            print('Import products')
            for product in data['products']:
                old = Product.objects.get(pk=product['id'])
                if not old:
                    Product.objects.create(**product)
                else:
                    print(f'Product already exists: [{product["id"]}] {product["name"]}')

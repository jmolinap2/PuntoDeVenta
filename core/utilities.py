import string

from config import wsgi
import random
from random import randint
import json
from core.pos.models import *
from core.user.models import User

numbers = list(string.digits)

user = User()
user.username = 'admin'
user.first_name = 'Jesus Alejandro'
user.last_name = 'Molina Peñaherrera'
user.email = 'jmolinap2@unemi.edu.ec'
user.set_password('12345')
user.is_superuser = True
user.is_staff = True
user.save()
print('Usuario creado correctamente')

company = Company()
company.name = 'DIVAMED'
company.ruc = '0928363212121'
company.address = 'Duran, Ecuador'
company.mobile = '0979014552'
company.phone = '2977557'
company.website = 'https://Divamed.com'
company.save()
print('Compañia creado correctamente')


def insert_products():
    with open(f'{settings.BASE_DIR}/deploy/json/products.json', encoding='utf8') as json_file:
        data = json.load(json_file)
        for p in data['rows'][0:100]:
            row = p['value']
            category = Category.objects.filter(name=row['marca'])
            if not category.exists():
                category = Category()
                category.name = row['marca']
                category.desc = 's/n'
                category.save()
            else:
                category = category[0]
            name = row['nombre']
            while Product.objects.filter(name=name).exists():
                name = f'{name} - {randint(1, 100)}'
            p = Product()
            p.name = name
            p.category_id = category.id
            p.is_service = False
            p.pvp = randint(1, 10)
            p.stock = randint(5, 100)
            p.save()
            print(p.name)


def insert_sale():
    client = Client()
    client.names = 'Consumidor final'
    client.dni = '9999999999'
    client.address = 'Milagro, cdla. Dager avda tumbez y zamora'
    client.save()

    with open(f'{settings.BASE_DIR}/deploy/json/customers.json', encoding='utf8') as json_file:
        data = json.load(json_file)
        for item in data[0:15]:
            client = Client()
            client.names = f"{item['first']} {item['last']}"
            client.dni = f"0{''.join(random.choices(numbers, k=9))}"
            client.address = item['country']
            client.save()

    customers = list(Client.objects.all().values_list('id', flat=True))

    for i in range(1, 30):
        sale = Sale()
        sale.user_id = 1
        sale.client_id = random.choices(customers, k=1)[0]
        sale.iva = 0.12
        sale.save()
        for d in range(1, 8):
            numberList = list(Product.objects.filter(stock__gt=0).values_list(flat=True))
            detail = SaleProduct()
            detail.sale_id = sale.id
            detail.product_id = random.choice(numberList)
            while sale.saleproduct_set.filter(product_id=detail.product_id).exists():
                detail.product_id = random.choice(numberList)
            detail.cant = randint(1, detail.product.stock)
            detail.price = detail.product.pvp
            detail.subtotal = float(detail.price) * detail.cant
            detail.save()
            detail.product.stock -= detail.cant
            detail.product.save()

        sale.calculate_invoice()
        print(i)


# //insert_products()
# insert_sale()

import os
import sys
sys.path.append(os.path.abspath(os.path.join(__file__, *[os.pardir] * 3)))
os.environ['DJANGO_SETTINGS_MDDULE']= 'shopify.settings'

import django
django.setup()

import json
from customer.models import User,Customer,Address,Metafield,Collect

filepath = './dummy-data/'

with open(filepath+'customer.json') as jsonfile:
    customer = json.load(jsonfile)
    for cust in customer:
        existsUser = User.objects.filter(email=cust['email']).first()
        if existsUser == None:
            user = User.objects.create_user(username=cust['email'],email=cust['email'],
                                            password=cust['password'],
                                            first_name=cust['first_name'],
                                            last_name=cust['last_name'])
            
            existsCust = Customer.objects.filter(user=user).first()
            if existsCust == None:
                Customer.objects.create(user=user,created_at=cust['created_at'],
                                        updated_at=cust['updated_at'],
                                        state=cust['state'],note=cust['note'],
                                        verified_email=cust['verified_email'],
                                        tags=cust['tags'],currency=cust['currency'],
                                        phone=cust['phone'],marketing_opt_in_level=cust['marketing_opt_in_level'],
                                        tax_exemptions=cust['tax_exemptions'])
                
with open(filepath+'address.json') as jsonfile:
    addresses = json.load(jsonfile)
    for num, adr in enumerate(addresses):
        addrExist = Address.objects.filter(id=num+1).first()
        if addrExist == None:
            Address.objects.create(customer_id=adr['customer'],
                                   address1=adr['address1'],
                                   address2=adr['address2'],
                                   city=adr['city'],province=adr['province'],country=adr['country'],
                                   company=adr['company'],phone=adr['phone'],zip=adr['zip'],default=adr['default'])   
            
with open(filepath + 'metafield.json') as jsonfile:
    metafields = json.load(jsonfile)
    for meta in metafields:
        Metafield.objects.create(
            created_at=meta['created_at'],
            description=meta['description'],
            key=meta['key'],
            namespace=meta['namespace'],
            owner_id=meta['owner_id'],
            owner_resource=meta['owner_resource'],
            updated_at=meta['updated_at'],
            value=meta['value'],
            type=meta['type']
        )

with open(filepath + 'collects.json') as jsonfile:
    collect = json.load(jsonfile)
    for clc in collect:
        Collect.objects.create(collection_id=clc['collection_id'],created_at=clc['created_at'],
                               collect_id=clc['collect_id'],position=clc['position'],product_id=clc['product_id'],
                               sort_value=clc['sort_value'], updated_at=clc['updated_at'])
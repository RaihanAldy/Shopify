from ninja import NinjaAPI, Query
from ninja.errors import HttpError
from ninja_simple_jwt.auth.views.api import mobile_auth_router
from ninja_simple_jwt.auth.ninja_auth import HttpJwtAuth
from .models import User, Customer, Address, Metafield,Collect
from .schemas import CustomerOut, CustomerResp, AddressIn, AddressResp, AddressOut, CustomerIn, MetafieldSchema , CollectResp,CollectIn, CollectOut
from typing import List

api = NinjaAPI()
api.add_router("/auth/", mobile_auth_router)
apiAuth = HttpJwtAuth()

@api.get("hello")
def helloWorld(request):
    return {'hello': 'world'}

@api.get("customers.json", auth=apiAuth, response=CustomerResp)
def getAllCustomers(request, ids:str):
    int_ids = ids.split(',')
    customers = Customer.objects.filter(id__in=int_ids)
    return {'customers': customers}

# Single Customer
@api.get('customers/{id_cust}.json', auth=apiAuth, response=CustomerOut)
def getCustomerById(request, id_cust: int):
    customer = Customer.objects.get(pk=id_cust)
    return customer

# Searches for customers that match a supplied query
@api.get('customers/search.json', auth=apiAuth, response=CustomerResp)
def searchCustomers(request, query: str = Query(...)):
    # Extract email, etc from query string
    email_query = query.split(':')[1] if 'email:' in query else None
    first_name_query = query.split(':')[1] if 'first_name:' in query else None
    last_name_query = query.split(':')[1] if 'last_name:' in query else None

    if email_query:
        customers = Customer.objects.filter(user__email=email_query)
    elif first_name_query:
        customers = Customer.objects.filter(user__first_name=first_name_query)
    elif last_name_query:
        customers = Customer.objects.filter(user__last_name=last_name_query)

    return {'customers': customers}

# Count all Customers
@api.get('customers/count.json', auth=apiAuth)
def countCustomers(request):
    customer_count = Customer.objects.count()
    return {"customer_count": customer_count}

# Update Customer
@api.put('customers/{id_cust}.json', auth=apiAuth, response=CustomerOut)
def updateCustomer(request, id_cust: int, data: CustomerIn):
    customer = Customer.objects.get(pk=id_cust)
    user = customer.user
    
    if data.email:
        user.email = data.email
    if data.first_name:
        user.first_name = data.first_name
    if data.last_name:
        user.last_name = data.last_name
    user.save()
    
    if data.phone:
        customer.phone = data.phone
    if data.state:
        customer.state = data.state
    if data.currency:
        customer.currency = data.currency
    customer.save()
    
    return customer

# Delete Customers
@api.delete('customers/{id_cust}.json')
def deleteCust(request, id_cust:int):
    Customer.objects.get(pk=id_cust).delete()
    return {}

# Add Address
@api.post('customers/{id_cust}/addresses.json', auth=apiAuth, response=AddressResp)
def addCustomer(request, id_cust:int, data:AddressIn):
    cust = Customer.objects.get(pk=id_cust)
    newAddr = Address.objects.create(
                customer=cust,
                address1=data.address1,
                address2=data.address2,
                city=data.city,
                province=data.province,
                company=data.company,
                phone=data.phone,
                zip=data.zip
            )
    return {"customer_address": newAddr}

# Retrieves a list of addresses for a customer
@api.get('customers/{id_cust}/addresses.json', auth=apiAuth, response=List[AddressOut])
def getCustomerAddresses(request, id_cust: int):
    addresses = Address.objects.filter(customer_id=id_cust)
    return addresses

# Retrieves details for a single customer address
@api.get('customers/{id_cust}/addresses/{id_addr}.json', auth=apiAuth, response=AddressResp)
def getCustomerAddress(request, id_cust: int, id_addr: int):
    try:
        address = Address.objects.get(customer_id=id_cust, id=id_addr)
        return {"customer_address": address}
    except Address.DoesNotExist:
        raise HttpError(404, "Address not found")

# Set Default Address
@api.put('customers/{id_cust}/addresses/{id_addr}/default.json', auth=apiAuth, response=AddressResp)
def setDefaultAddr(request, id_cust:int, id_addr:int):
    addr = Address.objects.get(pk=id_addr)
    addr.default =True
    addr.save()
    other = Address.objects.filter(customer_id=id_cust).exclude(id=id_addr)
    for data in other:
        data.default = False
        data.save()

    return {"customer_address": addr}

# Delete Address
@api.delete('customers/{id_cust}/addresses/{id_addr}.json')
def deleteAddr(request, id_cust:int, id_addr:int):
    Address.objects.get(pk=id_addr).delete()
    return {}

# Update Address
@api.put('customers/{id_cust}/addresses/{id_addr}.json', auth=apiAuth, response=AddressOut)
def updateCustomerAddress(request, id_cust: int, id_addr: int, data: AddressIn):
    address = Address.objects.get(pk=id_addr, customer_id=id_cust)
    address.address1 = data.address1
    address.address2 = data.address2
    address.city = data.city
    address.province = data.province
    address.company = data.company
    address.phone = data.phone
    address.zip = data.zip
    address.save()
    return address

# Retrieve Metafields by owner_id
@api.get('blogs/{owner_id}/metafield.json', auth=apiAuth, response=List[MetafieldSchema])
def getMetafieldsByOwnerId(request, owner_id: int):
    metafields = Metafield.objects.filter(owner_id=owner_id)
    return metafields

# Count Metafields by owner_id
@api.get('blogs/{owner_id}/metafield/count.json', auth=apiAuth)
def countMetafields(request, owner_id: int):
    metafield_count = Metafield.objects.filter(owner_id=owner_id).count()
    return {"metafield_count": metafield_count}

# Retrieve a specific Metafield by owner_id and metafield_id
@api.get('blogs/{owner_id}/metafield/{metafield_id}.json', auth=apiAuth, response=MetafieldSchema)
def getMetafieldById(request, owner_id: int, metafield_id: int):
    try:
        metafield = Metafield.objects.get(owner_id=owner_id, id=metafield_id)
        return metafield
    except Metafield.DoesNotExist:
        raise HttpError(404, "Metafield not found")

# Retrieve Metafields with query parameters
@api.get('blogs/{owner_id}/metafield/search.json', auth=apiAuth, response=List[MetafieldSchema])
def searchMetafields(request, owner_id: int, query: str = Query(...)):
    
    key_query = query.split(':')[1] if 'key:' in query else None
    namespace_query = query.split(':')[1] if 'namespace:' in query else None
    description_query = query.split(':')[1] if 'description:' in query else None

    if key_query:
        metafields = Metafield.objects.filter(owner_id=owner_id, key=key_query)
    elif namespace_query:
        metafields = Metafield.objects.filter(owner_id=owner_id, namespace=namespace_query)
    elif description_query:
        metafields = Metafield.objects.filter(owner_id=owner_id, description=description_query)
    else:
        metafields = Metafield.objects.filter(owner_id=owner_id)

    return metafields

# Update Metafields
@api.put('blogs/{owner_id}/metafield/{metafield_id}.json', auth=apiAuth, response=MetafieldSchema)
def updateMetafields(request, owner_id: int, data: MetafieldSchema):
    metafields = Metafield.objects.get(pk=owner_id)
    metafields.description = data.description
    metafields.key = data.key
    metafields.namespace = data.namespace
    metafields.province = data.province
    metafields.save()
    return metafields

# Delete Metafields
@api.delete('blogs/{owner_id}/metafield/{metafield_id}.json')
def deleteMetafields(request, owner_id:int):
    Metafield.objects.get(pk=owner_id).delete()
    return {}

# add Collect 
@api.post('collects.json', auth=apiAuth, response=CollectResp)
def addCollect(request, collect_id:int, data:CollectIn):
    newclc = Collect.objects.create(
                collect_id=data.collect_id,
                collction_id=data.colllection_id,
                product_id=data.product_id,
                position=data.position,
                sort_value=data.sort_value,
            )
    return {"customer_collect": newclc}

# Retrieves a list of Collects
@api.get('collects.json', auth=apiAuth, response=List[CollectOut])
def getCollect(request, collect_id: int):
    clc = Collect.objects.filter(collect_id=collect_id)
    return clc

# Retrieves a Count of Collect
@api.get('collects/count.json', auth=apiAuth)
def countCollect(request, collect_id: int):
    collect_count = Collect.objects.filter(collect_id=collect_id).count()
    return {"collect_count": collect_count}

# Delete collect
@api.delete('collects/{collect_id}.json')
def deleteCollect(request, collect_id:int):
    Collect.objects.get(pk=collect_id).delete()
    return {}
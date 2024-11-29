# coding: utf-8
import xmlrpclib
import xlrd
import glob
import base64
import datetime
import base64
print("\nstart time:",datetime.datetime.today())

dbname = "demo.alburuuj.group"
username = 'admin'
pwd = 'buruuj123'
sock_common = xmlrpclib.ServerProxy('http://165.232.139.10:8069/xmlrpc/common')
print("sock common \n\n",sock_common)
sock = xmlrpclib.ServerProxy('http://165.232.139.10:8069/xmlrpc/object')
print("sock \n\n",sock)
uid = sock_common.login(dbname, username, pwd)
print("uid \n\n",uid)
work_book = xlrd.open_workbook("/home/jatin/workspace/15.0/mrp_production_2024_records.xls")

print("work_book \n\n",work_book)

created_production = []
today = datetime.datetime.today().date()
print ('-----------today--------------',today)

from datetime import datetime, timedelta

def excel_serial_to_date(serial):

    start_date = datetime(1899, 12, 30) + timedelta(days=serial)
    return start_date.strftime("%Y-%m-%d %H:%M:%S")

last_prod_id = None

# products = sock.execute_kw(dbname, uid, pwd, 'product.product', 'search', [[]], {'fields': ['name', 'default_code']})
# product_by_name = {p['name'] + '----' + p['default_code']: p['id'] for p in products}

# print(product_by_name)

for sheet in work_book._sheet_list:
    sheet_values = sheet._cell_values
    cnt = 0
    for sheet_data in sheet_values[1:]:
        prod_ref = sheet_data[4].encode('utf-8')
        #cnt <= 4214 or 
        if cnt <=345 or prod_ref == 'GravelallTypes2':
            print ("cnt", cnt, sheet_data[1].encode('utf-8'))
            cnt +=1 
            continue
        cnt +=1
        reference = sheet_data[1].encode('utf-8')
        schedule_date = sheet_data[2]
        product = sheet_data[3].encode('utf-8')
        
        p_uom = sheet_data[5].encode('utf-8')
        quantity_to_produce = sheet_data[6]
        responsible = sheet_data[7].encode('utf-8')
        bom_ref = sheet_data[8].encode('utf-8')
        
        com_product = sheet_data[9].encode('utf-8')
        com_product_ref = sheet_data[10].encode('utf-8')
        com_uom = sheet_data[11].encode('utf-8')
        com_demand = sheet_data[12]
        com_display_name = sheet_data[13].encode('utf-8')
        com_dest_location = sheet_data[15].encode('utf-8')
        bom = sheet_data[16].encode('utf-8')

        if isinstance(schedule_date, (int, float)):
            schedule_date = excel_serial_to_date(schedule_date)
        else:
            schedule_date = schedule_date

        # print("=====schedule_date=\n\n",schedule_date)

        product_id = sock.execute_kw(dbname, uid, pwd, 'product.product', 'search', [[('display_name', '=', product),('default_code','=',prod_ref)]])
        product_id = product_id[0] if product_id else False
        # product_id = product_by_name.get(product + '----' + prod_ref) or False

        product_uom_id = sock.execute_kw(dbname, uid, pwd, 'uom.uom', 'search', [[('name', '=', p_uom)]])
        product_uom_id = product_uom_id[0] if product_uom_id else False

        bom_id = sock.execute_kw(dbname, uid, pwd, 'mrp.bom', 'search', [[('product_tmpl_id.display_name', '=', bom),('code','=',bom_ref)]])
        bom_id = bom_id[0] if bom_id else False

        user_id = sock.execute_kw(dbname, uid, pwd, 'res.users', 'search', [[('name', '=', responsible)]])
        user_id = user_id[0] if user_id else False


        # print("======product=====\n", product_id, product_uom_id,bom_id,user_id)

        # try:
        if product_id and reference:
            production_id = sock.execute_kw(dbname, uid, pwd, 'mrp.production', 'create', [{
                'name': reference,
                'product_id': product_id,
                'product_qty': float(quantity_to_produce),
                'user_id': user_id,
                'date_planned_start': schedule_date,
                'product_uom_id': product_uom_id,
                'bom_id': bom_id,
                'state': 'draft',
            }])
            last_prod_id = production_id
            # print ('------------------production_id----------------------',production_id)

        com_product_id = sock.execute_kw(dbname, uid, pwd, 'product.product', 'search', [[('display_name', '=', com_product),('default_code','=',com_product_ref)]])
        com_product_id = com_product_id[0] if com_product_id else False

        product = sock.execute_kw(dbname, uid, pwd, 'product.product', 'read', [com_product_id], {'fields': ['uom_id']})
        com_uom_id = product[0]['uom_id'][0] if product else False

        # print ('---------com_demand------------------',com_demand,com_product_id,com_product,com_uom_id)
        if last_prod_id and com_product_id:
            raw_materials = [(0, 0, {
                'product_id': com_product_id,
                'product_uom_qty': com_demand,
                'product_uom': com_uom_id,
                'name': com_display_name,
                'raw_material_production_id':last_prod_id,
                'location_id': 122,
                'location_dest_id':122,
            })]

            sock.execute_kw(dbname, uid, pwd, 'mrp.production', 'write', [last_prod_id, {
                'move_raw_ids': raw_materials
            }])

            print("Production order created with ID",reference,last_prod_id,cnt)
            created_production.append(last_prod_id)

print("Created production orders:", created_production)
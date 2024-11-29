# coding: utf-8
import xmlrpclib
import xlrd
import datetime

print("\nstart time:", datetime.datetime.today())

# Odoo connection details
dbname = "your_database_name"
username = 'your_username'
pwd = 'your_password'
url = 'https://your_instance.odoo.com'

# Connect to Odoo
sock_common = xmlrpclib.ServerProxy(f'{url}/xmlrpc/common')
sock = xmlrpclib.ServerProxy(f'{url}/xmlrpc/object')
uid = sock_common.login(dbname, username, pwd)
print("uid \n\n", uid)

# Open the Excel workbook
workbook_path = "/path/to/your/excel_file.xlsx"
work_book = xlrd.open_workbook(workbook_path)
print("work_book \n\n", work_book)

def find_or_create_product(product_name):
    product_ids = sock.execute_kw(dbname, uid, pwd, 'product.product', 'search', [[('name', '=', product_name)]])
    if product_ids:
        return product_ids[0]
    else:
        # Create new product if not found (example, adjust fields as needed)
        product_id = sock.execute_kw(dbname, uid, pwd, 'product.product', 'create', [{
            'name': product_name,
            'type': 'product',  # or 'consu', 'service' based on your needs
            'uom_id': sock.execute_kw(dbname, uid, pwd, 'uom.uom', 'search', [[('name', '=', 'Unit')]])[0],  # Adjust unit of measure
            'uom_po_id': sock.execute_kw(dbname, uid, pwd, 'uom.uom', 'search', [[('name', '=', 'Unit')]])[0],  # Adjust unit of measure
        }])
        return product_id

def import_data_from_excel():
    created_production = []
    
    for sheet in work_book.sheets():
        sheet_values = sheet.get_rows()
        for row_idx, row_data in enumerate(sheet_values):
            if row_idx == 0:  # Skip header row
                continue
            
            try:
                # Read data from the row
                reference = row_data[2].value.encode('utf-8')
                product_name = row_data[3].value.encode('utf-8')
                responsible = row_data[4].value.encode('utf-8')
                p_uom = row_data[5].value.encode('utf-8')
                schedule_date = xlrd.xldate.xldate_as_datetime(row_data[6].value, work_book.datemode)
                quantity_to_produce = row_data[7].value
                bom = row_data[8].value
                com_product = row_data[9].value.encode('utf-8')
                com_demand = row_data[10].value
                com_uom = row_data[11].value.encode('utf-8')

                # Find or create product
                product_id = find_or_create_product(product_name)

                # Create production order
                production_id = sock.execute_kw(dbname, uid, pwd, 'mrp.production', 'create', [{
                    'name': reference,
                    'product_id': product_id,
                    'product_qty': quantity_to_produce,
                    'product_uom_id': sock.execute_kw(dbname, uid, pwd, 'uom.uom', 'search', [[('name', '=', p_uom)]])[0],  # Adjust unit of measure
                    'date_planned_start': schedule_date,
                    'bom_id': bom,  # Ensure BOM ID is correctly set
                    'state': 'draft',
                }])

                # Add raw materials to move_raw_ids
                raw_materials = []
                com_product_id = find_or_create_product(com_product)
                raw_materials.append((0, 0, {
                    'product_id': com_product_id,
                    'product_qty': com_demand,
                    'product_uom_id': sock.execute_kw(dbname, uid, pwd, 'uom.uom', 'search', [[('name', '=', com_uom)]])[0],  # Adjust unit of measure
                }))

                sock.execute_kw(dbname, uid, pwd, 'mrp.production', 'write', [production_id, {
                    'move_raw_ids': raw_materials
                }])

                print(f"Production order {reference} created with ID {production_id}")
                created_production.append(production_id)
            except Exception as e:
                print(f"Error processing row {row_idx}: {e}")
    
    print("Created production orders:", created_production)

import_data_from_excel()

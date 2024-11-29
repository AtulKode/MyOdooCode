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
work_book = xlrd.open_workbook("/home/jatin/Downloads/final.xls")

print("work_book \n\n",work_book)

created_invoices = []
today = datetime.datetime.today().date()
print ('-----------today--------------',today)

from datetime import datetime, timedelta

def excel_serial_to_date(serial):

    start_date = datetime(1899, 12, 30) + timedelta(days=serial)
    return start_date.strftime("%Y-%m-%d")

last_inv_id = None

for sheet in work_book._sheet_list:
    sheet_values = sheet._cell_values
    cnt = 0
    for sheet_data in sheet_values[1:]:
        
        if cnt <=1437:
            print("=====cot====",cnt)
            cnt +=1
            continue
        # elif cnt == 1260:
        #     break
        # print("=====cot==new===",cnt)
        cnt +=1
        number = sheet_data[1].encode('utf-8')
        partner = sheet_data[2].encode('utf-8')
        bill_date = sheet_data[3]
        due_date = sheet_data[4]
        inv_prod = sheet_data[5].encode('utf-8')
        inv_qty = sheet_data[6]
        inv_unit_price = sheet_data[7]
        # inv_uom = sheet_data[8].encode('utf-8')
        
        inv_account = sheet_data[9].encode('utf-8').split(" ")[0]
        inv_code = sheet_data[9].encode('utf-8').split(" ")[1]
        journal = sheet_data[10].encode('utf-8')
        payment_ref = sheet_data[11].encode('utf-8')
        sales_person = sheet_data[12].encode('utf-8')
        sales_team = sheet_data[13].encode('utf-8')
        type_name = sheet_data[14].encode('utf-8')

        

        if isinstance(due_date, (int, float)):
            # bill_date = excel_serial_to_date(bill_date)
            due_date = excel_serial_to_date(due_date)
            bill_date = due_date
        else:
            bill_date = due_date
            due_date = due_date
        print ('--------created----partner id -------',due_date,bill_date,number)

        partner_id = sock.execute_kw(dbname, uid, pwd, 'res.partner', 'search', [[('name', '=', partner)]])
        partner_id = partner_id[0] if partner_id else False
        if not partner_id and partner:
            partner_id = sock.execute_kw(dbname, uid, pwd, 'res.partner', 'create', [{
                            'name': partner
                        }])
            print ('--------created----partner id -------',partner_id)

        inv_product_id = sock.execute_kw(dbname, uid, pwd, 'product.product', 'search', [[('name', '=', inv_prod)]])
        inv_product_id = inv_product_id[0] if inv_product_id else False

        inv_uom = sock.execute_kw(dbname, uid, pwd, 'product.product', 'read', [inv_product_id], {'fields': ['uom_id']})
        inv_uom_id = inv_uom[0]['uom_id'][0] if inv_uom else False
        user_type_id = sock.execute_kw(dbname, uid, pwd, 'account.account.type', 'search', [[('name', '=', type_name)]])[0]
        
        inv_account_id = sock.execute_kw(dbname, uid, pwd, 'account.account', 'search', [[('code', '=', inv_account)]])

        inv_account_id = inv_account_id[0] if inv_account_id else False

        if not inv_account_id and sheet_data[9]:
            inv_account_id = sock.execute_kw(dbname, uid, pwd, 'account.account', 'create', [{
                            'name': inv_code,
                            'code' : inv_account,
                            'user_type_id':user_type_id,
                        }])           
            print ('--------created----inv_account_id id -------',inv_account_id)
        journal_id = sock.execute_kw(dbname, uid, pwd, 'account.journal', 'search', [[('name', '=', journal)]])
        journal_id = journal_id[0] if journal_id else False

        team_id = sock.execute_kw(dbname, uid, pwd, 'crm.team', 'search', [[('name', '=', sales_team)]])
        team_id = team_id[0] if team_id else False

        context = {'check_move_validity': False}
        print ('------------partner id -------',partner_id,last_inv_id,sheet_data[1],sheet_data[2])
        if partner_id and sheet_data[1] and sheet_data[2]:
            invoice_id = sock.execute_kw(dbname, uid, pwd, 'account.move', 'create', [{
                'name': number,
                'partner_id': partner_id,
                'move_type': 'out_invoice',
                'payment_reference': payment_ref,
                'invoice_date': bill_date,
                'invoice_date_due': due_date,
                'journal_id': journal_id,
                'team_id': team_id,
            }])
            last_inv_id = invoice_id
        if last_inv_id and inv_product_id:
            vals = {
                        'product_id': inv_product_id,
                        'account_id': inv_account_id,
                        'quantity': inv_qty,
                        'product_uom_id': inv_uom_id,
                        'move_id':last_inv_id,
                        'price_unit': inv_unit_price,
                        'date_maturity': False,
                        }
            move_line = sock.execute_kw(dbname, uid, pwd, 'account.move.line', 'create', [vals], {'context': context})

            print("Invoice created with ID==count",last_inv_id,cnt)
            created_invoices.append(last_inv_id)
print("Created Invoices:", created_invoices)
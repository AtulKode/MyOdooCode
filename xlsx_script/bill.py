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
work_book = xlrd.open_workbook("/home/jatin/Downloads/bill.xls")

print("work_book \n\n",work_book)

created_bills = []
today = datetime.datetime.today().date()
print ('-----------today--------------',today)

from datetime import datetime, timedelta

def excel_serial_to_date(serial):

    start_date = datetime(1899, 12, 30) + timedelta(days=serial)
    return start_date.strftime("%Y-%m-%d")

last_bill_id = False
inv_product_id = False
inv_uom_id = False
journal_id = False
for sheet in work_book._sheet_list:
    sheet_values = sheet._cell_values
    cnt = 0
    for sheet_data in sheet_values[1:]:
        
        if cnt <=3060:
            print("=====cot====",cnt, sheet_data[1].encode('utf-8') if sheet_data[1] else None)
            cnt +=1
            continue
        cnt +=1
        number = sheet_data[0].encode('utf-8') if sheet_data[0] else None
        partner = sheet_data[1].encode('utf-8') if sheet_data[1] else None
        print ("partner==>", partner)
        ref = sheet_data[2].encode('utf-8') if sheet_data[2] else None
        # pay_ref = sheet_data[3].encode('utf-8') if sheet_data[3] else None

        bill_date = sheet_data[4]
        due_date = sheet_data[5]
        journal = sheet_data[6].encode('utf-8') if sheet_data[6] else None

        inv_prod = sheet_data[7].encode('utf-8') if sheet_data[7] else None
        inv_prod_label = sheet_data[8].encode('utf-8') if sheet_data[8] else None
        inv_qty = sheet_data[9]
        inv_unit_price = sheet_data[10]
        inv_code = sheet_data[12].encode('utf-8') if sheet_data[12] else None
        type_name = sheet_data[13].encode('utf-8') if sheet_data[13] else None
        
        inv_account_name = sheet_data[14].encode('utf-8') if sheet_data[14] else None


        

        if isinstance(due_date, (int, float)):
            due_date = excel_serial_to_date(bill_date)
            bill_date = due_date
        else:
            bill_date = bill_date
            due_date = due_date
        print ('--------created----partner id -------',due_date,bill_date,number,partner,inv_prod)
        if partner is not None and sheet_data[1]:
            partner_id = sock.execute_kw(dbname, uid, pwd, 'res.partner', 'search', [[('name', '=', partner)]])
            partner_id = partner_id[0] if partner_id else False
        if not partner_id and partner:
            partner_id = sock.execute_kw(dbname, uid, pwd, 'res.partner', 'create', [{
                            'name': partner
                        }])
            print ('--------created----partner id -------',partner_id)
        if inv_prod is not None and sheet_data[7]:
            inv_product_id = sock.execute_kw(dbname, uid, pwd, 'product.product', 'search', [[('name', '=', inv_prod)]])
            inv_product_id = inv_product_id[0] if inv_product_id else False
            print ('--------created----inv_product_id id -------',inv_product_id)
            inv_uom = sock.execute_kw(dbname, uid, pwd, 'product.product', 'read', [inv_product_id], {'fields': ['uom_id']})
            inv_uom_id = inv_uom[0]['uom_id'][0] if inv_uom else False
        user_type_id = sock.execute_kw(dbname, uid, pwd, 'account.account.type', 'search', [[('name', '=', type_name)]])[0]
        
        inv_account_id = sock.execute_kw(dbname, uid, pwd, 'account.account', 'search', [[('code', '=', inv_code)]])

        inv_account_id = inv_account_id[0] if inv_account_id else False

        if not inv_account_id and sheet_data[14]:
            inv_account_id = sock.execute_kw(dbname, uid, pwd, 'account.account', 'create', [{
                            'name': inv_account_name,
                            'code' : inv_code,
                            'user_type_id':user_type_id,
                        }])           
            print ('--------created----inv_account_id id -------',inv_account_id)
        if journal is not None and sheet_data[6]:
            journal_id = sock.execute_kw(dbname, uid, pwd, 'account.journal', 'search', [[('name', '=', journal)]])
            journal_id = journal_id[0] if journal_id else False


        context = {'check_move_validity': False}
        if partner_id and sheet_data[1] and sheet_data[2]:
            invoice_id = sock.execute_kw(dbname, uid, pwd, 'account.move', 'create', [{
                'name': number,
                'partner_id': partner_id,
                'move_type': 'in_invoice',
                'ref' : ref,
                'payment_reference': ref,
                'date': bill_date,
                'invoice_date': bill_date,
                'invoice_date_due': due_date,
                'journal_id': journal_id,
            }])
            last_bill_id = invoice_id
        if last_bill_id or inv_prod_label:
            vals = {
                        'product_id': inv_product_id or False,
                        'name' : inv_prod_label or False,
                        'account_id': inv_account_id or False,
                        'quantity': inv_qty,
                        'product_uom_id': inv_uom_id or False,
                        'move_id':last_bill_id,
                        'price_unit': inv_unit_price,
                        'date_maturity': False,
                        }
            move_line = sock.execute_kw(dbname, uid, pwd, 'account.move.line', 'create', [vals], {'context': context})

            print("Invoice created with ID==count",last_bill_id,cnt)
            created_bills.append(last_bill_id)
print("Created created_bills:", created_bills)
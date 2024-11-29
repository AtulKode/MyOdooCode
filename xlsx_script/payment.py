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
work_book = xlrd.open_workbook("/home/jatin/Downloads/payment_method.xls")

print("work_book \n\n",work_book)

# created_production = []
today = datetime.datetime.today().date()
print ('-----------today--------------',today)

from datetime import datetime, timedelta

def excel_serial_to_date(serial):

    start_date = datetime(1899, 12, 30) + timedelta(days=serial)
    return start_date.strftime("%Y-%m-%d")

pay_type_map = {
    "Send": "outbound",
    "Receive": "inbound"
}

paymnent_method = {
    "Check" : "ck",
    "Cash" : "cs"
}

created_payment = []
for sheet in work_book._sheet_list:
    sheet_values = sheet._cell_values
    cnt = 0
    # order_ref_list = []
    # completed_ref = []
    for sheet_data in sheet_values[1:]:
        if cnt <=102:
            cnt += 1
            continue
        # if cnt == 109:
        #     break
        cnt += 1
        date = sheet_data[0]
        number = sheet_data[1].encode('utf-8') if sheet_data[1] else False
        journal = sheet_data[2].encode('utf-8') if sheet_data[2] else False
        pay_method = sheet_data[3].encode('utf-8') if sheet_data[3] else False
        pay_type = sheet_data[4].encode('utf-8') if sheet_data[4] else False
        cust_vendor = sheet_data[5].encode('utf-8') if sheet_data[5] else False
        amount = sheet_data[6]
        currency = sheet_data[7].encode('utf-8') if sheet_data[7] else False
        voucher_no = sheet_data[8].encode('utf-8') if sheet_data[8] else False
        check_no = sheet_data[9].encode('utf-8') if sheet_data[9] else False
        destina_acc_name = sheet_data[10].encode('utf-8') if sheet_data[10] else False
        destina_acc_code = sheet_data[11].encode('utf-8') if sheet_data[11] else False
        ref = sheet_data[12].encode('utf-8') if sheet_data[12] else False
        # journa_entry_num = sheet_data[13].encode('utf-8') if sheet_data[13] else False
        # journa_item_acc = sheet_data[14].encode('utf-8') if sheet_data[14] else False
        receipent_acc = sheet_data[13].encode('utf-8') if sheet_data[13] else False
        payment_method = sheet_data[14].encode('utf-8') if sheet_data[14] else False

        # print("=sheet+data===",number,journal)
        if isinstance(date, (int, float)):
            date = excel_serial_to_date(date)
        else:
            date = date
        partner_id = sock.execute_kw(dbname, uid, pwd, 'res.partner', 'search', [[('name', '=', cust_vendor)]])
        if partner_id:
            partner_id = partner_id[0]
        else:
            partner_id = sock.execute_kw(dbname, uid, pwd, 'res.partner', 'create', [{'name': cust_vendor}])
            # print("==created pertner id===",partner_id)

        dest_acc_id = sock.execute_kw(dbname, uid, pwd, 'account.account', 'search', [[('code', '=', destina_acc_code)]])
        dest_acc_id = dest_acc_id[0] if dest_acc_id else False

        journal_id = sock.execute_kw(dbname, uid, pwd, 'account.journal', 'search', [[('name', '=', journal)]])
        journal_id = journal_id[0] if journal_id else False

        partner_bank_id = sock.execute_kw(dbname, uid, pwd, 'res.partner.bank', 'search', [[('acc_number', '=', receipent_acc)]])
        partner_bank_id = partner_bank_id[0] if partner_bank_id else False

        print("==search data===\n\n",partner_id,dest_acc_id,journal_id,partner_bank_id,date, cnt)

        if sheet_data[1] and number:
            payment_id = sock.execute_kw(dbname, uid, pwd, 'account.payment', 'create', [{
                'name': number,
                'partner_id': partner_id,
                'destination_account_id': dest_acc_id,
                'payment_type': pay_type_map[pay_type] if pay_type else False,
                'amount': amount,
                'date': date,
                'ref': ref,
                'journal_id': journal_id,
                'Vocher_number': voucher_no,
                'payment_Method': paymnent_method[payment_method] if payment_method else False,
                'partner_bank_id' : partner_bank_id,
            }])
            created_payment.append(payment_id)
            print("===created=====payment id ======",number,cnt)
print("=======created payments=ids=====",created_payment)
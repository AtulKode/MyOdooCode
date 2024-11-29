from datetime import datetime
import xmlrpclib
import xlrd

print("\nstart time:", datetime.today())

dbname = 'v15_zkteko'
username = 'admin'
pwd = 'admin'

sock_common = xmlrpclib.ServerProxy('http://0.0.0.0:9000/xmlrpc/common')
sock = xmlrpclib.ServerProxy('http://0.0.0.0:9000/xmlrpc/object')
uid = sock_common.login(dbname, username, pwd)
print("***************15******************", uid)

work_book = xlrd.open_workbook("/home/jatin/Downloads/HQ Attendnce.xls")

date_format = "%m/%d/%Y"
time_format = "%H:%M"

created_log = []
cnt = 0
for sheet in work_book.sheets():
    sheet_values = sheet._cell_values
    for sheet_data in sheet_values[1:]:
        cnt +=1
        emp_no = sheet_data[0].encode('utf-8')
        emp_name = sheet_data[1].encode('utf-8')
        date_str = sheet_data[2].encode('utf-8')
        duty = sheet_data[3].encode('utf-8')

        print("===emp_no=====", emp_no, emp_name, date_str, duty)
        if cnt % 2 == 0:
            checkin = duty
        checkout = duty

        print("==checkin=", checkin)
        print("==checkout=", checkout)
        emp_id = sock.execute_kw(dbname, uid, pwd, 'hr.employee', 'search', [[('name', '=', emp_name)]])
        emp_id = emp_id[0] if emp_id else False
        if not emp_id:
            emp_id = sock.execute_kw(dbname, uid, pwd, 'hr.employee', 'create', [{
                            'name': emp_name
                        }])

        # biometric_attendance_devices_id = sock.execute_kw(dbname, uid, pwd, 'biometric.attendance.devices',
        #                                                   'search_read',
        #                                                   [[('biometric_attendance_id', '=', emp_no),('employee_id','=', emp_name)]],
        #                                                   {
        #                                                       'fields': [
        #                                                           'employee_id'
        #                                                       ]})
        # if not biometric_attendance_devices_id:
        #     biometric_attendance_devices_id = sock.execute_kw(dbname, uid, pwd, 'biometric.attendance.devices', 'create', [{
        #                     'biometric_attendance_id': emp_no,
        #                     'employee_id': emp_id,
        #                     'device_id': "111"
        #                 }])            

        # print("===biometric_attendance_devices_id==",biometric_attendance_devices_id)
        # if biometric_attendance_devices_id:
        #     all_ready_id = sock.execute_kw(dbname, uid, pwd, 'attendance.log', 'search',
        #                           [('employee_id', '=', biometric_attendance_devices_id[0].get('employee_id')[0])])
        #     emp_val = {
        #             'check_in_time': checkin,
        #             'check_out_time': checkout,
        #             'punching_time': date_punch,
        #             'status': '1'
        #         }
        #     log_id = sock.execute_kw(dbname, uid, pwd, 'attendance.log', 'write', all_ready_id[0] , emp_val)
        #     print("==log_id updated==",log_id)
        if emp_id:
            print("==emp_id==",emp_id)
            attendance_log_id = sock.execute_kw(dbname, uid, pwd, 'attendance.log', 'create', [{
                    'employee_id': emp_id,
                    'punching_time': date_punch,
                    'check_in_time': checkin,
                    'check_out_time': checkout,
                    'device': '1236547',
                }])
            print("=====log created with id====",attendance_log_id)
            created_log.append(attendance_log_id)

print("====created_log====",created_log)

from odoo import api, fields, models
from io import BytesIO
import xlsxwriter


class PurchaseOrderXlsx(models.AbstractModel):
    _name = 'report.do_report_xlsx_po.report_purchase_order_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    @api.model
    def generate_xlsx_report(self, workbook, data, orders):
        # Create a worksheet
        worksheet = workbook.add_worksheet('Purchase Orders')

        # Define cell formats
        bold_format = workbook.add_format({'bold': True})
        headers_format = workbook.add_format({'bold': True, 'bg_color': '#00FF00', 'align': 'center'})

        # Write headers
        headers = [
            'Type of PO', 'PO No', 'PO Date', 'Vendor Code', 'Vendor Name', 'Sales Employee Name',
            'Contact Person', 'Telephone 1', 'Row No', 'Item/Service Description', 'Quantity',
            'UOM', 'Row Requested Delivery Date', 'Row Estimated Delivery Date'
        ]
        for col, header in enumerate(headers):
            worksheet.write(0, col, header, headers_format)

        # Write data rows
        row = 1
        for order in orders:
            worksheet.write(row, 1, order.name if hasattr(order, 'name') else '')
            worksheet.write(row, 5, order.origin if hasattr(order.origin, 'origin') else '')
            worksheet.write(row, 6, order.partner_id if hasattr(order, 'contact_person') else '')
            worksheet.write(row, 7, order.telephone_1 if hasattr(order, 'telephone_1') else '')
            worksheet.write(row, 8, order.row_no if hasattr(order, 'row_no') else '')
            worksheet.write(row, 9, order.item_description if hasattr(order, 'item_description') else '')
            worksheet.write(row, 10, order.quantity if hasattr(order, 'quantity') else '')
            worksheet.write(row, 11, order.uom if hasattr(order, 'uom') else '')
            row += 1

        # Auto-adjust column widths
        for col, header in enumerate(headers):
            worksheet.set_column(col, col, len(header) * 1.2)

        return BytesIO()

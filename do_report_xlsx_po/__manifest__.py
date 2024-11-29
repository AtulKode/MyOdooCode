
{
    "name": "Purchase Order Xlsx Report",
    "summary": "This module create purchase order xlsx report",
    "author": "doincredible",
    "website": "",
    "category": "Reporting",
    "version": "16.0.0.0",
    
    "external_dependencies": {"python": ["xlsxwriter", "xlrd"]},
    "depends": ["purchase",'report_xlsx'],
    "data": [
        "views/report_purchase_order_xlsx.xml",
    ],

    "license": "AGPL-3",
    "installable": True,

}

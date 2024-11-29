# -*- coding: utf-8 -*-
################################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2023-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author:  Mruthul Raj (odoo@cybrosys.com)
#
#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
{
    'name': "Approval Dashboard",
    'version': '17.0.1.0.1',
    'category': 'Extra Tools',
    'summary': """Get a visual report of CRM through a Dashboard in CRM """,
    'description': """CRM dashboard module brings a multipurpose graphical
     dashboard for CRM module and making the relationship management 
     better and easier""",
    'author': 'Cybrosys Techno Solutions',
    'company': 'Cybrosys Techno Solutions',
    'maintainer': 'Cybrosys Techno Solutions',
    'website': "https://www.cybrosys.com",
    'depends': ['approval_custom','approvals'],
    'data': [
        'views/crm_team_views.xml',
             # 'views/res_users_views.xml',
             # 'views/utm_campaign_views.xml',
             ],
    'assets': {
        'web.assets_backend': [
            'approval_dashboard/static/src/css/dashboard.css',
            'approval_dashboard/static/src/css/style.scss',
            'approval_dashboard/static/src/css/material-gauge.css',
            'approval_dashboard/static/src/js/crm_dashboard.js',
            'approval_dashboard/static/src/js/lib/highcharts.js',
            'approval_dashboard/static/src/js/lib/Chart.bundle.js',
            'approval_dashboard/static/src/js/lib/funnel.js',
            'approval_dashboard/static/src/js/lib/d3.min.js',
            'approval_dashboard/static/src/js/lib/material-gauge.js',
            'approval_dashboard/static/src/js/lib/columnHeatmap.min.js',
            'approval_dashboard/static/src/js/lib/columnHeatmap.js',
            'approval_dashboard/static/src/xml/dashboard_templates.xml',
            "https://cdnjs.cloudflare.com/ajax/libs/html2canvas/0.4.1/html2canvas.min.js",
            "https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js",
        ],
    },
    'images': ['static/description/banner.jpg'],
    'license': 'AGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
}

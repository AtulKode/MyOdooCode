# Part of Odoo. See LICENSE file for full copyright and licensing details.

from lxml import html

import odoo
import odoo.modules.registry
from odoo import http
from odoo.http import request
from odoo.service import db
from odoo.tools.misc import file_open
from odoo.tools.translate import _

from odoo.addons.web.controllers.database import Database
from odoo.addons.base.models.ir_qweb import render as qweb_render


DBNAME_PATTERN = '^[a-zA-Z0-9][a-zA-Z0-9_.-]+$'

class Debrand(Database):

    def _render_template(self, **d):

        d.setdefault('manage', True)
        d['insecure'] = odoo.tools.config.verify_admin_password('admin')
        d['list_db'] = odoo.tools.config['list_db']
        d['langs'] = odoo.service.db.exp_list_lang()
        d['countries'] = odoo.service.db.exp_list_countries()
        d['pattern'] = DBNAME_PATTERN
        # databases list
        try:
            d['databases'] = http.db_list()
            d['incompatible_databases'] = odoo.service.db.list_db_incompatible(d['databases'])
        except odoo.exceptions.AccessDenied:
            d['databases'] = [request.db] if request.db else []

        templates = {}

        with file_open("do_odoo_debranding/views/database_manager_extended.qweb.html", "r") as fd:
            templates['database_manager'] = fd.read()
        with file_open("web/static/src/public/database_manager.master_input.qweb.html", "r") as fd:
            templates['master_input'] = fd.read()
        with file_open("web/static/src/public/database_manager.create_form.qweb.html", "r") as fd:
            templates['create_form'] = fd.read()

        def load(template_name):
            fromstring = html.document_fromstring if template_name == 'database_manager' else html.fragment_fromstring
            return (fromstring(templates[template_name]), template_name)

        return qweb_render('database_manager', d, load)
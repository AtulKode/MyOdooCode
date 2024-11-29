from odoo import http
from odoo.addons.web.controllers.binary import Binary
from odoo.http import request
import sass

class ColourCode(Binary):

    @http.route('/web/content', type='http', auth="public")
    def content(self, xmlid=None, model='ir.attachment', id=None, field='datas', unique=None, filename=None, mimetype=None, download=None, data=None, token=None):
        if model == 'ir.attachment' and field == 'content' and xmlid == 'do_odoo_debranding.btn.variable':
            dynamic_brand_primary_color = request.env['res.config.settings'].sudo().get_values()['dynamic_brand_primary_color']
            print("colour dynamic \n\n",dynamic_brand_primary_color)
            if dynamic_brand_primary_color:
                scss_content = """
                    $dynamic_brand_primary_color: %s;
                    %s
                """ % (dynamic_brand_primary_color, request.env.ref('do_odoo_debranding.btn.variable').data.decode('utf-8'))
                css = sass.compile(string=scss_content)
                return request.make_response(css, [('Content-Type', 'text/css')])
        return super(ColourCode, self).content(xmlid, model, id, field, unique, filename, mimetype, download, data, token)

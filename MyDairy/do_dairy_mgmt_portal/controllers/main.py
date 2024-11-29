import logging
import werkzeug
import base64
from odoo import http, tools, _
from odoo.addons.web.controllers.home import LOGIN_SUCCESSFUL_PARAMS
from odoo.exceptions import UserError
from odoo.http import request
from werkzeug.exceptions import BadRequest
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
_logger = logging.getLogger(__name__)

LOGIN_SUCCESSFUL_PARAMS.add('account_created')


class DairySignupHome(AuthSignupHome):

    def get_auth_signup_config(self):
        """retrieve the module config (which features are enabled) for the login page"""

        get_param = request.env['ir.config_parameter'].sudo().get_param
        return {
            'disable_database_manager': not tools.config['list_db'],
            'signup_enabled': request.env['res.users']._get_signup_invitation_scope() == 'b2c',
            'reset_password_enabled': get_param('auth_signup.reset_password') == 'True',
            'dairy_signup' : get_param("base.dairy_signup")
        }

    @http.route('/web/signup', type='http', auth='public', website=True, sitemap=False)
    def web_auth_signup(self, *args, **kw):
    	qcontext = self.get_auth_signup_qcontext()
    	if not qcontext.get('token') and not qcontext.get('signup_enabled'):
    		raise werkzeug.exceptions.NotFound()
    	if not qcontext.get('dairy_signup'):
    		response = super(DairySignupHome, self).web_auth_signup(*args, **kw)
    		return response
    	return request.redirect('/dairy/route')
    	
    @http.route('/dairy/route', type='http', auth="public", website=True)
    def handle_form_submission(self, **post):
        response = request.render('do_dairy_mgmt_portal.dairy_info')
        return response

    @http.route('/dairy/signup/data', type='http', auth="public", website=True, methods=['POST'], csrf=False)
    def dairy_data(self, **kwargs):
        # print("kwargs value === \n\n\n",kwargs,"\n\n\n")
        # created user obj
        user_obj = request.env['res.users']

        #created dairy object
        dairy_obj = request.env['milk.dairy']

        # Getting owner info from website
        owner_name = kwargs.get('owner_name')
        owner_address = kwargs.get('owner_address')
        owner_contact = kwargs.get('contact_owner')

        owner_id = user_obj.sudo().create({
            'name': owner_name,
            'login': owner_contact,
            'street': owner_address,
            'mobile': owner_contact,
        })

        # Getting incharge info from website
        incharge_name = kwargs.get('incharge_name')
        incharge_address = kwargs.get('incharge_address')
        incharge_contact = kwargs.get('contact_incharge')
        owner_is_incharge = kwargs.get('owner_inch')

        if owner_is_incharge == 'on':
            pass
        else:
            incharge_id = user_obj.sudo().create({
                
                'name': incharge_name,
                'login': incharge_contact,
                'street': incharge_address,
                'action_id' : request.env.ref('do_dairy_mgmt.dairy_kiosk_action').id,
                'mobile': incharge_contact,
            })

        # Getting dairy info from website
        dairy_name = kwargs.get('dairy_name')
        dairy_address = kwargs.get('dairy_address')
        dairy_cert_no = kwargs.get('certificate_no')
        
        # Creating dairy
        if owner_is_incharge == 'on':
            dairy = dairy_obj.sudo().create({
                'name': dairy_name,
                'street' : dairy_address,
                'certificate_no' : dairy_cert_no,
                'active' : True,
                'owner_id' : owner_id.id,
                'incharge_id' : owner_id.id,
                })
        else:
            dairy = dairy_obj.sudo().create({
                'name': dairy_name,
                'street' : dairy_address,
                'certificate_no' : dairy_cert_no,
                'active' : True,
                'owner_id' : owner_id.id,
                'incharge_id' : incharge_id.id,
                })            

        dairy.sudo().write({'state': 'submit'})
        csrf_token = request.params.pop('csrf_token', None)
        if request.session.uid and not request.validate_csrf(csrf_token):
            raise BadRequest('Session expired (invalid CSRF token)')
        res = request.render('do_dairy_mgmt_portal.dairy_success')
        return res
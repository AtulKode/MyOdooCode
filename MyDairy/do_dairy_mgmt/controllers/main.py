from odoo import http
from odoo.http import request
from odoo.exceptions import UserError

class DairyKioskController(http.Controller):

    @http.route('/update_rate_management', type='json', auth='user')
    def update_rate_management(self, dairy_id, animal_rates):
        rate_management = request.env['rate.management']
        for animal_name, rate in animal_rates.items():
            existing_record = rate_management.search([
                ('animal_id.name', '=', animal_name),
                ('dairy_id', '=', dairy_id)
            ])

            if existing_record:
                if rate > 0:
                    existing_record.write({
                        'rate_per_fat': rate
                    })
                else:
                    raise UserError('Rate should be greater than 0')
        return {'result': 'success'}

    def _get_allowed_company_ids(self):
        """ Return the allowed_company_ids based on cookies.

        Currently request.env.company returns the current user's company when called within a controller
        rather than the selected company in the company switcher and request.env.companies lists the
        current user's allowed companies rather than the selected companies.

        :returns: List of active companies. The first company id in the returned list is the selected company.
        """
        cids = request.httprequest.cookies.get('cids', str(request.env.user.company_id.id))
        return [int(cid) for cid in cids.split(',')]
   
    @http.route('/milk_intake_management/get_customer_data', type='json', auth='user')
    def get_customer_data(self):

        # if not res_id:
        #     target_record = request.env[model].with_context(allowed_company_ids=self._get_allowed_company_ids())
        # else:
        #     target_record = request.env[model].browse(res_id).with_context(allowed_company_ids=self._get_allowed_company_ids())
        # data = target_record._get_customer_data()
        data = request.env.ref('do_dairy_management.view_milk_intake_management_form').id
        print("dataaaaaaaaa ==",data)
        return {'data' : data}

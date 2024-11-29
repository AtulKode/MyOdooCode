import calendar
from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from odoo.http import request
from odoo.tools import date_utils


class ApprovalRequest(models.Model):
    """Extends crm.lead for adding more functions in it"""
    _inherit = 'approval.request'

    first_approval_date = fields.Datetime("First Approval Date")
    last_approval_date = fields.Datetime("Last Approval Date")
    finance_paid_date = fields.Datetime("Finance Paid Date")
    

    def _get_user_domain(self):
        if self.env.user.has_group('base.group_system'):
            return []
        return [('id', '=', self.env.user.id)]

    @api.model
    def get_date_domain(self, date_filter=None):
        """
        Returns a domain for filtering based on the date.
        """
        today = datetime.today()

        if not date_filter:
            return []

        if date_filter == 'day':
            # Filter for today's date
            return [('date_start', '>=', today.date())]

        elif date_filter == 'week':
            # Filter for the current week (Monday to Sunday)
            start_of_week = today - timedelta(days=today.weekday())
            return [('date_start', '>=', start_of_week.date())]

        elif date_filter == 'month':
            # Filter for the current month
            first_day_of_month = today.replace(day=1)
            last_day_of_month = today.replace(day=calendar.monthrange(today.year, today.month)[1])
            return [('date_start', '>=', first_day_of_month.date()), 
                    ('date_start', '<=', last_day_of_month.date())]

        return []

    @api.model
    def get_avg_time_submit_to_paid(self, date=None, stage=None, approval_type=None):
        domain = [('date_start', '!=', False), ('finance_paid_date', '!=', False)]
        if not self.env.user.has_group('base.group_system'):
            domain.append(('user_id', '=', self.env.user.id))
            
        today = datetime.today()

        if date:
            domain += self.get_date_domain(date)

        if stage and stage in ['in_progress','paid','approved']:
            domain.append(('request_status', '=', stage))

        if approval_type:
            domain.append(('approval_type', '=', approval_type))
        
        requests = self.search(domain)
        total_time = timedelta()
        count = 0
        for request in requests:
            if request.date_start and request.finance_paid_date:
                time_diff = request.finance_paid_date - request.date_start
                total_time += time_diff
                count += 1

        if count > 0:
            avg_time = total_time / count
            total_seconds = avg_time.total_seconds()
            if total_seconds >= 3600:
                hours = total_seconds // 3600
                return "{:.2f} hr".format(hours)
            elif total_seconds >= 60:
                minutes = total_seconds // 60
                return "{:.2f} min".format(minutes)
            else:
                return "{:.2f} sec".format(total_seconds)
        return "0 sec"

    @api.model
    def get_avg_time_submit_to_all_approved(self, date=None, stage=None, approval_type=None):
        """
        Computes the average time for all requests from submit to last approval.
        This method calculates the total time from date_start to last_approval_date.
        """
        domain = [('date_start', '!=', False), ('last_approval_date', '!=', False)]
        if not self.env.user.has_group('base.group_system'):
            domain.append(('user_id', '=', self.env.user.id))
        today = datetime.today()

        if date:
            domain += self.get_date_domain(date)

        if stage and stage in ['in_progress','paid','approved']:
            domain.append(('request_status', '=', stage))

        if approval_type:
            domain.append(('approval_type', '=', approval_type))

        requests = self.search(domain)
        total_time = timedelta()
        count = 0

        for request in requests:
            if request.date_start and request.last_approval_date:
                time_diff = request.last_approval_date - request.date_start
                total_time += time_diff
                count += 1

        if count > 0:
            avg_time = total_time / count
            total_seconds = avg_time.total_seconds()

            if total_seconds >= 3600:
                hours = total_seconds // 3600
                return "{:.2f} hr".format(hours)
            elif total_seconds >= 60:
                minutes = total_seconds // 60
                return "{:.2f} min".format(minutes)
            else:
                return "{:.2f} sec".format(total_seconds)
        return "0 sec"

    @api.model
    def get_avg_time_submit_to_first_approval(self, date=None, stage=None, approval_type=None):
        """
        Computes the average time for all requests from submit to first approval.
        This method calculates the total time from date_start to first_approval_date.
        """
        domain = [('date_start', '!=', False), ('first_approval_date', '!=', False)]
        if not self.env.user.has_group('base.group_system'):
            domain.append(('user_id', '=', self.env.user.id))
        today = datetime.today()

        if date:
            domain += self.get_date_domain(date)

        if stage and stage in ['in_progress','paid','approved']:
            domain.append(('request_status', '=', stage))

        if approval_type:
            domain.append(('approval_type', '=', approval_type))

        requests = self.search(domain)
        total_time = timedelta()
        count = 0
        for request in requests:
            if request.date_start and request.first_approval_date:
                time_diff = request.first_approval_date - request.date_start
                total_time += time_diff
                count += 1

        if count > 0:
            avg_time = total_time / count
            total_seconds = avg_time.total_seconds()

            if total_seconds >= 3600:
                hours = total_seconds // 3600
                return "{:.2f} hr".format(hours)
            elif total_seconds >= 60:
                minutes = total_seconds // 60
                return "{:.2f} min".format(minutes)
            else:
                return "{:.2f} sec".format(total_seconds)
        return "0 sec"

    def get_all_req_count(self):
        res = {}
        res['my_request_count'] = self.env['approval.request'].search_count([('request_owner_id','=',self.env.user.id), ('request_status', '!=', 'deleted')])
        res['my_request_review_count'] = self.env['approval.request'].search_count([('next_approver_user_id','=',self.env.user.id),('request_status','in',['pending', 'approved','in_progress'])])
        res['my_request_all_count'] = self.env['approval.request'].search_count([('approver_ids.user_id','=',self.env.user.id),('request_status','!=','pending')])
        res['my_request_deleted_count'] = self.env['approval.request'].search_count([('request_status', '=', 'deleted')])
        return res

    @api.model    
    def get_submitted_requests(self, date=None, stage=None, approval_type=None):
        domain = [('request_status', '=', 'pending')]
        if not self.env.user.has_group('base.group_system'):
            domain.append(('user_id', '=', self.env.user.id))
        if date:
            domain += self.get_date_domain(date)
        if approval_type:
            domain.append(('approval_type', '=', approval_type))

        res = self.env['approval.request'].search_count(domain)
        return res

    @api.model
    def get_approved_requests(self, date=None, stage=None, approval_type=None):
        domain = [('request_status', '=', 'approved')]
        if not self.env.user.has_group('base.group_system'):
            domain.append(('user_id', '=', self.env.user.id))
        if date:
            domain += self.get_date_domain(date)
        if approval_type:
            domain.append(('approval_type', '=', approval_type))

        res = self.env['approval.request'].search_count(domain)
        return res

    @api.model    
    def get_inprogress_requests(self, date=None, stage=None, approval_type=None):
        domain = [('request_status', '=', 'in_progress')]
        if not self.env.user.has_group('base.group_system'):
            domain.append(('user_id', '=', self.env.user.id))
        if date:
            domain += self.get_date_domain(date)
        if approval_type:
            domain.append(('approval_type', '=', approval_type))

        res = self.env['approval.request'].search_count(domain)
        return res

    @api.model    
    def get_paid_requests(self, date=None, stage=None, approval_type=None):
        domain = [('request_status', '=', 'paid')]
        if not self.env.user.has_group('base.group_system'):
            domain.append(('user_id', '=', self.env.user.id))
        if date:
            domain += self.get_date_domain(date)
        if approval_type:
            domain.append(('approval_type', '=', approval_type))

        res = self.env['approval.request'].search_count(domain)
        return res

    @api.model    
    def get_rejected_requests(self, date=None, stage=None, approval_type=None):
        domain = [('request_status', '=', 'rejected')]
        if not self.env.user.has_group('base.group_system'):
            domain.append(('user_id', '=', self.env.user.id))
        if date:
            domain += self.get_date_domain(date)
        if approval_type:
            domain.append(('approval_type', '=', approval_type))

        res = self.env['approval.request'].search_count(domain)
        return res

    def get_request_by_stage(self):
        state_dict = {
            'new': 'To Submit',
            'pending': 'Submitted',
            'receiving': 'Receiving',
            'in_progress': 'In Progress',
            'approved': 'Approved',
            'paid': 'Paid',
            'cancel': 'Cancelled',
            'rejected': 'Rejected',
            'refused': 'Refused',
            'deleted': 'Deleted',
        }
        result = self.env['approval.request'].read_group([('request_owner_id','=',self.env.user.id)], ["id:count"], ["request_status"])
        state_list = []
        value_list = []
        for res in result:
            state_list.append(state_dict[res['request_status']])
            value_list.append(res['request_status_count'])


        return [value_list, state_list]



    @api.model
    def get_my_requests(self, kwargs):

        return [('request_owner_id','=',self.env.user.id), ('request_status', '!=', 'deleted')]


    @api.model
    def deleted_my_requests(self, kwargs):

        return [('request_status', '=', 'deleted')]



    @api.model
    def get_all_requests_review(self, kwargs):
        return [('approver_ids.user_id','=',self.env.user.id),('request_status','!=','pending')]



    @api.model
    def get_my_requests_review(self, kwargs):
        return [('next_approver_user_id','=',self.env.user.id),('request_status','in',['pending', 'approved','in_progress'])]


    @api.model    
    def view_submitted_request(self, date=None, stage=None, approval_type=None):
        domain = [('request_status', '=', 'pending')]
        if not self.env.user.has_group('base.group_system'):
            domain.append(('user_id', '=', self.env.user.id))
        if date:
            domain += self.get_date_domain(date)
        if approval_type:
            domain.append(('approval_type', '=', approval_type))
        return domain

    @api.model    
    def view_approved_request(self, date=None, stage=None, approval_type=None):
        domain = [('request_status', '=', 'approved')]
        if not self.env.user.has_group('base.group_system'):
            domain.append(('user_id', '=', self.env.user.id))
        if date:
            domain += self.get_date_domain(date)
        if approval_type:
            domain.append(('approval_type', '=', approval_type))
        return domain

    @api.model    
    def view_in_progress_request(self, date=None, stage=None, approval_type=None):
        domain = [('request_status', '=', 'in_progress')]
        if not self.env.user.has_group('base.group_system'):
            domain.append(('user_id', '=', self.env.user.id))
        if date:
            domain += self.get_date_domain(date)
        if approval_type:
            domain.append(('approval_type', '=', approval_type))
        return domain

    @api.model    
    def view_paid_request(self, date=None, stage=None, approval_type=None):
        domain = [('request_status', '=', 'paid')]
        if not self.env.user.has_group('base.group_system'):
            domain.append(('user_id', '=', self.env.user.id))
        if date:
            domain += self.get_date_domain(date)
        if approval_type:
            domain.append(('approval_type', '=', approval_type))
        return domain

    @api.model    
    def view_rejected_request(self, date=None, stage=None, approval_type=None):
        domain = [('request_status', '=', 'rejected')]
        if not self.env.user.has_group('base.group_system'):
            domain.append(('user_id', '=', self.env.user.id))
        if date:
            domain += self.get_date_domain(date)
        if approval_type:
            domain.append(('approval_type', '=', approval_type))
        return domain
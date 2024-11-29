# -*- coding: utf-8 -*-

from odoo import models, api, tools
from collections import defaultdict
from odoo.http import request

class Menu(models.Model):
    _inherit = 'ir.ui.menu'

    @api.model
    @tools.ormcache("frozenset(self.env.user.show_menu_access_ids.ids)", "debug")
    def _visible_menu_ids(self, debug=False):
        """Return the ids of the menu items visible to the user."""
        self.clear_caches()

        visible = super()._visible_menu_ids(debug=debug)
        if not self.env.user.has_group('base.group_system') and self.env.user.user_menu_access_ids:
            context = {'ir.ui.menu.full_list': True}
            menus = self.env.user.show_menu_access_ids

            groups = self.env.user.groups_id
            if not debug:
                groups = groups - self.env.ref('base.group_no_one')
            # first discard all menus with groups the user does not have
            menus = menus.filtered(
                lambda menu: not menu.groups_id or menu.groups_id & groups)

            # take apart menus that have an action
            actions_by_model = defaultdict(set)
            for action in menus.mapped('action'):
                if action:
                    actions_by_model[action._name].add(action.id)
            existing_actions = {
                action
                for model_name, action_ids in actions_by_model.items()
                for action in self.env[model_name].browse(action_ids).exists()
            }
            action_menus = menus.filtered(lambda m: m.action and m.action in existing_actions)
            folder_menus = menus - action_menus
            visible = self.browse()
            # process action menus, check whether their action is allowed
            access = self.env['ir.model.access']
            MODEL_BY_TYPE = {
                'ir.actions.act_window': 'res_model',
                'ir.actions.report': 'model',
                'ir.actions.server': 'model_name',
            }

            # performance trick: determine the ids to prefetch by type
            prefetch_ids = defaultdict(list)
            for action in action_menus.mapped('action'):
                prefetch_ids[action._name].append(action.id)

            for menu in action_menus:
                action = menu.action
                action = action.with_prefetch(prefetch_ids[action._name])
                model_name = action._name in MODEL_BY_TYPE and action[MODEL_BY_TYPE[action._name]]
                if not model_name or access.check(model_name, 'read', False):
                    # make menu visible, and its folder ancestors, too
                    visible += menu
                    menu = menu.parent_id
                    while menu and menu in folder_menus and menu not in visible:
                        visible += menu
                        menu = menu.parent_id

            return set(visible.ids),context
        return visible,None

    def get_child_menus(self):
        Menus = self
        if self.child_id:
            for menu in self.child_id:
                Menus |= menu.get_child_menus()
            return Menus
        else:
            Menus |= self.child_id
            return Menus


    @api.returns('self')
    def _filter_visible_menus(self):
        """ Filter `self` to only keep the menu items that should be visible in
            the menu hierarchy of the current user.
            Uses a cache for speeding up the computation.
        """
        visible_ids,ctx = self._visible_menu_ids(request.session.debug if request else False)
        if ctx:
            return self.env['ir.ui.menu'].browse(visible_ids)
        return self.filtered(lambda menu: menu.id in visible_ids)
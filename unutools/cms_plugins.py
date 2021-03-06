# -*- coding: utf-8 -*-

from cms.plugin_base import CMSPluginBase
from cms.models.pluginmodel import CMSPlugin
from cms.plugin_pool import plugin_pool
from .forms import ApplicationForm
from django.utils.translation import gettext as _


class UnuToolPlugin(CMSPluginBase):
    model=CMSPlugin
    name = _(u"Форма бронирования УНУ-объектов ")
    render_template="unutool-plugin.html"
    def render(self, context, instance, placeholder):
        context.update({'form': ApplicationForm(prefix='equipment'),
                        'error': ' '})
        return context


plugin_pool.register_plugin(UnuToolPlugin)

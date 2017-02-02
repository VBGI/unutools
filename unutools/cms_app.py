# -*- coding: utf-8 -*-

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

class UnuToolApphook(CMSApp):
    name = _(u"Ajax-служба для бронирования УНУ-объектов")
    urls = ["bgi.unutools.urls"]

apphook_pool.register(UnuToolApphook)

from django.conf.urls import *
from bgi.unutools.views import (request_rent, equipment_list,
                            delete_rent_app)

urlpatterns = patterns('',
   url(r'^$', request_rent, name="unutool-app"),
   url(r'^show$', equipment_list, name="unutool-list"),
   url(r'^del$', delete_rent_app, name="delete_unu_app")

)

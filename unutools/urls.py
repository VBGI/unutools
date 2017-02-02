from django.conf.urls import *
from bgi.equipment.views import (request_rent, equipment_list,
                            delete_rent_app)

urlpatterns = patterns('',
   url(r'^$', request_rent, name="equipment-app"),
   url(r'^show$', equipment_list, name="equipment-list"),
   url(r'^del$', delete_rent_app, name="delete_rent_app")
   
)
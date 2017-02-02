#coding: utf-8
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from .models import Equipment, Application
from .messages import app_status, app_status_theme

class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization', 'startdate', 'enddate')
    list_filter = ('status', 'equipment', 'startdate', 'enddate', 'created')
    readonly_fields = ('unum',)

    def save_model(self, *args): 
        request, obj, form, change = args
        if change:
            send_mail(app_status_theme.format(obj.created),
                          app_status.format(obj.name,
                                            obj.created,
                                            obj.get_status_display()
                                            ),
                          'equipment@botsad.ru', [obj.email,], fail_silently=True)
        super(ApplicationAdmin, self).save_model(*args)


class EquipmentAdmin(admin.ModelAdmin):
    pass

admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(Application, ApplicationAdmin)

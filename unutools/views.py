# coding: utf-8
import gc

from django.http import HttpResponse
from django.template import RequestContext
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.utils.translation import gettext as _
from django.template.loader import render_to_string
from django.utils import timezone

from django.contrib.sites.models import Site

current_site = Site.objects.get_current()



from .forms import ApplicationForm

from .models import Application, Equipment
from .messages import *


@never_cache
def delete_rent_app(request):
    if request.method == 'GET':
        unum = request.GET.get('unum', '')
        pk = request.GET.get('pk', '')
        if not pk:
            obj = Application.objects.none()
        else:
            obj = Application.objects.filter(unum=unum, id=pk)
        if obj.exists():
            print obj[0].startdate, obj[0].enddate
            send_mail(app_created_theme.format(obj[0].created),
                      app_deleted.format(obj[0].name,
                                     obj[0].equipment.name,
                                     obj[0].startdate,
                                     obj[0].enddate
                                     ),
                      'equipment@botsad.ru', [obj[0].email], fail_silently=True)
            obj[0].delete()
            return HttpResponse(u'<h2>{}</h2>'.format(app_del_completed))
    return HttpResponse(u'<h2>{}</h2>'.format(_(u'Нечего выполнять')))


@never_cache
def equipment_list(request):
    objs = Application.objects.filter(enddate__gte=timezone.now()).exclude(status=2).order_by('-created',
                                                                                            'startdate',
                                                                                            'enddate')
    result = render_to_string('unutool-list.html',
                              {'objs': objs},
                              context_instance=RequestContext(request)
                              )
    return HttpResponse(result, content_type="text/plain")

        
@never_cache
@csrf_protect
def request_rent(request):
    response_data = {'error' : ''}

    if request.method == 'POST':
        form = ApplicationForm(request.POST, prefix='equipment')
        if form.is_valid():
            name = form.cleaned_data['name']
            org = form.cleaned_data['organization']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            content = form.cleaned_data['content']
            equipment = form.cleaned_data['equipment']
            startdate = form.cleaned_data['startdate'] 
            enddate = form.cleaned_data['enddate'] 
            try:
                equip = Equipment.objects.get(name__icontains=equipment)
                start_intersect = Application.objects.filter(startdate__lte=startdate,
                                              enddate__gte=startdate,
                                              equipment__pk=equip.pk).exclude(status='2').exists()
                end_intersect = Application.objects.filter(startdate__lte=enddate,
                                              enddate__gte=enddate,
                                              equipment__pk=equip.pk).exclude(status='2').exists()
                if start_intersect or end_intersect:
                    response_data.update({'error': _('На данное время уже подана заявка')})
                else:
                    application = Application.objects.create(name=name,
                                      organization=org,
                                      email=email,
                                      phone=phone,
                                      content=content,
                                      startdate=startdate,
                                      enddate=enddate,
                                      equipment=equip
                                      )
                    send_mail(app_created_theme.format(application.created),
                              app_created.format(name, application.equipment.name,
                                          application.startdate,
                                          application.enddate,
                                          'http://' +\
                                          current_site.domain +\
                                          reverse('delete_rent_app') +\
                                          '?unum={}&pk={}'.format(application.unum,
                                                                  application.pk)
                                          ),
                           'equipment@botsad.ru', [application.email, 'equipment@botsad.ru'], fail_silently=True)

            except Equipment.DoesNotExist:
                response_data.update({'error': _(u'Такого оборудования нет')})
            
        else:
            response_data.update({'error': _(u'Ошибка при заполнении полей формы')})

        response_data.update({'form' : form})
        result = render_to_string('unutool-form.html', response_data,  context_instance=RequestContext(request))
        gc.collect()
        return HttpResponse(result, content_type="text/plain")
            


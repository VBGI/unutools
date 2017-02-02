#coding: utf-8

import datetime
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _
# from cms.models.pluginmodel import CMSPlugin
import uuid


class Equipment(models.Model):
    name = models.CharField(default='',
                            verbose_name=_('название оборудования'),
                            unique=True,
                            max_length=255)
    
    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('оборудование')
        verbose_name_plural = _('оборудование')
        ordering = ('name',)


class Application(models.Model):
    statuses = (_('Находится на рассмотрении'),
                _('Время рассмотрения продлено'),
                _('Отклонена'),
                _('Принята'),
                )
    STATUSES = [('%s' % ind, item) for ind, item in enumerate(statuses)]
    
    name = models.CharField(max_length=300, default='', verbose_name=_('заказчик'))
    organization = models.CharField(max_length=300, default='', blank=True,
                                    verbose_name=_('организация'))
    email = models.EmailField(blank=False)
    phone = models.CharField(max_length=20, default='', verbose_name=_('телефон'),
                             blank=True)
    content = models.TextField(blank=True, default='',
                               verbose_name=_('дополнительно'))
    status = models.CharField(blank=True, verbose_name=_('статус'),
                              choices=STATUSES, max_length=1,
                              default=STATUSES[0][0])
    equipment = models.ForeignKey(Equipment, null=True,
                                  verbose_name=_('оборудование'))
    startdate = models.DateField(default=timezone.now(),
                                     verbose_name=_("Начало использования"),
                                     blank=True)
    enddate = models.DateField(default=timezone.now(),
                                   verbose_name=_("Окончание использования"),
                                   blank=True)
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name=_('подана'))
    updated = models.DateTimeField(auto_now=True,
                                   verbose_name=_('изменена'))
    unum = models.CharField(default=uuid.uuid4().hex,
                            max_length=32)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('заявка')
        verbose_name_plural = _('заявки')
        ordering = ('equipment', 'status', 'organization', 'created', 'startdate')
        

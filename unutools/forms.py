# coding: utf-8

from django.forms import ModelForm
from .models import Application
from django import forms
from django.utils.translation import gettext as _
from django.utils import timezone
from captcha.fields import ReCaptchaField

class  ApplicationForm(ModelForm):
    required_css_class = 'required'
    captcha = ReCaptchaField(attrs={'lang': 'ru'})
        
    class Meta:
        model = Application
        fields = ('name', 'organization', 'email', 'phone', 
                  'content', 'equipment', 'startdate', 'enddate',
                  )

    def clean_enddate(self):
        end = self.cleaned_data['enddate']
        start = self.cleaned_data['startdate']
        if end < start:
            raise forms.ValidationError(_("Дата окончания аренды должна быть больше даты  ее начала"))
        return end

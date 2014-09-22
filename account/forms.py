import re

from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import RadioSelect
from django.utils.translation import ugettext_lazy as _
from models import MyProfile

from village.models import Village, calculate_villages
from village.utils import get_fourth_point, get_distance


SPEED=(('full','Army full speed'),('full_cap','Captain full speed'),('mini','Army minimal speed'),('mini_cap','Captain minimal speed'))

class UserForm(forms.Form):
#    class Meta:
#        model = MyProfile
#        exclude = ['id']
    speed_army = forms.IntegerField(label=_("Speed army"),
                            help_text=_("required, 1-10, digits only."),
                            widget=forms.TextInput(attrs={'size':'2'}))
    speed_captain = forms.IntegerField(label=_("Speed captain"),
                            help_text=_("required, 1-10, digits only."),
                            widget=forms.TextInput(attrs={'size':'2'}))
    speed_merchant = forms.IntegerField(label=_("Speed merchant"),
                            help_text=_("required, 1-10, digits only."),
                            widget=forms.TextInput(attrs={'size':'2'}))
    speed_monk = forms.IntegerField(label=_("Speed monk"),
                            help_text=_("required, 1-10, digits only."),
                            widget=forms.TextInput(attrs={'size':'2'}))
    id = forms.IntegerField(initial='class',
                            label=_(" "),
                            widget=forms.TextInput(attrs={'size':'2', 'hidden':'true'}))

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        speed_army = cleaned_data['speed_army']
        speed_captain = cleaned_data['speed_captain']
        speed_merchant = cleaned_data['speed_merchant']
        speed_monk = cleaned_data['speed_monk']
        id = cleaned_data['id']
        try:
            cleaned_data['profile'] = MyProfile(speed_army=cleaned_data['speed_army'],
                                                speed_captain=cleaned_data['speed_captain'],
                                                speed_merchant=cleaned_data['speed_merchant'],
                                                speed_monk=cleaned_data['speed_monk'],
                                                id=cleaned_data['id'])
        except ValueError:
            raise forms.ValidationError(_('source data wrong, please, verify source data'))
        return cleaned_data

    def save(self):
        self.cleaned_data['profile'].save()
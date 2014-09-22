from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.template import context
from django.template.response import TemplateResponse
from forms import UserForm
from models import  MyProfile

@login_required
def profile(request):
#    id = request.user.id
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
#            speed_army = form.cleaned_data['speed_army']
#            speed_captain = form.cleaned_data['speed_captain']
#            id = request.user.id
            form.save()
            return TemplateResponse(request, "registration/profile.html", {"user": request.user, 'form':form})
    else:
        id = request.user.id
        try: #MyProfile.objects.get(id=int(id))

            speed_army = MyProfile.objects.get(id=int(id)).speed_army
            speed_captain = MyProfile.objects.get(id=int(id)).speed_captain
            speed_merchant = MyProfile.objects.get(id=int(id)).speed_merchant
            speed_monk = MyProfile.objects.get(id=int(id)).speed_monk
            form = UserForm(initial={'id': id,
                                     'speed_army': speed_army,
                                     'speed_captain': speed_captain,
                                     'speed_merchant': speed_merchant,
                                     'speed_monk': speed_monk})
        except:

            form = UserForm(initial={'id': id})

#    def form_valid(self, form):
#        form.save()
#        return super(profile, self).form_valid(form)
    return TemplateResponse(request, "registration/profile.html", {"user": request.user, 'form':form})


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/accounts/profile/")
    else:
        form = PasswordChangeForm()
    return TemplateResponse(request, "registration/password_change.html", {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/accounts/profile/")
    else:
        form = UserCreationForm()
    return TemplateResponse(request, "registration/register.html", {'form': form})
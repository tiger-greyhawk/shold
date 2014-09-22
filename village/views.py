import json
import datetime

from django.http import HttpResponse
from django.views.generic import FormView

from village.forms import InitVillagesForm, CreateVillageForm, format_distance, CalculateTimeForm, CalculateAttacksForm, AttackFromUserForm
from django.template.response import TemplateResponse
from village.models import Village
from village.utils import get_distance, seconds_to_strtime_and_more


class AddVillageView(FormView):
    form_class = CreateVillageForm
    success_url = '/villages/'
    template_name = 'village/add.html'

    def form_valid(self, form):
        form.save()
        return super(AddVillageView, self).form_valid(form)


class InitVillagesView(FormView):
    form_class = InitVillagesForm
    success_url = '/villages/'
    template_name = 'village/init.html'

    def form_valid(self, form):
        form.save()
        return super(InitVillagesView, self).form_valid(form)

def calculate_time(request):
    distance = None
    distance_x2 = None
    distance_x3 = None
    distance_x4 = None
    distance_x5 = None
    distance_x6 = None
    if request.method == 'POST':
        form = CalculateTimeForm(request.POST)
#        distance=(request.POST['distance'])
        if form.is_valid():
            a = form.cleaned_data['a']
            b = form.cleaned_data['b']
#            form.save()
#            village = form.cleaned_data['village']
#            distance = distance.cleaned_data['distance']
            distance = get_distance((a.x, a.y), (b.x, b.y))
            distance_x2 = distance//2
            distance_x3 = distance//3
            distance_x4 = distance//4
            distance_x5 = distance//5
            distance_x6 = distance//6
            distance = datetime.datetime.utcfromtimestamp(distance).strftime('%H:%M:%S')
            distance_x2 = ',  X2 = '+str(datetime.datetime.utcfromtimestamp(distance_x2).strftime('%H:%M:%S'))
            distance_x3 = ',  X3 = '+str(datetime.datetime.utcfromtimestamp(distance_x3).strftime('%H:%M:%S'))
            distance_x4 = ',  X4 = '+str(datetime.datetime.utcfromtimestamp(distance_x4).strftime('%H:%M:%S'))
            distance_x5 = ',  X5 = '+str(datetime.datetime.utcfromtimestamp(distance_x5).strftime('%H:%M:%S'))
            distance_x6 = ',  X6 = '+str(datetime.datetime.utcfromtimestamp(distance_x6).strftime('%H:%M:%S'))
            return TemplateResponse(request, 'village/calculate_time.html', {'form':form,
                                        'distance':distance, 'distance_x2':distance_x2, 'distance_x3':distance_x3,
                                        'distance_x4':distance_x4, 'distance_x5':distance_x5, 'distance_x6':distance_x6})
    else:
        form = CalculateTimeForm()

    return TemplateResponse(request, 'village/calculate_time.html', {'form': form, 'distance':distance})


def get_attack_from_user(request):
#    from_user = None
    if request.method == 'POST':
        form = AttackFromUserForm(request.POST)

        if form.is_valid():
            from_user = form.cleaned_data['from_user']
            from_user = from_user.village_set.all()

#            from_user = Village.owner(id=int(from_user.id))
#            from_user = owner.Village.all()
#            return calculate_attacks(from_user.village_set.all)
            return TemplateResponse(request, 'village/attack_from_user.html', {'form':form, 'from_user':from_user})
        else:
            from_user = None
            return TemplateResponse(request, 'village/attack_from_user.html', {'form': form, 'from_user':from_user})

    else:
#        from_user = None
        form = AttackFromUserForm()
    from_user = None
#    distance_b = None
#    id_village = None
    return TemplateResponse(request, 'village/attack_from_user.html', {'form': form, 'from_user':from_user})


def calculate_attacks(request):

    if request.method == 'POST':

        form = CalculateAttacksForm(request.POST)
        dict = form.data.copy()
        dict = dict.dict()
        a = {}
        x = 0;
        id_village = dict.pop('id_village')
        id_attack_village = Village.objects.get(id=int(id_village))
        distance_a = {}
        from_a = ()
        del dict['csrfmiddlewaretoken']
        dict = dict.values()
        while x < len(dict):
#            a[x] = dict[x]
            a[x] = Village.objects.get(id=int(dict[x]))
            distance_a[x] = get_distance((a[x].x, a[x].y), (id_attack_village.x, id_attack_village.y))
#            distance_b = get_distance((b.x, b.y), (id_attack_village.x, id_attack_village.y))
            distance_a[x] = a[x].name + ' :    ' + seconds_to_strtime_and_more(distance_a[x])
#            distance_b = seconds_to_strtime_and_more(distance_b)
#            from_a[x] = ((a[x].name) +'( '+ str(a[x].id) +' )  :')
            x = x+1
#            from_b = (b.name +'( '+ str(b.id) +' )  :')
#        b = dict[2]
#        b = Village.objects.get(id=int(b))

#        b = form.data[2]
#        distance=(request.POST['distance'])
#        if form.is_valid():
#            a = form.cleaned_data['a']
#            a = Village.objects.get(id=int(a))
#            b = form.cleaned_data['b']
#            b = Village.objects.get(id=int(b))
#            id_village = form.cleaned_data['id_village']
#            id_attack_village = Village.objects.get(id=int(id_village))
#            id_attack_village = form.cleaned_data['id_attack_village']
#            form.save()
#            village = form.cleaned_data['village']
#            distance = distance.cleaned_data['distance']

#            distance = datetime.datetime.utcfromtimestamp(distance_a).strftime('%H:%M:%S')
        return TemplateResponse(request, 'village/calculate_attacks.html', {'form':form, 'from_a':from_a,
                                        'distance_a':distance_a, 'a':a,})

    else:

        form = CalculateAttacksForm()
    distance_a = None
    distance_b = None
    id_village = None
    return TemplateResponse(request, 'village/calculate_attacks.html', {'form': form, 'distance_a':distance_a, 'distance_b':distance_b, 'id_village':id_village})




def calculated(request, distance):
#    village = Village.objects.get(pk=village_id)
#    distance = (request.POST['distance'])
    return TemplateResponse(request, "village/calculated.html", {'distance': distance})

def calculate_distance(request, a, b):
    a = Village.objects.get(pk=a)
    b = Village.objects.get(pk=b)

    data = {
        'a': {
            'id': a.id,
            'name': a.name
        },
        'b': {
            'id': b.id,
            'name': b.name
        },
        'distance': format_distance(get_distance((a.x, a.y), (b.x, b.y)))
    }
    response = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
    return HttpResponse(response, content_type='application/json')

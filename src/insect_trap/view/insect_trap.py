from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from base.gis import get_bounding_box, list_dict_to_geojson
from insect_trap.models import InsectTrap
from insect_trap.repositories import InsectTrapRepository
from rural_property.models import Field
from rural_property.repository import FieldRepository


@login_required
@csrf_exempt
def view(request):
    if request.method == "GET":
        fields = FieldRepository().list_all()
        bounding_box = [get_bounding_box(fields=fields, field_gis='geometry')]

        insect_traps = InsectTrapRepository().list_all()

        context = dict(
            fields_geojson=list_dict_to_geojson(list(fields.values())),
            insect_traps_geojson=list_dict_to_geojson(list(insect_traps.values())),
            bounding_box=bounding_box,
        )

        return render(request, 'insect_trap.html', context)

    elif request.method == "POST":
        field_id = request.POST.get('field_id')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        insect_trap_type_id = request.POST.get('trap_type_id')

        field = Field.objects.get(id=field_id)

        InsectTrap.objects.create(
            field=field,
            geometry=f'POINT({longitude} {latitude})',
            type_id=insect_trap_type_id,
            created_by=request.user
        )

        return JsonResponse(dict(success=True))

    else:
        return JsonResponse(dict(success=False, errors='Invalid request method'))

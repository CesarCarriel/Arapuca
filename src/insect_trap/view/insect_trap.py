import json
from datetime import datetime, date
from typing import List, Dict

from django.contrib.gis.geos import GEOSGeometry
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from geojson import FeatureCollection

from base.gis import get_bounding_box
from insect_trap.models import InsectTrap
from insect_trap.repositories import InsectTrapRepository
from rural_property.models import Field
from rural_property.repository import FieldRepository


def list_dict_to_geojson(values: List[Dict]):
    def format_list_of_dicts(data):
        def format_datetime(value):
            if isinstance(value, datetime):
                return value.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            elif isinstance(value, date):
                return value.strftime('%Y-%m-%d')
            elif isinstance(value, dict):
                return {key: format_datetime(val) for key, val in value.items()}
            elif isinstance(value, list):
                return [format_datetime(item) for item in value]
            else:
                return value

        return [{key: format_datetime(value) for key, value in item.items()} for item in data]

    format_dict = []

    for value in values:
        rec = dict()

        rec["type"] = "Feature"
        rec["geometry"] = json.loads(value["geometry"].geojson)

        rec["properties"] = dict()

        for index, field in value.items():
            if not isinstance(field, GEOSGeometry):
                rec["properties"][index] = field

        format_dict.append(rec)

    fields_geojson = FeatureCollection(format_list_of_dicts(format_dict))

    return json.dumps(dict(fields_geojson))


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
            created_by_id=1
        )

        return JsonResponse(dict(success=True))

    else:
        return JsonResponse(dict(success=False, errors='Invalid request method'))

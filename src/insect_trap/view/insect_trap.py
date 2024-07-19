import json
from datetime import datetime, date
from typing import List, Dict

from django.contrib.gis.db.models import Collect
from django.contrib.gis.geos import GEOSGeometry
from django.db import models
from django.db.models.functions import Concat
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from geojson import FeatureCollection

from insect_trap.models import InsectTrap
from rural_property.models import Field


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
        fields = Field.objects.annotate(
            path=Concat(
                models.F('tract__rural_property__code'),
                models.Value('-'),
                models.F('tract__code'),
                models.Value('-'),
                models.F('code'),
                output_field=models.CharField()
            ),
            rural_property_code=models.F('tract__rural_property__code'),
        ).all()
        insect_traps = InsectTrap.objects.annotate(
            rural_property_code=Concat(
                models.F('field__tract__rural_property__code'),
                models.Value('-'),
                models.F('field__tract__rural_property__name'),
                output_field=models.CharField()
            ),
            tract_code=models.F('field__tract__code'),
            field_code=models.F('field__code'),
            created_by_name=models.F('created_by__name'),
            insect_trap_type_name=Concat(
                models.F('type__name'),
                models.Value(' ('),
                models.F('type__insect__name'),
                models.Value(')'),
                output_field=models.CharField()
            )
        ).all()

        fields_bbox = fields.aggregate(Collect('geometry'))['geometry__collect'].extent

        min_x, min_y, max_x, max_y = fields_bbox[0], fields_bbox[1], fields_bbox[2], fields_bbox[3]
        bounding_box = [min_x, min_y, max_x, max_y]

        context = {
            'fields_geojson': list_dict_to_geojson(list(fields.values())),
            'insect_traps_geojson': list_dict_to_geojson(list(insect_traps.values())),
            'bounding_box': bounding_box,
        }

        return render(request, 'insect_trap.html', context)

    elif request.method == "POST":
        if request.method == 'POST':
            field_id = request.POST.get('field_id')
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')
            trap_type = request.POST.get('trap_type_id')

            field = Field.objects.get(id=field_id)
            insect_trap = InsectTrap.objects.create(
                field=field,
                geometry=f'POINT({longitude} {latitude})',
                type_id=trap_type,
                created_by_id=1
            )

            popup_content = f"""
            <div class="popup-content">
                <table class="popup-table">
                    <tr><th>Propriedade</th><td>{field.tract.rural_property.code}</td></tr>
                    <tr><th>Gleba</th><td>{field.tract.code}</td></tr>
                    <tr><th>Talhão</th><td>{field.code}</td></tr>
                    <tr><th>Criado por</th><td>{insect_trap.created_by.name}</td></tr>
                    <tr><th>Criado em</th><td>{insect_trap.created_at}</td></tr>
                </table>
            </div>
            """

            response_data = {
                'success': True,
                'latitude': latitude,
                'longitude': longitude,
                'popupContent': popup_content
            }

            return JsonResponse(response_data)
        return JsonResponse({'success': False}, status=400)

    else:
        return JsonResponse({'success': False, 'errors': 'Invalid request method'})

import json
from datetime import date, datetime
from typing import List, Dict

from django.contrib.gis.db.models import Collect
from django.contrib.gis.geos import GEOSGeometry
from django.db.models import QuerySet
from geojson import FeatureCollection


def get_bounding_box(fields: QuerySet, field_gis: str):
    fields_box = fields.aggregate(Collect(field_gis))[f'{field_gis}__collect'].extent

    min_x, min_y, max_x, max_y = fields_box[0], fields_box[1], fields_box[2], fields_box[3]

    return min_x, min_y, max_x, max_y


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

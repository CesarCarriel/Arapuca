from django.contrib.gis.db.models import Collect
from django.db.models import QuerySet


def get_bounding_box(fields: QuerySet, field_gis: str):
    fields_box = fields.aggregate(Collect(field_gis))[f'{field_gis}__collect'].extent

    min_x, min_y, max_x, max_y = fields_box[0], fields_box[1], fields_box[2], fields_box[3]

    return min_x, min_y, max_x, max_y

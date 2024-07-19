from django.db import models
from django.db.models import QuerySet
from django.db.models.functions import Concat

from rural_property.models import Field


class FieldRepository:
    def list_all(self) -> QuerySet[Field]:
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

        return fields

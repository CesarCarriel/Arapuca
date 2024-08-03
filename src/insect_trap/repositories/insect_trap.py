from django.db import models
from django.db.models.functions import Concat
from django.db.models.query import QuerySet

from insect_trap.models import InsectTrap, InsectTrapResult


class InsectTrapRepository:
    def list_all(self) -> QuerySet[InsectTrap]:
        latest_results = InsectTrapResult.objects.filter(insect_trap=models.OuterRef('pk')).order_by('-created_at')

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
            ),
            latest_result=models.Subquery(latest_results.values('insect_number')[:1]),
            high_infestation=models.Case(
                models.When(
                    type__infestation_alert_level__lte=models.F('latest_result'),
                    then=models.Value(True)
                ),
                default=models.Value(False)
            )
        ).all()

        return insect_traps

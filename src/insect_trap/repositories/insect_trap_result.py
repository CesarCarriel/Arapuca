from django.db import models
from django.db.models import QuerySet

from insect_trap.models import InsectTrapResult


class InsectTrapResultRepository:
    def list_by_insect_trap_id(self, insect_trap_id: int) -> QuerySet[InsectTrapResult]:
        return InsectTrapResult.objects.filter(insect_trap_id=insect_trap_id).annotate(
            created_by_name=models.F('created_by__name'),
        ).all().order_by('-created_at')

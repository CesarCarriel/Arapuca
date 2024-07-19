from django.db import models

from insect_trap.models import InsectTrapType


class InsectTrapTypeRepository:
    def list_all(self):
        return InsectTrapType.objects.annotate(insect_name=models.F('insect__name')).all()

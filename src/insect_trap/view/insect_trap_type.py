from django.db import models
from django.http import JsonResponse

from insect_trap.models import InsectTrapType


def view(request):
    if request.method == 'GET':
        types = InsectTrapType.objects.annotate(insect_name=models.F('insect__name')).all()
        data = list(types.values('id', 'name', 'insect_name'))

        return JsonResponse(data, safe=False)

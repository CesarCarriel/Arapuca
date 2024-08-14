from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from insect_trap.repositories import InsectTrapTypeRepository


@login_required
def view(request):
    if request.method == 'GET':
        insect_trap_types = InsectTrapTypeRepository().list_all()
        data = list(insect_trap_types.values('id', 'name', 'insect_name'))

        return JsonResponse(data, safe=False)

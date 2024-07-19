from django import forms
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from insect_trap.models import InsectTrap, InsectTrapResult
from insect_trap.repositories import InsectTrapResultRepository


class InsectTrapResultForm(forms.ModelForm):
    class Meta:
        model = InsectTrapResult
        fields = ['insect_number', 'observation']


@csrf_exempt
def view(request, id: int):
    if request.method == 'GET':
        insect_trap_result = InsectTrapResultRepository().list_by_insect_trap_id(insect_trap_id=id)

        data = list(insect_trap_result.values('id', 'insect_number', 'created_by_name', 'created_at', 'observation'))

        return JsonResponse(data, safe=False)

    elif request.method == 'POST':
        insect_trap = get_object_or_404(InsectTrap, id=id)

        form = InsectTrapResultForm(request.POST)

        if form.is_valid():
            result = form.save(commit=False)
            result.insect_trap = insect_trap
            result.created_by_id = 1

            result.save()

            return JsonResponse(dict(success=True))

        else:
            return JsonResponse(dict(success=False, errors=form.errors))

    return JsonResponse(dict(success=False, errors='Invalid request method'))

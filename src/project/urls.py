from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView

from insect_trap.view import insect_trap, insect_trap_result, insect_trap_type

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', RedirectView.as_view(pattern_name='rural_property', permanent=False)),

    path('insect-trap/', insect_trap.view, name='insect_trap'),

    path('insect-trap-types/', insect_trap_type.view, name='insect_trap_type'),

    path('insect-trap/<int:id>/result/', insect_trap_result.view, name='insect_trap_result'),
]

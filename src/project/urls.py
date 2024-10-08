from django import forms
from django.contrib import admin
from django.contrib.auth.forms import AuthenticationForm
from django.urls import path
from django.views.generic import RedirectView

from authentication.view.login import CustomLoginView
from insect_trap.view import insect_trap, insect_trap_result, insect_trap_type


class EmailLoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email')


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', RedirectView.as_view(pattern_name='insect_trap', permanent=False)),

    path('login/', CustomLoginView.as_view(), name='login'),

    path('insect-trap/', insect_trap.view, name='insect_trap'),

    path('insect-trap-types/', insect_trap_type.view, name='insect_trap_type'),

    path('insect-trap/<int:id>/result/', insect_trap_result.view, name='insect_trap_result'),
]

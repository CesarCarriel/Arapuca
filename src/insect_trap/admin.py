from django.contrib import admin
from .models import InsectTrap, InsectTrapType, Insect, InsectTrapResult


@admin.register(InsectTrap)
class InsectTrapAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'field', 'created_by', 'created_at')
    list_filter = ('type', 'type__insect', 'created_by')
    date_hierarchy = 'created_at'


@admin.register(InsectTrapType)
class InsectTrapTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    list_filter = ('insect',)
    search_fields = ('name', 'description')


@admin.register(Insect)
class InsectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'scientific_name', 'description')
    search_fields = ('name', 'description', 'scientific_name')


@admin.register(InsectTrapResult)
class InsectTrapResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'insect_number', 'insect_trap', 'created_by', 'created_at')
    list_filter = ('insect_trap', 'created_by')
    date_hierarchy = 'created_at'

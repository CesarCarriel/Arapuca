from django.contrib import admin
from .models import RuralProperty, Tract, Field


@admin.register(RuralProperty)
class RuralPropertyAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'name')
    list_filter = ('code',)
    search_fields = ('code', 'name')
    search_help_text = 'filtra pelo código e nome da propriedade'


@admin.register(Tract)
class TractAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'rural_property')
    list_filter = ('rural_property',)
    search_fields = ('code', 'rural_property__code', 'rural_property__name')


@admin.register(Field)
class Field(admin.ModelAdmin):
    list_display = ('id', 'code', 'tract')
    list_filter = ('tract__rural_property', 'tract')
    search_fields = ('code', 'tract__code', 'tract__rural_property__code', 'tract__rural_property__name')

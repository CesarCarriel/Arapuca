from django.db import models

from base.models import LogMixin


class Tract(LogMixin):
    code = models.CharField('código', max_length=20)
    rural_property = models.ForeignKey('rural_property.RuralProperty', verbose_name='propriedade', on_delete=models.PROTECT)

    class Meta:
        db_table = 'tract'
        verbose_name = 'gleba'

    def __str__(self):
        return f'{self.rural_property} - {self.code}'

from django.contrib.gis.db import models

from base.models import LogMixin


class Field(LogMixin):
    code = models.CharField('código', max_length=20)
    tract = models.ForeignKey('rural_property.Tract', verbose_name='gleba', on_delete=models.PROTECT)
    area = models.PolygonField(verbose_name='área')

    class Meta:
        db_table = 'field'
        verbose_name = 'talhão'
        verbose_name_plural = 'talhões'

    def __str__(self):
        return f'{self.tract.rural_property} - {self.tract} - {self.code}'

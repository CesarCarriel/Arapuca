from django.contrib.gis.db import models

from base.models import LogMixin


class InsectTrap(LogMixin):
    field = models.ForeignKey('rural_property.Field', verbose_name='talhão', on_delete=models.PROTECT)
    type = models.ForeignKey('insect_trap.InsectTrapType', verbose_name='tipo', on_delete=models.PROTECT)

    geometry = models.PointField()

    class Meta:
        db_table = 'insect_trap'
        verbose_name = 'armadilha'

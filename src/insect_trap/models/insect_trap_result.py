from django.conf import settings
from django.db import models

from base.models import LogMixin


class InsectTrapResult(LogMixin):
    insect_trap = models.ForeignKey('insect_trap.InsectTrap', verbose_name='armadilha', on_delete=models.PROTECT)

    insect_number = models.PositiveIntegerField('número de insetos')
    observation = models.TextField('observações', null=True, blank=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='criado por', on_delete=models.PROTECT)

    class Meta:
        db_table = 'insect_trap_result'
        verbose_name = 'resultado de armadilha'
        verbose_name_plural = 'resultados de armadilhas'

    def __str__(self):
        return f'{self.insect_number} inseto(s) na armadilha {self.insect_trap}'

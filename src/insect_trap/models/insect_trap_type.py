from django.db import models

from base.models import LogMixin


class InsectTrapType(LogMixin):
    name = models.CharField('nome', max_length=100)
    description = models.TextField('descrição', null=True, blank=True)
    insect = models.ForeignKey('insect_trap.Insect', verbose_name='inseto', on_delete=models.CASCADE)

    infestation_alert_level = models.PositiveIntegerField(' nível alerta de infestação',
                                                          help_text='em número de insetos')

    class Meta:
        db_table = 'insect_trap_type'
        verbose_name = 'tipo de armadilha'
        verbose_name_plural = 'tipos de armadilhas'

    def __str__(self):
        return f'{self.name} para {self.insect}'

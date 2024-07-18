from django.db import models

from base.models import LogMixin


class RuralProperty(LogMixin):
    code = models.CharField('código', max_length=20, db_index=True, unique=True)
    name = models.CharField('nome', max_length=100, unique=True)

    class Meta:
        db_table = 'rural_property'
        verbose_name = 'propriedade'

    def __str__(self):
        return f'{self.code}-{self.name}'

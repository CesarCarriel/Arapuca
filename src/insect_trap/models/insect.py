from django.db import models

from base.models import LogMixin


class Insect(LogMixin):
    name = models.CharField('nome', max_length=100)
    scientific_name = models.CharField('nome científico', max_length=200, null=True, blank=True)
    description = models.TextField('descrição', null=True, blank=True)

    class Meta:
        db_table = 'insect'
        verbose_name = 'inseto'

    def __str__(self):
        return self.name


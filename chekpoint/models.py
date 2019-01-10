import uuid
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator


class KeyCounter(models.Model):
    # общее количество ключей
    keys_amount = models.PositiveSmallIntegerField('Счётчик остатка',
        validators=[MaxValueValidator(999)], blank=True, null=True)
    
    def __str__(self):
        return '{}'.format(self.keys_amount)


class KeyBox(models.Model):
    """
    Базовая модель для хранения информации о выданных и
    погашенных ключах.
    """
    
    # уникальный идентификатор записи
    id = models.UUIDField(unique=True, auto_created=True, editable=False,
                          primary_key=True, default=uuid.uuid4)
    
    # ключь для погашения контрольной суммы
    key_code = models.CharField('Ключ', max_length=4, blank=True, null=True,
                                unique=True)
    
    # контрольная сумма
    check_sum = models.CharField('Контрольная сумма', max_length=32, blank=True,
                                 null=True, unique=True)
    
    # статус активации ключа (погашен/не погашен)
    activation_status = models.BooleanField('Активирован', default=False,
                                            blank=False, null=True)
    
    # статус выдачи ключа (выдан/не выдан)
    issue_status = models.BooleanField('Выдан', default=False, blank=False,
                                       null=True)
    
    # дата и время создания ключа
    pub_date = models.DateTimeField('Дата и время создания', blank=True,
                                    null=True)
    
    # дата и время погашения ключа
    end_date = models.DateTimeField('Дата и время активации', blank=True,
                                    null=True)
    
    # подсчёт ключей
    key_counter = models.ForeignKey(KeyCounter, verbose_name='Осталось',
                                    blank=True,
                                    null=True,
                                    on_delete=models.DO_NOTHING, default=1,
                                    editable=False)
    # остановка подсчёта ключей
    counter_write_off = models.BooleanField(blank=True, null=True,
                                            default=False,
                                            editable=False)
    
    # владелец ключа
    owner = models.ForeignKey(User, verbose_name='Владелец', blank=True,
                              null=True, default=1,
                              on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.id)
    
    def save(self, *args, **kwargs):
        # ленивый импорт, исключает рекурсию
        from .sumchecker import check_sum_generator
        check_sum_generator(self)
        super(KeyBox, self).save(*args, **kwargs)
    
    class Meta:
        ordering = ['-pub_date']

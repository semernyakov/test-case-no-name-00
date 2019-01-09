import uuid
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator


class KeyCounter(models.Model):
    # общее количество ключей
    keys_amount = models.PositiveSmallIntegerField(
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
    key_code = models.CharField(max_length=4, blank=True, unique=True)
    
    # контрольная сумма
    check_sum = models.CharField(max_length=32, blank=True, unique=True)
    
    # статус активации ключа (погашен/не погашен)
    activation_status = models.BooleanField(default=None, blank=False)

    # статус выдачи ключа (выдан/не выдан)
    issue_status = models.BooleanField(default=False, blank=False)
    
    # дата и время выдачи ключа
    pub_date = models.DateTimeField(blank=True, null=True)
    
    # дата и время погашения ключа
    end_date = models.DateTimeField(blank=True, null=True)

    # подсчёт ключей
    key_counter = models.ForeignKey(KeyCounter, blank=True, null=True,
                                    on_delete=models.DO_NOTHING, default=1,
                                    editable=False)

    # владелец ключа
    owner = models.ForeignKey(User, blank=True, null=True,
                              on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        # ленивый импорт, исключает рекурсию
        from .sumchecker import check_sum_generator
        check_sum_generator(self)
        super(KeyBox, self).save(*args, **kwargs)

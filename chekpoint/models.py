import uuid
import hashlib
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator


class KeyBox(models.Model):
    """
    Базовая модель для хранения информации о выданных и
    погашенных ключах.
    """
    # уникальный идентификатор записи
    id = models.UUIDField(unique=True, auto_created=True, editable=False,
                          primary_key=True, default=uuid.uuid4)
    
    # ключь для погашения контрольной суммы
    key_code = models.CharField(max_length=4, blank=True)
    
    # контрольная сумма
    check_sum = models.CharField(max_length=32, blank=True)
    
    # статус активации ключа (погашен/не погашен)
    activation_status = models.BooleanField(default=None, blank=False)

    # статус выдачи ключа (выдан/не выдан)
    issue_status = models.BooleanField(default=False, blank=False)
    
    # общее количество ключей
    keys_amount = models.SmallIntegerField(validators=[MaxValueValidator(999)],
                                           blank=True, null=True)
    
    # дата и время выдачи ключа
    pub_date = models.DateTimeField(blank=True, null=True)
    
    # дата и время погашения ключа
    end_date = models.DateTimeField(blank=True, null=True)

    # владелец ключа
    owner = models.ForeignKey(User, blank=True, null=True,
                              on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

    def check_sum_generator(self):
        """
        Генератор контрольной суммы. Используется 128-битный
        алгоритм хеширования md5
        """
        hash = hashlib.md5()
        if self.key_code:
            # t = self.key_code.encode()
            hash.update(b'self')
        return hash.hexdigest()


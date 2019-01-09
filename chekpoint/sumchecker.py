import hashlib

from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import KeyCounter, KeyBox


def check_sum_generator(self):
    """
    Генерация контрольной сумму,
    c установкой сопутсвующих параметров
    """
    if self.key_code is not None:
        hashgen = hashlib.md5()
        key_code = self.key_code.encode()
        hashgen.update(key_code)
        self.check_sum = hashgen.hexdigest()
        if self.check_sum:
            self.pub_date = timezone.now()
            #TODO: доработать счётчик!
            if self.end_date is None and self.key_counter.keys_amount:
                obj = get_object_or_404(KeyCounter, pk=self.key_counter.id)
                obj.keys_amount -= 1
                obj.save()
        return


def check_sum_controller(code):
    """
    Проверка контрольной суммы
    """
    if code:
        hashgen = hashlib.md5()
        key_code = code.encode()
        hashgen.update(key_code)
        input_check_sum = hashgen.hexdigest()
        if input_check_sum:
            try:
                obj = KeyBox.objects.get(check_sum=input_check_sum)
                return obj.check_sum
            except KeyBox.DoesNotExist:
                raise Http404("Введённый код отсутствует, либо уже активирован")
                
            




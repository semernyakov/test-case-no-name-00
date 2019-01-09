from django.core.management.base import BaseCommand, CommandError
from django.utils.crypto import get_random_string
from chekpoint.models import KeyBox
import random


class Command(BaseCommand):
    help = 'Генеририрует 10 4-х значных кодов и создаёт 10 соответсвующих ' \
           'записей в базе. Для запуска выполните команду' \
           '"./manage.py createkeycode" число можно указать любое!'

    def handle(self, *args, **options):

        key_cod = ""
        key_box = list()
        row = list('123456789qwertyuiopasdfghjklzxc'
                   'vbnmQWERTYUIOPASDFGHJKLZXCVBNM')

        counter = 10
        while counter:
            counter -= 1
            for x in range(4):
                key_cod += random.choice(row)
            key_box.append(key_cod)
            key_cod = ""
        
        if key_box:
            try:

                for i in key_box:
                    kb = KeyBox(key_code=i)
                    kb.save()
                    
            except CommandError as e:
                print(e)
                raise

        self.stdout.write(self.style.SUCCESS('Успешно созданно 10 записей! {}'.format(key_box)))
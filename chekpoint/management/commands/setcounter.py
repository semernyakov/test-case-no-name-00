from django.core.management.base import BaseCommand, CommandError

from chekpoint.models import KeyCounter


class Command(BaseCommand):
    help = 'Создёт запись со значением "500" в модели KeyCounter,' \
           'в случае если модель пуста!'
    
    def handle(self, *args, **options):
        
        try:
            counter = KeyCounter(keys_amount=500)
            counter.save()
        except CommandError as e:
            print(e)
            raise CommandError
        
        self.stdout.write(self.style.SUCCESS('Запись успешно создана, со '
                                             'значением 500 едениц!'))

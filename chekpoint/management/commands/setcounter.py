from django.core.management.base import BaseCommand, CommandError
from chekpoint.models import KeyCounter


class Command(BaseCommand):
    help = 'Создёт запись со значением "500" в модели KeyCounter,' \
           'в случае если модель пуста!'

    def handle(self, *args, **options):

        try:
            counter = KeyCounter.objects.get(pk=1)
        except KeyCounter.DoesNotExist:
            counter = KeyCounter(keys_amount=500)
            counter.save()

        self.stdout.write(self.style.SUCCESS('Alredy exists or Successfully '
                                             'created: "%s"' % counter))
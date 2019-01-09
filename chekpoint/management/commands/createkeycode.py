from django.core.management.base import BaseCommand, CommandError
import random


class Command(BaseCommand):
    help = 'Generates random 4-digit numbers'

    def add_arguments(self, parser):
        parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        psw = ""
        box = list()
        row = list('123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM')
    
        limit = 1000
        while limit:
            for x in range(4):
                psw += random.choice(row)
            box.append(psw)
            limit -= 1
            psw = ""
        
        #
        # for poll_id in options['poll_id']:
        #     try:
        #         poll = Poll.objects.get(pk=poll_id)
        #     except Poll.DoesNotExist:
        #         raise CommandError('Poll "%s" does not exist' % poll_id)
        #
        #     poll.opened = False
        #     poll.save()

        self.stdout.write(self.style.SUCCESS('Successfully created cod "%s"' % box))
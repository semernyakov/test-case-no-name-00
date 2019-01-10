from django.contrib import messages
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone

from .form import ChekActivationForm, KeyCodeActivator
from .models import KeyBox, KeyCounter
from .sumchecker import check_sum_controller


def home(request):
    if request.method == 'POST':
        form = ChekActivationForm(request.POST or None)
        if form.is_valid():
            code = form.cleaned_data['code']
            if code:
                try:
                    hash_link = check_sum_controller(code)
                    obj = KeyBox.objects.get(check_sum=hash_link)
                    return HttpResponseRedirect('/push/{}'.format(obj.id))
                except:
                    messages.info(request,
                                  'Вы не правльно ввели секретный код, '
                                  'попробуйте ещё раз!')
                    return HttpResponseRedirect('/')
    else:
        form = ChekActivationForm()
    try:
        kb = KeyBox.objects.all()
    except KeyBox.DoesNotExist:
        raise Http404("Link does not exist")
    try:
        kc = KeyCounter.objects.latest('id')
    except:
        raise Http404("Key counter does not exist")
    return render(request, 'chekpoint/home.html', {
        'items': kb, 'counter': kc, 'form': form})


def push_check_sum(request, id):
    try:
        check_sum = KeyBox.objects.get(id=id)
    except KeyBox.DoesNotExist:
        messages.info(request, 'Объект не найден! Ошибка 404')
        return HttpResponseRedirect('/')
    except Exception as e:
        print(e)
        messages.info(request, 'Объект не найден! Ошибка 404')
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        form = KeyCodeActivator(request.POST or None)
        if form.is_valid():
            get_check_sum = form.cleaned_data['check_sum']
            
            if get_check_sum == check_sum.check_sum:
    
                if not check_sum.issue_status:
                    messages.info(request, 'Ключ нельзя активировать, до момента '
                                           'его выдачи!')
                    return HttpResponseRedirect('/push/{}'.format(check_sum))
                else:
                    check_sum.activation_status = True
                    check_sum.end_date = timezone.now()
                    check_sum.save()
                    messages.info(request,
                                  'Поздравляем! Вы успешно активировали ваш '
                                  'секретный ключ.')
                    return HttpResponseRedirect('/push/{}'.format(check_sum))
            else:
                messages.info(request,
                              'Контрольные суммы не совпадают! Попробуйте ещё '
                              'раз.')
                return HttpResponseRedirect('/push/{}'.format(check_sum))
        else:
            messages.info(request,
                          'Не верно введена контрольная сумма! Попробуйте ещё '
                          'раз!')
    else:
        form = ChekActivationForm()
    return render(request, 'chekpoint/done.html',
                  {'check_sum': check_sum, 'form': form})

from django.http import Http404
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect

from .models import KeyBox, KeyCounter
from .form import ChekActivationForm
from .sumchecker import check_sum_controller


def home(request):
    if request.method == 'POST':
        form = ChekActivationForm(request.POST or None)
        if form.is_valid():
            code = form.cleaned_data['code']
            if code:
                try:
                    hash_link = check_sum_controller(code)
                    return HttpResponseRedirect('/push/{}'.format(hash_link))
                except:
                    messages.info(request, 'Вы не правльно ввели секретный код, попробуйте ещё раз!')
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


def push_check_sum(request, check_sum):
    try:
        check_sum = KeyBox.objects.get(check_sum=check_sum)
    except KeyBox.DoesNotExist:
        raise Http404("Link does not exist")
    return render(request, 'chekpoint/done.html', {'check_sum': check_sum})

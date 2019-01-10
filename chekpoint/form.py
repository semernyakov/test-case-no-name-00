from django import forms


class ChekActivationForm(forms.Form):
    code = forms.CharField(max_length=4)


class KeyCodeActivator(forms.Form):
    check_sum = forms.CharField(max_length=32, min_length=32)

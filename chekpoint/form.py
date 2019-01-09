from django import forms


class ChekActivationForm(forms.Form):
    code = forms.CharField(max_length=4)


class KeyCodeGenerator(forms.Form):
    pass

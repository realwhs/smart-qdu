from django import forms


class BindJwForm(forms.Form):
    jw_account = forms.CharField(max_length=12)
    jw_password = forms.CharField()
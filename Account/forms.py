from django import forms


class LoginForm(forms.Form):
    user_name = forms.CharField(max_length=15)
    password = forms.CharField(max_length=20)


class RegisterForm(forms.Form):
    user_name = forms.CharField(max_length=10)
    password1 = forms.CharField(max_length=20)
    #password2 = forms.CharField(max_length=20)
    email = forms.EmailField(max_length=20)


class ChangePswForm(forms.Form):
    old_password = forms.CharField(max_length=20)
    password1 = forms.CharField(max_length=20)
    password2 = forms.CharField(max_length=20)
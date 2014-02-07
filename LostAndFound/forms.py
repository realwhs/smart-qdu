from django import forms


class PostInfoForm(forms.Form):
    item_name = forms.CharField(max_length=30)
    item_type = forms.CharField(max_length=10)
    location = forms.CharField(max_length=30)
    #image = forms.FileField(required=False)
    content = forms.CharField(max_length=100)
    time = forms.DateField()
    name = forms.CharField(max_length=15)
    phone = forms.CharField(max_length=11)
    qq = forms.CharField(max_length=11)
    email = forms.EmailField()


class CommentForm(forms.Form):
    comment = forms.CharField(max_length=300)







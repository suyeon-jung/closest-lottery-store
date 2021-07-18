from django import forms

class SearchForm(forms.Form):
    print(forms)
    user_address = forms.CharField(label='user_address')
    print(user_address)
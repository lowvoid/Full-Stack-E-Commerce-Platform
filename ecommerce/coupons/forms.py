from django import forms


class CounponApplyForm(forms.Form):
    code = forms.CharField(max_length=8)
    
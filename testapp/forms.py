from django import forms
from .models import Employee

class empform(forms.ModelForm):
    class Meta:
        model = Employee
        fields='__all__'
    def clean_ename(self):
        print("here ")
        if self.cleaned_data['ename']=="venu":
            # print("kaefkf")
            self.cleaned_data['ename']="babu"


        return self.cleaned_data['ename']

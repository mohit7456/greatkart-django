from django import forms
from .models import Account

class RegistrationForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput(attrs={          # In form we dont have password field so here we add password field
        'placeholder': 'Enter Password',                                   # and confirm password field in the form
    }))

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password',
    }))
    

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']

    def __init__(self, *args, **kwargs):                                               # And here we add CSS to all fields in the form and place-
        super(RegistrationForm, self).__init__(*args, **kwargs)                        # -holder also.
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'     # "super" yaha pe joh django ki deafult classs h usko modified kar rahe h.
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter last Name'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone Number'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email Address'

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean(self):                                                                  # Here we checking password and confirm-password are same or not?
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match!"
            )

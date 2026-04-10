from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms

User = get_user_model()

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        base_class = 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
        placeholders = {
        "username": "Username",
        "email": "Email",
        "first_name": "First name",
        "last_name": "Last name",
        "password1": "Password",
        "password2": "Confirm password",
    }


        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': base_class,
                'placeholder': placeholders.get(field_name, field.label)

            })
            
            field.label = ""

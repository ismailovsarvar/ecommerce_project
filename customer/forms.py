from django import forms

from customer.models import CustomerUser
from customer.models import Customer, User


class CustomerModelForm(forms.ModelForm):
    class Meta:
        model = Customer
        exclude = ()


class LoginForm(forms.Form):
    # email = forms.EmailField()
    phone = forms.CharField(max_length=13)
    password = forms.CharField(max_length=255)

    # def clean_email(self):
    #     email = self.data.get('email')
    #     if not User.objects.filter(email=email).exists():
    #         raise forms.ValidationError('Email does not exist')
    #     return email

    def clean_phone(self):
        phone = self.data.get('phone')
        if not User.objects.filter(phone=phone).exists():
            raise forms.ValidationError('Number does not exist')
        return phone

    def clean_password(self):
        email = self.cleaned_data.get('email')
        password = self.data.get('password')
        try:
            user = User.objects.get(email=email)
            print(user)
            if not user.check_password(password):
                raise forms.ValidationError('Password did not match')
        except User.DoesNotExist:
            raise forms.ValidationError(f'{email} does not exists')
        return password


# class RegisterModelForm(forms.ModelForm):
#     confirm_password = forms.CharField()
#
#     class Meta:
#         model = User
#         fields = ('email', 'password')
#
#     def clean_confirm_password(self):
#         pass

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=150)
    phone_number = forms.CharField(max_length=13)
    password = forms.CharField(widget=forms.PasswordInput, max_length=100)
    confirm_password = forms.CharField(widget=forms.PasswordInput, max_length=100)

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if User.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError("Phone number already exists")
        return phone_number

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords don't match")

        return User

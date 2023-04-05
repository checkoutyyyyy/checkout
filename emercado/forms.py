# from django import forms
# from django.contrib.auth import authenticate, login, get_user_model
# from .models import User
# from django.contrib.auth.forms import ReadOnlyPasswordHashField
# from django.contrib.auth.forms import UserCreationForm


# # Create your forms here.

# class SignupForm(UserCreationForm):

#     password1 = forms.Field(
#         label='Password', widget=forms.PasswordInput)
#     password2 = forms.Field(
#         label='Confirm Password', widget=forms.PasswordInput)

#     class Meta:
#         model = User
#         fields = ('email','first_name', 'middle_name', 'last_name', 'address', 'phone_number',
#                   'password1', 'password2'
#                   )

#         widgets = {
#                    'email': forms.EmailInput(attrs={'class': 'form-control', 'required': 'true' }),
#                    'first_name': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
#                    'middle_name': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
#                    'last_name': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
#                    'address': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
#                    'phone_number': forms.NumberInput(attrs={'class': 'form-control', 'required': 'true'}),
#                    'password1': forms.PasswordInput(attrs={'class': 'form-control', 'required': 'true'}),
#                    'password2': forms.PasswordInput(attrs={'class': 'form-control', 'required': 'true'}),
#         }

    # def clean_password2(self):
    #     '''
    #     Verify both passwords match.
    #     '''
    #     password1 = self.cleaned_data.get("password1")
    #     password2 = self.cleaned_data.get("password2")
    #     if password1 and password2 and password1 != password2:
    #         raise forms.ValidationError("Passwords don't match")
    #     return password2

    # def save(self, commit=True):
    #     # Save the provided password in hashed format
    #     user = super(SignupForm, self).save(commit=False)
    #     user.set_password(self.cleaned_data["password1"])
    #     user.is_active = True

    #     if commit:
    #         user.is_active = True
    #         user.save()
    #     return user

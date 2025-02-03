from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms


User = get_user_model()

class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        class_update_fields = ('password1','password2')
        for field in class_update_fields:
            self.fields[field].widget.attrs['placeholder'] ='password'
            if field == 'password1':
                self.fields[field].label = '비밀번호'
            else:
                self.fields[field].label = '비밀번호 확인'

    class Meta:
        model = User
        fields = ('email','nickname')
        labels = {
            'email':'이메일',
            'nickname':'닉네임'
            }
        widgets= {
            'email': forms.EmailInput(
                attrs={
                    'placeholder':'eample@example.com',
                    'class': 'form-control'
                }
            ),
            'nickname': forms.TextInput(
                attrs={
                    'placeholder': '닉네임',
                    'class':'form-control,'
                }
            )
        }

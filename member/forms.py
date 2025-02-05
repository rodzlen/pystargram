from django.contrib.auth import get_user_model, authenticate
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

class LoginForm(forms.Form):
    email = forms.CharField(
        label= '이메일',
        required=True,
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'eample@example.com',
                'class': 'form-control'
            }
        )
    )
    password = forms.CharField(
        label='패스워드',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'PASSWORD',
                'class': 'form-control'
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.user = None

    def clean(self):
        cleaned_data = super().clean()
        email= cleaned_data.get('email')
        password= cleaned_data.get('password')
        print(email, password)

        self.user = authenticate(username=email, password=password)
        print(self.user)
        if self.user is None:
            raise forms.ValidationError('아이디와 비밀번호가 틀렸거나 없는 사용자입니다.')

        if not self.user.is_active:
            raise forms.ValidationError('이메일이 인증되지 않았습니다')

        return cleaned_data
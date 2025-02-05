from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import signing
from django.core.signing import TimestampSigner, SignatureExpired
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import FormView, DetailView
from django.views import View
from member.forms import SignupForm, LoginForm
from member.models import UserFollowing
from util.email import send_email

User = get_user_model()
class SignupView(FormView):
    template_name = 'auth/signup.html'
    form_class = SignupForm
    #success_url = reverse_lazy('signup_done')

    def form_valid(self, form):
        user = form.save()
        # 이메일 발송
        signer = TimestampSigner()
        signed_user_email = signer.sign(user.email)
        signer_dump = signing.dumps(signed_user_email)
        # print(signer_dump)
        # decoded_user_email = signing.loads(signer_dump)
        # print(decoded_user_email)
        # email = signer.unsign(decoded_user_email, max_age=60*30)
        # print(email)

        #http://localhost:8000/verify/?code=asd
        url = f'{self.request.scheme}://{self.request.META['HTTP_HOST']}/verify/?code={signer_dump}'

        from config import settings
        if settings.DEBUG:
            print(url)

        subject= '[Pystargram]이메일 인증을 완료해 주세요'
        message = f'다음 링크를 클릭해 주세요. <a href="{url}">url</a>'
        send_email(subject,message,user.email)

        return render(self.request, template_name='auth/signup_done.html', context={'user':user})

def verify_email(request):
    code = request.GET.get('code','')
    signer = TimestampSigner()

    try:
        decoded_user_email = signing.loads(code)
        email = signer.unsign(decoded_user_email, max_age=60)
    except (TypeError, SignatureExpired):
        return render(request, 'auth/not_verified.html')

    user = get_object_or_404(User, email=email, is_active=False)
    user.is_active = True
    user.save()

    return redirect(reverse('login'))

class LoginView(FormView):
    template_name = 'auth/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        user = form.user
        login(self.request, user)

        next_page = self.request.GET.get('next')
        if next_page:
            return HttpResponseRedirect(next_page)

        return HttpResponseRedirect(self.get_success_url())

class UserProfileView(DetailView):
    model = User
    template_name = 'profile/detail.html'
    slug_field = 'nickname'
    slug_url_kwarg = 'slug'
    queryset = User.objects.all().prefetch_related('post_set', 'post_set__images','followers','following')

class UserFollowingView(LoginRequiredMixin, View):
    def post(self, *args, **kwargs):
        pk = kwargs.get('pk',0)
        to_user = get_object_or_404(User, pk-pk)

        following= UserFollowing.objects.filter(
            to_user= to_user,
            from_user = self.request.user
        )
        if following.exist():
            following.delete()
        else:
            UserFollowing.objects.filter(
                to_user=to_user,
                from_user=self.request.user
            )
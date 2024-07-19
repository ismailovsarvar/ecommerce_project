from django.contrib.auth import authenticate, logout
from django.contrib.auth import login
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from customer.forms import LoginForm, RegisterModelForm


# def login_page(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data['email']
#             password = form.cleaned_data['password']
#             user = authenticate(request, email=email, password=password)
#             if user:
#                 login(request, user)
#                 return redirect('customers')
#     else:
#         form = LoginForm()
#
#     return render(request, 'Login_Register/login.html', {'form': form})


def logout_page(request):
    if request.method == 'GET   ':
        logout(request)
        return redirect('customers')
    return render(request, 'Login_Register/logout.html')


# def register_page(request):
#     if request.method == 'POST':
#         form = RegisterModelForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             password = form.cleaned_data['password']
#
#             user.set_password(password)
#             user.save()
#
#             login(request, user)
#             return redirect('customers')
#     else:
#         form = RegisterModelForm()
#     return render(request, 'Login_Register/register.html', {'form': form})


"""TEMPLATE VIEW"""


class LoginPageView(TemplateView):

    def get(self, request):
        form = LoginForm()
        return render(request, 'Login_Register/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                return redirect('customers')


# class RegisterPageView(TemplateView):
#     def get(self, request):
#         form = RegisterModelForm()
#         return render(request, 'Login_Register/register.html', {'form': form})
#
#     def post(self, request):
#         form = RegisterModelForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data['email']
#             password = form.cleaned_data['password']
#             user = form.save(commit=False)
#             user.set_password(password)
#             user.save()
#             login(request, user)
#             return redirect('customers')

# class RegisterView(FormView):
#     template_name = 'Login_Register/register.html'
#     form_class = RegisterModelForm
#     redirect_authenticated_user = True
#     success_url = reverse_lazy('customers')
#
#     def form_valid(self, form):
#         user = form.save()
#         if user:
#             login(self.request, user)
#         return super(RegisterView, self).form_valid(form)


class RegisterView(FormView):
    template_name = 'Login_Register/register.html'
    form_class = RegisterModelForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('customers')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.is_active = False
        user.save()

        # Send activation email
        current_site = get_current_site(self.request)
        mail_subject = 'Activate your account.'
        message = render_to_string('Login_Register/activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })
        to_email = form.cleaned_data.get('email')
        send_mail(mail_subject, message, 'webmaster@mydomain.com', [to_email])

        return HttpResponse('Please confirm your email address to complete the registration')

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(self.success_url)
        return super().get(request, *args, **kwargs)


# Activation View

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(User, pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('customers')  # Replace 'customers' with your home view name
    else:
        return HttpResponse('Activation link is invalid!')

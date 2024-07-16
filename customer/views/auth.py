from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy

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

class RegisterView(FormView):
    template_name = 'Login_Register/register.html'
    form_class = RegisterModelForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('customers')

    def form_valid(self, form):
        user = form.save()
        if user:
            login(self.request, user)
        return super(RegisterView, self).form_valid(form)

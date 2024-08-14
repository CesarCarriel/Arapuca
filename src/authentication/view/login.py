from django import forms
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views import View


class CustomLoginForm(forms.Form):
    username = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


class CustomLoginView(View):
    def get(self, request):
        form = CustomLoginForm()

        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = CustomLoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                return redirect('/')

            else:
                form.add_error(None, 'Credenciais inválidas.')

        return render(request, 'login.html', {'form': form})

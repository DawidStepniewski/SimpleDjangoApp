from django.shortcuts import render, redirect
from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def log_in(request):
    if request.user.is_authenticated:
        return redirect('view_news')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password')
            )
            if user is not None:
                login(request, user)
                return redirect('view_news')
            else:
                context = {'form': form}
                return render(request, 'authentication/login.html', context)
        else:
            context = {'form': form}
            return render(request, 'authentication/login.html', context)
    else:
        context = {'form': LoginForm()}
        return render(request, 'authentication/login.html', context)


@login_required(login_url='/login/')
def log_out(request):
    if request.user.is_authenticated:
        logout(request)
        return render(request, 'authentication/logout.html')

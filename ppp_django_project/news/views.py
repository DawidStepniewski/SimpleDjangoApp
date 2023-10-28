from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import News
from .forms import NewsForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required


def index(request):
    news = News.objects.order_by('-create_time')
    context = {'news': news}
    return render(request, 'news/index.html', context)


@login_required(login_url='/login/')
def add(request):
    if request.method == 'POST':
        news = NewsForm(request.POST)
        if news.is_valid():
            news = news.save(commit=False)
            news.create_time = timezone.now()
            news.last_edit_time = timezone.now()
            news.save()
            return redirect('index')
        else:
            context = {'form': news}
            return render(request, 'news/add.html', context)
    else:
        news = NewsForm()
        context = {'form': news}
        return render(request, 'news/add.html', context)


@login_required
def edit(request, id):
    news = get_object_or_404(News, id=id)

    if request.method == 'GET':
        context = {'form': NewsForm(instance=news), 'id': id}
        return render(request, 'news/edit.html', context)

    elif request.method == 'POST':
        form = NewsForm(request.POST, instance=news)
        if form.is_valid():
            form.save()
            return render(request, 'news/index.html', {'news': News.objects.order_by('-create_time')})
        else:
            return render(request, 'news/edit.html', {'form': form})

def get(request, id):
    news = get_object_or_404(News, id=id)
    context = {'news': news}
    return render(request, 'news/view.html', context)

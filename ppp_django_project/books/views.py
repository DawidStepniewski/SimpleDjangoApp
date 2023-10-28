from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Books
from .forms import BooksForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required


def index(request):
    books = Books.objects.order_by('-create_time')
    context = {'books': books}
    return render(request, 'books/index.html', context)


@login_required(login_url='/login/')
def add(request):
    if request.method == 'POST':
        books = BooksForm(request.POST)
        if books.is_valid():
            books = books.save(commit=False)
            books.create_time = timezone.now()
            books.last_edit_time = timezone.now()
            books.save()
            return redirect('index')
        else:
            context = {'form': books}
            return render(request, 'books/add.html', context)
    else:
        books = BooksForm()
        context = {'form': books}
        return render(request, 'books/add.html', context)


@login_required
def edit(request, id):
    books = get_object_or_404(Books, id=id)

    if request.method == 'GET':
        context = {'form': BooksForm(instance=books), 'id': id}
        return render(request, 'news/edit.html', context)

    elif request.method == 'POST':
        form = BooksForm(request.POST, instance=books)
        if form.is_valid():
            form.save()
            return render(request, 'books/index.html', {'books': Books.objects.order_by('-create_time')})
        else:
            return render(request, 'books/edit.html', {'form': form})


@login_required
def get(request, id):
    books = get_object_or_404(Books, id=id)
    context = {'books': books}
    return render(request, 'books/view.html', context)


@login_required
def delete(request, id):
    books = get_object_or_404(Books, pk=id)
    context = {'books': books}

    if request.method == 'GET':
        return render(request, 'books/books_confirm_delete.html', context)
    elif request.method == 'POST':
        books.delete()
        return redirect('index')

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from books.forms import SearchForm, RatingForm
from books.models import Book, Rental, Rating


def book_list(request):
    books = Book.objects.all()
    per_page = request.GET.get('per_page', 3)
    page_number = request.GET.get('page', 1)
    paginator = Paginator(books, per_page, orphans=1)
    try:
        books = paginator.page(page_number)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)
    return render(request, 'books/book_list.html', {'books': books})


def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    form = RatingForm()
    return render(request, 'books/book_detail.html', {'book': book, 'form': form})


@login_required
def rent_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if book.stock > 0:
        rental = Rental(user=request.user, book=book)
        rental.save()
        book.stock -= 1
        book.save()
        return redirect('books:book_list')
    else:
        messages.error(request, f'{book.title} is no stock.')
        return redirect('books:book_list')


def rental_list(request):
    rentals = Rental.objects.filter(user=request.user)
    return render(request, 'books/rental_list.html', {'rentals': rentals})


def book_search(request):
    if request.method == 'GET':
        form = SearchForm()
    else:
        form = SearchForm(request.POST)
        if form.is_valid():
            query = request.POST.get('query', '')
            books = Book.objects.filter(title__icontains=query)
        else:
            books = []

        return render(request, 'books/book_search.html', {'books': books})


@require_POST
def rate_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    form = RatingForm(data=request.POST)
    if form.is_valid():
        rating = form.cleaned_data['rating']
        Rating.objects.create(user=request.user, book=book, rating=rating)
        return render(request, 'books/rate_book.html', {'book': book, 'rating': rating})

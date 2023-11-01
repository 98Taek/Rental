from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Avg
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from books.forms import SearchForm, RatingForm, ReviewForm
from books.models import Book, Rental, Rating, Review


def book_list(request):
    books = Book.objects.all()
    per_page = request.GET.get("per_page", 3)
    page_number = request.GET.get("page", 1)
    paginator = Paginator(books, per_page, orphans=1)
    try:
        books = paginator.page(page_number)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)
    return render(request, "books/book_list.html", {"books": books})


def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    form = RatingForm()
    review_form = ReviewForm()
    book.avg_rating = Rating.objects.filter(book=book).aggregate(
        avg_rating=Avg("rating")
    )["avg_rating"]
    reviews = Review.objects.filter(book=book)
    return render(
        request,
        "books/book_detail.html",
        {"book": book, "form": form, "review_form": review_form, "reviews": reviews},
    )


@login_required
def rent_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if book.stock > 0:
        rental = Rental(user=request.user, book=book)
        rental.save()
        book.stock -= 1
        book.save()
        return redirect("books:book_list")
    else:
        messages.error(request, f"{book.title} is no stock.")
        return redirect("books:book_list")


def rental_list(request):
    rentals = Rental.objects.filter(user=request.user)
    return render(request, "books/rental_list.html", {"rentals": rentals})


def book_search(request):
    if request.method == "GET":
        form = SearchForm()
    else:
        form = SearchForm(request.POST)
        if form.is_valid():
            query = request.POST.get("query", "")
            books = Book.objects.filter(title__icontains=query)
        else:
            books = []

        return render(request, "books/book_search.html", {"books": books})


@login_required
@require_POST
def rate_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    form = RatingForm(data=request.POST)
    try:
        if form.is_valid():
            rating = Rating.objects.get(user=request.user, book=book)
            form = RatingForm(data=request.POST, instance=rating)
            form.save()
            return redirect("books:book_detail", book_id=book_id)

    except Rating.DoesNotExist:
        if form.is_valid():
            form.instance.user = request.user
            form.instance.book = book
            form.save()
            return redirect("books:book_detail", book_id=book_id)


@login_required
@require_POST
def review_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    form = ReviewForm(data=request.POST)
    if form.is_valid():
        review = form.cleaned_data["body"]
        Review.objects.create(user=request.user, book=book, body=review)
        return render(
            request, "books/review_book.html", {"book": book, "review": review}
        )
    return redirect("books:book_detail", book_id)


@login_required
@require_POST
def delete_review(request, review_id, book_id):
    review = get_object_or_404(Review, id=review_id)
    if review.user == request.user:
        review.delete()
    else:
        messages.error(request, "Only review authors can be deleted.")
    return redirect("books:book_detail", book_id)


@login_required
def profile(request, user_id):
    reviews = Review.objects.filter(user_id=user_id)
    ratings = Rating.objects.filter(user_id=user_id)
    rentals = Rental.objects.filter(user_id=user_id).count()
    return render(
        request,
        "books/profile.html",
        {"reviews": reviews, "ratings": ratings, "rentals": rentals},
    )

from django.urls import path

from books import views

app_name = 'books'

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('rental_list/', views.rental_list, name='rental_list'),
    path('books/search/', views.book_search, name='book_search'),
    path('books/<book_id>/', views.book_detail, name='book_detail'),
    path('books/<book_id>/rent/', views.rent_book, name='rent_book'),
    path('books/<book_id>/rate/', views.rate_book, name='rate_book'),
]
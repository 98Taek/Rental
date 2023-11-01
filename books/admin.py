from django.contrib import admin

from books.models import Book, Rental, Rating, Review
from books.tasks import return_book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "publisher", "stock"]


@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ["user", "get_book_title", "rental_date", "return_date"]
    actions = ["return_book_action"]

    def get_book_title(self, obj):
        return obj.book.title

    get_book_title.short_description = "Book Title"

    def return_book_action(self, request, queryset):
        for rental in queryset:
            rental.book.stock += 1
            rental.book.save()
            return_book.delay(rental.id)

        self.message_user(request, f"Successfully returned {len(queryset)} rentals.")

    return_book_action.short_description = "Return selected rentals"


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ["user", "book", "rating"]
    list_filter = ["user", "book"]
    search_fields = ["user", "book"]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["user", "book", "body", "created"]
    list_filter = ["user", "book"]
    search_fields = ["user", "book"]

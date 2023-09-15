from django.contrib import admin

from books.models import Book, Rental
from books.tasks import return_book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'publisher', 'stock']


@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_book_title', 'rental_date', 'return_date']
    actions = ['return_book_action']

    def get_book_title(self, obj):
        return obj.book.title

    get_book_title.short_description = 'Book Title'

    def return_book_action(self, request, queryset):
        for rental in queryset:
            rental.book.stock += 1
            rental.book.save()
            result = return_book.apply_async(args=[rental.id])
            result.get()
            rental.delete()

        self.message_user(request, f'Successfully returned {len(queryset)} rentals.')

    return_book_action.short_description = 'Return selected rentals'

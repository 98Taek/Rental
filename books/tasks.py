from celery import shared_task
from django.core.mail import send_mail

from books.models import Rental


@shared_task
def return_book(rental_id):
    rental = Rental.objects.get(id=rental_id)
    subject = f'Dear {rental.user.username}'
    message = f'Return {rental.book.title}\n\n' \
              f'You have successfully returned the book.'
    mail_sent = send_mail(subject, message, 'admin@example.com', [rental.user.email])
    return mail_sent

from celery import shared_task
from django.core.mail import send_mail
from .models import Order
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from io import BytesIO

@shared_task
def send_emails(order_id) -> str:
    order = Order.objects.get(order_id=order_id)
    subject = f'Order ID: {order.order_id}'
    message = f'Dear {order.get_full_name()}, \n You Have Message Successfuly Placed An Order. \n Your Order ID Is: {order.order_id}'
    from_email = settings.DEFAULT_FROM_EMAIL

    mail_sent = send_mail(subject, message, from_email, [order.email])
    return mail_sent


@shared_task
def payment_completed(order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return False

    subject = f'My Shop - Invoice {order.order_id}'
    message = f'Hello {order.get_full_name()},\nPlease find attached the invoice.'
    from_email = settings.DEFAULT_FROM_EMAIL
    email_user = [order.email]

    html = render_to_string("orders/pdf.html", {"order": order})

    out = BytesIO()
    pisa.CreatePDF(src=html, dest=out)

    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=from_email,
        to=email_user,
    )

    email.attach(
        f'order_{order.order_id}.pdf',
        out.getvalue(),
        'application/pdf'
    )

    email.send()
    return True
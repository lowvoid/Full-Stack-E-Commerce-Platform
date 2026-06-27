from django.shortcuts import render , get_object_or_404 , redirect
from .models import OrderItem , Order
from .forms import OrderCreateForm , OrderPayForm
from cart.cart import Cart
from django.core.mail import send_mail
from django.conf import settings 
from .tasks import send_emails , payment_completed
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.admin.views.decorators import staff_member_required
# import weasyprint
import os
from xhtml2pdf import pisa
# from django.template.loader import render_to_string
# from django.http import HttpResponse

def admin_order_pdf(request, order_id):
    order = Order.objects.get(id=order_id)

    html = render_to_string("orders/pdf.html", {"order": order})

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'filename="order_{order.order_id}.pdf"'

    pisa.CreatePDF(html, dest=response)

    return response





def order_create(request):
    cart = Cart(request)

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)

        if form.is_valid():
            order = form.save()

            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )

            order_id = order.order_id

            send_emails.delay(order_id)

            cart.clear()

            return redirect(
                'orders:pay_order',
                order_id=order.id
            )

    else:
        form = OrderCreateForm()

    return render(
        request,
        'orders/create.html',
        {
            'form': form,
            'cart': cart,
            'success': False
        }
    )


def order_pay_by_vodafone(request, order_id):
    order = get_object_or_404(Order,id=order_id)
    if request.method == 'POST':
        form = OrderPayForm(request.POST, request.FILES)
        if form.is_valid():
            order_pay = form.save(commit=False)
            order_pay.order = order
            order_pay.paid = True
            order_pay.save()
            return redirect('orders:payment_success',order_id=order_id)
    else:
        form = OrderPayForm()


    context = {
        'order': order ,
        'form': form ,
    }
    return render(request, 'orders/pay_form.html', context)


def payment_success(request, order_id):
    order = get_object_or_404(Order, id =order_id)
    payment_completed.delay(order.id)
    return render(request, 'orders/payment_success.html', {'order':order})
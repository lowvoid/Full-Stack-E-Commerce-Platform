from django.urls import path
from .views import order_create , order_pay_by_vodafone , payment_success ,admin_order_pdf

app_name = "orders"


urlpatterns = [
    path('create/',order_create, name="order_create"),
    path('pay-order/<int:order_id>/',order_pay_by_vodafone, name="pay_order"),
    path('payment-success/<int:order_id>/', payment_success, name="payment_success"),
    path('admin/pdf/<int:order_id>/',admin_order_pdf,name="admin_order_pdf")
]

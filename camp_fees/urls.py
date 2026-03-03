from django.urls import path
from .views import my_fees
from .views import my_fees, download_fee_receipt

urlpatterns = [
    path("my/", my_fees, name="my_fees"),
    path("receipt/", download_fee_receipt, name="fee_receipt"),
]

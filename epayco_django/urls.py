from django.conf.urls import url

from .views import ConfirmationView

# app_name = 'epayco_django' # If i include this it will not find the urls.
urlpatterns = [
    url('^epayco/confirmation$', ConfirmationView.as_view(), name='epayco_confirmation'),
    url('^payment/response-validation', ConfirmationView.as_view(), name='epayco_response_validation'),
]

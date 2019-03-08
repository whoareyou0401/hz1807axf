from django.conf.urls import url
from .apis import *
urlpatterns = [
    url(r"^register$", RegisterAPI.as_view(), name="register"),
    url(r"^login$", LoginAPI.as_view() ),
    url(r"^cart-item$", ItemCartAPI.as_view()),
    url(r"^cart/status$", CartItemStatusAPI.as_view()),
    url(r"^cart-status$", cart_data_status_api),
    url(r"^cart/options$", CartDataOptionAPI.as_view()),
    url(r"^orderitem/(?P<pk>\d+)", OrderItemAPI.as_view())
]
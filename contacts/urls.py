from django.urls import path
from .views import ContactCreate,ContactDetail,CheckContactDetail,SpamCounterView

urlpatterns = [
    path('contact_detail/', ContactDetail.as_view(), name='contact_detail'),
    path('contact_list/', ContactCreate.as_view(), name='contact_create'),
    path('check_contact/', CheckContactDetail.as_view(), name='check_contact'),
    path('spam_number/', SpamCounterView.as_view(), name='spam_number')

]
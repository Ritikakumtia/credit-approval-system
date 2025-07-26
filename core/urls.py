from django.urls import path
from core.views import (
    RegisterCustomerView,
    check_eligibility,
    create_loan,
    view_loans_by_customer,
    view_loan,
    root_view
)

urlpatterns = [
    path("", root_view),
    path('register/', RegisterCustomerView.as_view(), name='register-customer'),
    path('check-eligibility/', check_eligibility),
    path('create-loan/', create_loan),
    path('view-loans/<int:customer_id>/', view_loans_by_customer),
    path('view-loan/<int:loan_id>/', view_loan),
]

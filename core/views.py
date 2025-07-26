# core/views.py
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Customer, Loan
from .serializers import CustomerSerializer
import math
from django.http import JsonResponse
from datetime import datetime, timedelta

def register_customer(request):
    return JsonResponse({"message": "Register endpoint placeholder"})

def root_view(request):
    return JsonResponse({"message": "Welcome to the Credit Approval System API"})

@api_view(['POST'])
def check_eligibility(request):
    data = request.data
    customer_id = data['customer_id']
    loan_amount = float(data['loan_amount'])
    interest_rate = float(data['interest_rate'])
    tenure = int(data['tenure'])

    try:
        customer = Customer.objects.get(customer_id=customer_id)
    except Customer.DoesNotExist:
        return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)

    past_loans = Loan.objects.filter(customer=customer)
    on_time_emis = sum(loan.emis_paid_on_time for loan in past_loans)
    total_loans = past_loans.count()
    current_year_loans = past_loans.filter(start_date__year=datetime.now().year).count()
    approved_volume = sum(loan.loan_amount for loan in past_loans)

    credit_score = 100
    if customer.current_debt > customer.approved_limit:
        credit_score = 0
    else:
        credit_score -= (total_loans * 5)
        credit_score += (on_time_emis * 1)
        credit_score += (current_year_loans * 2)
        credit_score += (approved_volume / 100000)

    P = loan_amount
    R = interest_rate / (12 * 100)
    N = tenure
    try:
        emi = (P * R * (1 + R)**N) / ((1 + R)**N - 1)
    except ZeroDivisionError:
        emi = P / N

    if emi * N + customer.current_debt > customer.approved_limit or emi > 0.5 * customer.monthly_salary:
        return Response({
            "customer_id": customer_id,
            "approval": False,
            "message": "Loan not approved due to income or credit limit constraints",
        })

    corrected_interest_rate = interest_rate
    approval = False

    if credit_score > 50:
        approval = True
    elif 30 < credit_score <= 50:
        corrected_interest_rate = max(interest_rate, 12)
        approval = True
    elif 10 < credit_score <= 30:
        corrected_interest_rate = max(interest_rate, 16)
        approval = True

    return Response({
        "customer_id": customer_id,
        "approval": approval,
        "interest_rate": interest_rate,
        "corrected_interest_rate": corrected_interest_rate,
        "tenure": tenure,
        "monthly_installment": round(emi, 2)
    })

@api_view(['POST'])
def create_loan(request):
    data = request.data
    customer_id = data.get('customer_id')
    loan_amount = float(data.get('loan_amount'))
    interest_rate = float(data.get('interest_rate'))
    tenure = int(data.get('tenure'))

    try:
        customer = Customer.objects.get(customer_id=customer_id)
    except Customer.DoesNotExist:
        return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)

    past_loans = Loan.objects.filter(customer=customer)
    on_time_emis = sum(loan.emis_paid_on_time for loan in past_loans)
    total_loans = past_loans.count()
    current_year_loans = past_loans.filter(start_date__year=datetime.now().year).count()
    approved_volume = sum(loan.loan_amount for loan in past_loans)

    credit_score = 100
    if customer.current_debt > customer.approved_limit:
        credit_score = 0
    else:
        credit_score -= (total_loans * 5)
        credit_score += (on_time_emis * 1)
        credit_score += (current_year_loans * 2)
        credit_score += (approved_volume / 100000)

    P = loan_amount
    R = interest_rate / (12 * 100)
    N = tenure
    try:
        emi = (P * R * (1 + R) ** N) / ((1 + R) ** N - 1)
    except ZeroDivisionError:
        emi = P / N

    if emi * N + customer.current_debt > customer.approved_limit or emi > 0.5 * customer.monthly_salary:
        return Response({
            "loan_id": None,
            "customer_id": customer_id,
            "loan_approved": False,
            "message": "Loan not approved due to income or credit limit constraints",
            "monthly_installment": 0
        }, status=status.HTTP_400_BAD_REQUEST)

    approved = False
    if credit_score > 50:
        approved = True
    elif 30 < credit_score <= 50 and interest_rate >= 12:
        approved = True
    elif 10 < credit_score <= 30 and interest_rate >= 16:
        approved = True

    if not approved:
        return Response({
            "loan_id": None,
            "customer_id": customer_id,
            "loan_approved": False,
            "message": "Loan not approved due to credit score restrictions",
            "monthly_installment": 0
        }, status=status.HTTP_400_BAD_REQUEST)

    loan = Loan.objects.create(
        customer=customer,
        loan_amount=loan_amount,
        interest_rate=interest_rate,
        tenure=tenure,
        start_date=datetime.today().date(),
        end_date=(datetime.today() + timedelta(days=30 * tenure)).date(),
        emis_paid_on_time=0,
        monthly_repayment=round(emi, 2)
    )

    customer.current_debt += loan_amount
    customer.save()

    return Response({
        "loan_id": loan.loan_id,
        "customer_id": customer_id,
        "loan_approved": True,
        "message": "Loan approved successfully",
        "monthly_installment": round(emi, 2)
    }, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def view_loan(request, loan_id):
    try:
        loan = Loan.objects.get(loan_id=loan_id)
        customer = loan.customer
    except Loan.DoesNotExist:
        return Response({'error': 'Loan not found'}, status=status.HTTP_404_NOT_FOUND)

    data = {
        "loan_id": loan.loan_id,
        "customer": {
            "customer_id": customer.customer_id,
            "first_name": customer.first_name,
            "last_name": customer.last_name,
            "phone_number": customer.phone_number,
            "age": customer.age,
        },
        "loan_amount": loan.loan_amount,
        "interest_rate": loan.interest_rate,
        "monthly_installment": loan.monthly_repayment,
        "tenure": loan.tenure
    }

    return Response(data, status=status.HTTP_200_OK)

@api_view(['GET'])
def view_loans_by_customer(request, customer_id):
    try:
        customer = Customer.objects.get(customer_id=customer_id)
    except Customer.DoesNotExist:
        return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)

    loans = Loan.objects.filter(customer=customer)
    response_data = []

    for loan in loans:
        today = datetime.today().date()
        repayments_left = max(0, ((loan.end_date.year - today.year) * 12 + (loan.end_date.month - today.month))) if today < loan.end_date else 0

        response_data.append({
            "loan_id": loan.loan_id,
            "loan_amount": loan.loan_amount,
            "interest_rate": loan.interest_rate,
            "monthly_installment": loan.monthly_repayment,
            "repayments_left": repayments_left
        })

    return Response(response_data, status=status.HTTP_200_OK)

class RegisterCustomerView(APIView):
    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            customer = serializer.save()
            return Response(CustomerSerializer(customer).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

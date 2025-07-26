# core/serializers.py

from rest_framework import serializers
from core.models import Customer
import math
from core.models import Loan 
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            'customer_id',
            'first_name',
            'last_name',
            'age',
            'phone_number',
            'monthly_income',
            'approved_limit'
        ]
        read_only_fields = ['customer_id', 'approved_limit']

    def create(self, validated_data):
        salary = validated_data['monthly_income']
        approved_limit = int(round((salary * 36) / 100000.0)) * 100000  # Round to nearest lakh
        validated_data['approved_limit'] = approved_limit
        return super().create(validated_data)
class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = [
            'id',
            'customer',
            'loan_amount',
            'tenure',
            'interest_rate',
            'monthly_installment',
            'start_date',
            'end_date',
            'emis_paid_on_time',
            'loan_approved'
        ]
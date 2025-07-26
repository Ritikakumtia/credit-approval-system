import pandas as pd
from celery import shared_task
from core.models import Customer, Loan

@shared_task
def load_initial_data():
    df_customers = pd.read_excel('customer_data.xlsx')
    print("Loaded customer rows:", len(df_customers))

    customers = []
    for _, row in df_customers.iterrows():
        print("Importing customer:", row['Customer ID'])
        customers.append(Customer(
            customer_id=int(row['Customer ID']),
            first_name=row['First Name'],
            last_name=row['Last Name'],
            phone_number=str(row['Phone Number']),
            age=int(row['Age']),
            monthly_income=int(row['Monthly Salary']),
            approved_limit=int(row['Approved Limit']),
        ))
    Customer.objects.bulk_create(customers, ignore_conflicts=True)

    df_loans = pd.read_excel('loan_data.xlsx')
    print("Loaded loan rows:", len(df_loans))

    loans = []
    for _, row in df_loans.iterrows():
        print("Importing loan for customer ID:", row['Customer ID'])

        loans.append(Loan(
            customer_id=int(row['Customer ID']),                      # ✅ valid field
            loan_amount=float(row['Loan Amount']),                    # ✅ valid field
            tenure=int(row['Tenure']),                                # ✅ valid field
            interest_rate=float(row['Interest Rate']),                # ✅ valid field
            monthly_installment=float(row['Monthly payment']),        # ✅ field in model
            start_date=row['Date of Approval'],                       # ✅ valid field
            end_date=row['End Date'],                                 # ✅ valid field
            emis_paid_on_time=int(row['EMIs paid on Time']),          # ✅ valid field
            loan_approved=True                                        # ✅ optional logic
        ))
    Loan.objects.bulk_create(loans, ignore_conflicts=True)

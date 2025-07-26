from django.core.management.base import BaseCommand
import pandas as pd
from core.models import Loan, Customer

print("✅ Loan ingestion script loaded")

class Command(BaseCommand):
    help = 'Load loan data from Excel'

    def handle(self, *args, **kwargs):
        print("📌 handle() called for loan ingestion")
        try:
            df = pd.read_excel('loan_data.xlsx')
            print(f"🧾 Loan Excel Columns: {df.columns.tolist()}")

            for _, row in df.iterrows():
                try:
                    customer = Customer.objects.get(customer_id=row['Customer ID'])
                except Customer.DoesNotExist:
                    print(f"❌ Customer ID {row['Customer ID']} not found. Skipping.")
                    continue

                try:
                    Loan.objects.update_or_create(
    loan_id=row['Loan ID'],
    defaults={
        'customer': customer,
        'loan_amount': row['Loan Amount'],
        'tenure': row['Tenure'],
        'interest_rate': row['Interest Rate'],
        'monthly_emi': row['Monthly payment'],  # ✅ This one!
        'start_date': pd.to_datetime(row['Date of Approval']),
        'end_date': pd.to_datetime(row['End Date']),
        'status': 'PAID'  # Or use a status column if available
    }
)

                except Exception as e:
                    print(f"❌ Error saving loan {row['Loan ID']}: {e}")
                    continue

            self.stdout.write(self.style.SUCCESS('✅ Loan data loaded successfully.'))

        except Exception as e:
            import traceback
            traceback.print_exc()
            self.stdout.write(self.style.ERROR(f'❌ Error loading loan data: {e}'))

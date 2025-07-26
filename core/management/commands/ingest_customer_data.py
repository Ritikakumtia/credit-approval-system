from django.core.management.base import BaseCommand
import pandas as pd
from core.models import Customer

print("✅ Python script is loaded")

class Command(BaseCommand):
    help = 'Load customers from Excel'

    def handle(self, *args, **kwargs):
        print("📌 handle() called")
        try:
            df = pd.read_excel('customer_data.xlsx')
            print(f"🧾 Excel Columns: {df.columns.tolist()}")

            for _, row in df.iterrows():
                Customer.objects.update_or_create(
                    customer_id=row['Customer ID'],
                    defaults={
                        'first_name': row['First Name'],
                        'last_name': row['Last Name'],
                        'phone_number': row['Phone Number'],
                        'monthly_income': row['Monthly Salary'],
                        'approved_limit': row['Approved Limit'],
                        'current_debt': 0  # ✅ Set to 0 manually
                    }
                )

            self.stdout.write(self.style.SUCCESS('✅ Customer data loaded.'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error loading customer data: {e}'))

# credit-approval-system
A Django REST backend for credit approval with Docker &amp; PostgreSQL
# 💳 Credit Approval System (Backend Only)

A Django 4.x + DRF + PostgreSQL backend application that evaluates loan eligibility, processes loans, and stores customer and loan data. The system supports background ingestion of Excel files and provides multiple API endpoints.

---

## 🚀 Features

- ✅ Customer Registration (`/register`)
- ✅ Loan Eligibility Check (`/check-eligibility`)
- ✅ Loan Creation (`/create-loan`)
- ✅ View Loan by Loan ID (`/view-loan/<loan_id>`)
- ✅ View All Loans by Customer ID (`/view-loans/<customer_id>`)
- ✅ Background ingestion of `customer_data.xlsx` and `loan_data.xlsx`
- ✅ Dockerized app with PostgreSQL
- ✅ Compound interest logic for EMI calculations

---

## 🏗️ Tech Stack

- Python 3.10+
- Django 4.x
- Django REST Framework
- PostgreSQL
- Celery (for background ingestion)
- Docker + Docker Compose

---

## 🐳 Docker Setup

```bash
# Clone the repo
git clone https://github.com/Ritikakumtia/credit-approval-system.git
cd credit-approval-system

# Build and run the app
docker-compose up --build

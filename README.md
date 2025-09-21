# Finance App

**Finance App** – shaxsiy moliya boshqaruvi ilovasi. Foydalanuvchi daromad va xarajatlarini kuzatadi, kategoriyalarga ajratadi va statistikani ko‘radi. Django va Django REST Framework asosida yaratilgan.

---

## 🛠 Texnologiyalar

- Python 3.11+
- Django 4.2+
- Django REST Framework
- djangorestframework-simplejwt (JWT auth)
- SQLite (lokal DB)
- Tailwind CSS (frontend)

---

## ⚡ Xususiyatlar

1. **Authentication**
   - JWT login/logout
   - Token refresh
   - Signup: email/phone orqali 6 xonali tasdiqlash kodi
   - Profile update, password reset

2. **Finance Management**
   - Categories (Income / Expense)
   - Budgets
   - Transactions
   - Oxirgi 5 ta tranzaksiya
   - Income / Expense alohida filtrlash
   - Summary va daily stats (kunlik, start-end date)

---

## 📌 API Endpoints

Base URL: `/api/transactions/`  

| Endpoint            | Method | Description |
|--------------------|--------|------------|
| `/categories/`      | GET, POST, PUT, DELETE | Categories CRUD |
| `/budgets/`         | GET, POST, PUT, DELETE | Budgets CRUD |
| `/transactions/`    | GET, POST, PUT, DELETE | Transactions CRUD |
| `/transactions/income/` | GET | Faqat INCOME lar |
| `/transactions/expense/`| GET | Faqat EXPENSE lar |
| `/transactions/summary/`| GET | Umumiy balans, income va expense |
| `/transactions/daily_stats/?date=YYYY-MM-DD` | GET | Tanlangan kun statistika |
| `/transactions/last/` | GET | Oxirgi 5 ta tranzaksiya |

---

## 🚀 O‘rnatish

1. Klonlash:

```bash
git clone https://github.com/yourusername/finance_app_MVT.git
cd finance_app

python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate

python manage.py createsuperuser


python manage.py runserver

# MediConnect - Crowed Based Medicine Finder

MediConnect is a premium, dark-themed healthcare management platform designed to connect users with local pharmacies. It features a modern glassmorphism design and handles everything from medicine discovery to secure delivery tracking.

## 🌟 Key Features

### 👤 Multi-Role Dashboard

- **Admin**: Manage pharmacies, verify delivery personnel, and monitor system analytics.
- **Pharmacy**: Manage inventory, stock reservation, and incoming orders.
- **User**: Search for medicines, upload prescriptions, and track active deliveries.
- **Delivery Boy**: Manage assigned deliveries, navigate using user addresses, and update real-time status.

### 💊 Core Functionalities

- **Real-time Stock Management**: Automatic deduction upon booking and restoration on cancellation.
- **Prescription System**: Secure prescription upload for restricted medicines with pharmacist approval workflow.
- **Smart Delivery Tracking**: Real-time status updates (Picked Up, On the Way, Delivered) with user confirmation.
- **Invoice Management**: Automated generation of separate invoices for each payment transaction.
- **Profile Customization**: Detailed profiles with image support for both users and pharmacies.

## 🛠️ Tech Stack

- **Backend**: Python 3.x, Django 4.x
- **Database**: SQLite (Development) / PostgreSQL (Production ready)
- **Frontend**: HTML5, CSS3 (Custom Glassmorphism Design System), Vanilla JavaScript
- **Icons & UI**: FontAwesome, Google Fonts (Inter)

## 🚀 Getting Started

### Prerequisites

- Python installed on your machine.
- Git.

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/VishnuSuresh0204/crowed-based-medicine-finder.git
   cd medicine
   ```

2. **Setup virtual environment (Optional but Recommended)**

   ```bash
   python -m venv env
   source env/bin/activate  # On Windows use: env\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install django pillow
   ```

4. **Database Migrations**

   ```bash
   cd medi
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Run the Development Server**
   ```bash
   python manage.py runserver
   ```

## 🎨 Design Philosophy

MediConnect utilizes a **Premium Dark Glassmorphism** aesthetic. The UI focuses on high contrast, translucency, and vibrant gradients to provide a modern, high-end feel for healthcare management.

## 📄 License

This project is for educational/demonstration purposes.

---

_Developed with ❤️ for Advanced Healthcare Solutions._

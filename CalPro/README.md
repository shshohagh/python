# CalPro - Calorie Counter & Diet Tracker

CalPro is a comprehensive, feature-rich Django web application designed to help users track their daily dietary intake, monitor their macros, and achieve their health goals. It features a modern, premium **Glassmorphism** UI design.

## 🚀 Features

- **User Authentication & Profiles**: Secure registration and login system. Users can maintain personalized profiles with their height, weight, age, and target weight to automatically calculate their **BMR (Basal Metabolic Rate)**.
- **Daily Dashboard**: A beautifully designed dashboard that tracks daily calorie consumption against the user's required BMR.
- **Food Logging & API Integration**: Log food items easily. Includes built-in integration with the **OpenFoodFacts API** to instantly fetch nutrition data (Calories, Protein, Carbs, Fats) by simply searching for a food item.
- **Macronutrient Tracking**: Monitor your daily intake of Proteins, Carbohydrates, and Fats with visual progress bars.
- **Analytics & Charts**: Dedicated analytics page utilizing **Chart.js** to visualize your last 7 days of calorie trends and macronutrient distribution.
- **Water & Weight Logging**: Keep track of daily water intake (by glasses) and log body weight over time.
- **Custom Meal Categories**: Categorize your meals (e.g., Breakfast, Lunch, Dinner, Snack) with custom colors and icons.
- **Data Export**: Export your complete food log history as a CSV file for personal records.

## 💻 Tech Stack

- **Backend**: Python, Django
- **Frontend**: HTML5, Vanilla CSS (Glassmorphism design), Bootstrap 5, Vanilla JavaScript
- **Database**: SQLite (Default)
- **Data Visualization**: Chart.js
- **External API**: OpenFoodFacts API

## 🛠️ Setup & Installation

Follow these steps to run the project locally on your machine.

### 1. Prerequisites
Ensure you have Python installed on your computer.

### 2. Create a Virtual Environment
It is recommended to use a virtual environment to manage dependencies.
```bash
# Create the virtual environment
python -m venv virtual

# Activate the virtual environment (Windows)
virtual\Scripts\activate

# Activate the virtual environment (Mac/Linux)
source virtual/bin/activate
```

### 3. Install Dependencies
```bash
pip install django
```
*(Note: If you plan to extend the project with APIs later, you may also install `djangorestframework`)*

### 4. Database Setup
Apply the migrations to set up your SQLite database.
```bash
cd CalPro
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a Superuser (Admin)
Create an admin account to access the Django backend panel.
```bash
python manage.py createsuperuser
```

### 6. Run the Server
Start the development server.
```bash
python manage.py runserver
```
Navigate to `http://127.0.0.1:8000/` in your web browser to view the application!

## 🎨 Design System

The frontend strictly adheres to a modern **Glassmorphism** aesthetic:
- **Colors**: Primary Indigo/Purple (`#6366f1`), Accent Amber (`#f59e0b`), and a multi-color radial-gradient background (`#f1f5f9`).
- **Typography**: Uses the 'Outfit' font family for a clean, geometric look.
- **UI Components**: Features translucent backgrounds `rgba(255, 255, 255, 0.6 to 0.85)` with `backdrop-filter: blur(...)` to create the frosted glass effect.

## 📄 License
This project is for educational and personal use.

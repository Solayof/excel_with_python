# 📊 Comprehensive High School Igbope Broadsheet Management System

This is a web-based application built with **Streamlit** to help manage student information, upload academic scores, and generate downloadable result sheets. It is tailored for **Comprehensive High School Igbope** and streamlines academic data management across all classes and subjects.

---

## 📌 Features

### 🔧 Class Management

- Add and manage class groups (e.g., JSS 1A, SSS 3B).
- View class lists and student records.

### 🧑‍🎓 Student Management

- Register new students to a class.
- Edit and update student details.
- Delete student records if needed.

### 📝 Score Management

- Upload academic scores per student for each subject:
  - Continuous Assessment (CA)
  - Exam scores
  - First and Second Term scores
- Update previously uploaded scores.

### 📄 Sheet Generation

- Generate Excel (.xlsx) result sheets per class.
- Download result sheets for printing or archiving.

### 📈 Data Display

- View detailed scores for individual students.
- View the full student list per class.

---

---

## 🛠️ Built With

- **Python 3**
- **Streamlit** – for building interactive UI
- **Pandas** – for data handling and table rendering
- **Sqlalchemy** – for data persistence (via `storage.py`)
- **openpyxl** – read, write and generate to excel file

---

## 🚀 Getting Started

### ✅ Prerequisites

- Python 3.7+
- pip

### 📥 Installation

1. Clone the Repository

```bash
git clone https://github.com/solayof/excel_with_python.git
cd excel_with_python

pip install -r requirements.txt

streamlit run CHS_IGBOPE_PORTAL.py
```

## 📚 How to Use

1. Add Class: Create new class sections like JSS 1 A, SSS 2 C, etc.

2. Add Students: Enter student details and assign them to their class.

3. Upload Scores: Add subject scores for a student. Scores include CA, exam, and first/second term values.

4. Edit or Update: Modify student details or subject scores as needed.

5. Generate & Download Sheets: Create and download performance result sheets per class.

6. View Data: Browse through student scores or class lists directly in the app.

## ⚠️ Notes

- Admission numbers must be unique.

- A student should not be assigned duplicate subjects in the same term.

- Sheets must be regenerated after each score update to ensure accuracy.

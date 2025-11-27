import sys
import os
import json
import datetime
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QTextEdit, QPushButton, 
                             QFileDialog, QMessageBox, QListWidget, QStackedWidget)
from PyQt5.QtCore import Qt

PROFILE_DIR = "profiles"

class ProfileSelectionWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.profile_data = None
        self.profile_filename = None
        self.initUI()
        
        # Ensure profile directory exists
        if not os.path.exists(PROFILE_DIR):
            os.makedirs(PROFILE_DIR)

    def initUI(self):
        self.setWindowTitle("AI Interview Assistant - Profile Selection")
        self.setGeometry(300, 300, 500, 400)
        self.setStyleSheet("background-color: #2b2b2b; color: #ffffff;")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Title
        title = QLabel("Welcome to AI Interview Assistant")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 20px; color: #00ffff;")
        self.layout.addWidget(title)

        # Stacked Widget to switch between Selection and Form
        self.stacked_widget = QStackedWidget()
        self.layout.addWidget(self.stacked_widget)

        # Page 1: Selection (Add / Load)
        self.selection_page = QWidget()
        self.selection_layout = QVBoxLayout()
        self.selection_page.setLayout(self.selection_layout)

        btn_style = """
            QPushButton {
                background-color: #3d3d3d;
                color: white;
                border: 1px solid #555;
                padding: 15px;
                font-size: 16px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #4d4d4d;
                border: 1px solid #00ffff;
            }
        """

        self.btn_create = QPushButton("Create New Profile")
        self.btn_create.setStyleSheet(btn_style)
        self.btn_create.clicked.connect(self.show_create_form)
        self.selection_layout.addWidget(self.btn_create)

        self.btn_load = QPushButton("Load Existing Profile")
        self.btn_load.setStyleSheet(btn_style)
        self.btn_load.clicked.connect(self.show_load_list)
        self.selection_layout.addWidget(self.btn_load)

        self.stacked_widget.addWidget(self.selection_page)

        # Page 2: Create Form
        self.form_page = QWidget()
        self.form_layout = QVBoxLayout()
        self.form_page.setLayout(self.form_layout)
        
        self.setup_form()
        
        self.stacked_widget.addWidget(self.form_page)

        # Page 3: Load List
        self.load_page = QWidget()
        self.load_layout = QVBoxLayout()
        self.load_page.setLayout(self.load_layout)
        
        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet("background-color: #3d3d3d; color: white; font-size: 14px;")
        self.load_layout.addWidget(self.list_widget)
        
        self.btn_load_confirm = QPushButton("Load Selected")
        self.btn_load_confirm.setStyleSheet(btn_style)
        self.btn_load_confirm.clicked.connect(self.load_selected_profile)
        self.load_layout.addWidget(self.btn_load_confirm)
        
        self.btn_back_load = QPushButton("Back")
        self.btn_back_load.setStyleSheet("background-color: #555; color: white; padding: 5px;")
        self.btn_back_load.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.load_layout.addWidget(self.btn_back_load)

        self.stacked_widget.addWidget(self.load_page)

    def setup_form(self):
        input_style = "background-color: #3d3d3d; color: white; border: 1px solid #555; padding: 5px;"
        label_style = "font-weight: bold; margin-top: 10px;"

        # Name
        self.form_layout.addWidget(QLabel("Full Name:", styleSheet=label_style))
        self.inp_name = QLineEdit()
        self.inp_name.setStyleSheet(input_style)
        self.form_layout.addWidget(self.inp_name)

        # Intro
        self.form_layout.addWidget(QLabel("Short Intro (e.g. 'I am a backend dev...'):", styleSheet=label_style))
        self.inp_intro = QTextEdit()
        self.inp_intro.setMaximumHeight(60)
        self.inp_intro.setStyleSheet(input_style)
        self.form_layout.addWidget(self.inp_intro)

        # Company / Designation
        self.form_layout.addWidget(QLabel("Current Company & Designation:", styleSheet=label_style))
        self.inp_company = QLineEdit()
        self.inp_company.setStyleSheet(input_style)
        self.form_layout.addWidget(self.inp_company)
        
        # Skills
        self.form_layout.addWidget(QLabel("Key Skills (comma separated):", styleSheet=label_style))
        self.inp_skills = QLineEdit()
        self.inp_skills.setStyleSheet(input_style)
        self.form_layout.addWidget(self.inp_skills)
        
        # Projects
        self.form_layout.addWidget(QLabel("Key Projects (Brief summary):", styleSheet=label_style))
        self.inp_projects = QTextEdit()
        self.inp_projects.setStyleSheet(input_style)
        self.form_layout.addWidget(self.inp_projects)

        # Buttons
        btn_box = QHBoxLayout()
        self.btn_save = QPushButton("Save & Start")
        self.btn_save.setStyleSheet("background-color: #008000; color: white; padding: 10px; font-weight: bold;")
        self.btn_save.clicked.connect(self.save_profile)
        
        self.btn_back_form = QPushButton("Back")
        self.btn_back_form.setStyleSheet("background-color: #555; color: white; padding: 10px;")
        self.btn_back_form.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        
        btn_box.addWidget(self.btn_back_form)
        btn_box.addWidget(self.btn_save)
        self.form_layout.addLayout(btn_box)

    def show_create_form(self):
        self.stacked_widget.setCurrentIndex(1)

    def show_load_list(self):
        self.list_widget.clear()
        files = [f for f in os.listdir(PROFILE_DIR) if f.endswith('.json')]
        if not files:
            QMessageBox.information(self, "No Profiles", "No saved profiles found.")
            return
        self.list_widget.addItems(files)
        self.stacked_widget.setCurrentIndex(2)

    def save_profile(self):
        name = self.inp_name.text().strip()
        if not name:
            QMessageBox.warning(self, "Error", "Name is required!")
            return

        data = {
            "name": name,
            "intro": self.inp_intro.toPlainText().strip(),
            "company": self.inp_company.text().strip(),
            "skills": self.inp_skills.text().strip(),
            "projects": self.inp_projects.toPlainText().strip()
        }

        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        filename = f"{name}_{date_str}.json".replace(" ", "_")
        filepath = os.path.join(PROFILE_DIR, filename)

        try:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=4)
            
            self.profile_data = data
            self.profile_filename = filename
            self.close() # Close window to proceed
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save profile: {e}")

    def load_selected_profile(self):
        selected_item = self.list_widget.currentItem()
        if not selected_item:
            return
        
        filename = selected_item.text()
        filepath = os.path.join(PROFILE_DIR, filename)
        
        try:
            with open(filepath, 'r') as f:
                self.profile_data = json.load(f)
            self.profile_filename = filename
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load profile: {e}")

    def get_profile(self):
        return self.profile_data, self.profile_filename

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ProfileSelectionWindow()
    win.show()
    app.exec_()
    print(win.get_profile())

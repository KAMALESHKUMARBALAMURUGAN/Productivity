import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QComboBox, QTableWidget, QTableWidgetItem, QMessageBox, QInputDialog, QFileDialog
)
from PyQt5.QtGui import QFont, QPixmap, QPainter
from PyQt5.QtCore import QDateTime
from datetime import datetime
from PyQt5.QtCore import Qt  # Import Qt for colors
from PyQt5.QtGui import QColor  # Import QFont and QColor for styling the font and colors


class EisenhowerMatrixApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set up the window
        self.setWindowTitle('Eisenhower Matrix Manager')
        self.setGeometry(100, 100, 800, 600)

        # Create the layout
        main_layout = QVBoxLayout()

        # Display the current date at the top
        current_date = datetime.now().strftime("%A, %d %B %Y")  # Format: "Monday, 25 December 2024"
        self.date_label = QLabel(current_date)
        self.date_label.setFont(QFont("Arial", 14, QFont.Bold))  # Styling the font
        self.date_label.setAlignment(Qt.AlignCenter)  # Center align the date

        # Task input and category selection
        self.task_label = QLabel('Enter Task Description:')
        self.task_input = QLineEdit(self)

        self.category_label = QLabel('Select Category:')
        self.category_combobox = QComboBox(self)
        self.category_combobox.addItems([
            "Urgent & Important(DO FIRST)",
            "Not Urgent & Important(SCHEDULE)",
            "Urgent & Not Important(DELEGATE)",
            "Not Urgent & Not Important(DON'T DO)"
        ])

        # Buttons to add and remove tasks
        self.add_button = QPushButton('Add Task', self)
        self.add_button.clicked.connect(self.add_task)

        self.remove_button = QPushButton('Remove Task', self)
        self.remove_button.clicked.connect(self.remove_task)

        # Create a table widget to display tasks in a 2x2 table
        self.matrix_table = QTableWidget(self)
        self.matrix_table.setRowCount(2)
        self.matrix_table.setColumnCount(2)
        self.matrix_table.setHorizontalHeaderLabels(['Important', 'Not Important'])
        self.matrix_table.setVerticalHeaderLabels(['Urgent', 'Not Urgent'])

        # Increase table size
        self.matrix_table.setMinimumHeight(30)
        self.matrix_table.setMinimumWidth(60)

        # Set font for headers
        header_font = QFont()
        header_font.setBold(True)
        self.matrix_table.horizontalHeader().setFont(header_font)
        self.matrix_table.verticalHeader().setFont(header_font)

    
        # Add a save button
        self.save_button = QPushButton('Save', self)
        self.save_button.clicked.connect(self.save_screenshot)

        # Add widgets to the layout
        main_layout.addWidget(self.date_label)
        main_layout.addWidget(self.task_label)
        main_layout.addWidget(self.task_input)
        main_layout.addWidget(self.category_label)
        main_layout.addWidget(self.category_combobox)
        main_layout.addWidget(self.add_button)
        main_layout.addWidget(self.remove_button)
        main_layout.addWidget(self.matrix_table)

        # Save button layout
        save_layout = QHBoxLayout()
        save_layout.addStretch()
        save_layout.addWidget(self.save_button)
        save_layout.addStretch()

        main_layout.addLayout(save_layout)
        self.setLayout(main_layout)

        # Initialize task storage
        self.tasks = {
            "Urgent & Important(DO FIRST)": [],
            "Not Urgent & Important(SCHEDULE)": [],
            "Urgent & Not Important(DELEGATE)": [],
            "Not Urgent & Not Important(DON'T DO)": []
        }

    def add_task(self):
        task = self.task_input.text().strip()
        if not task:
            QMessageBox.warning(self, "Warning", "Task description cannot be empty!")
            return

        category = self.category_combobox.currentText()

        # Determine the row and column based on the category
        if category == "Urgent & Important(DO FIRST)":
            row, col = 0, 0
        elif category == "Not Urgent & Important(SCHEDULE)":
            row, col = 1, 0
        elif category == "Urgent & Not Important(DELEGATE)":
            row, col = 0, 1
        elif category == "Not Urgent & Not Important(DON'T DO)":
            row, col = 1, 1

        # Add the task to the storage
        self.tasks[category].append(task)

        
        # Update the corresponding cell in the table
        self.update_cell(row, col, category)

        # Clear the input field
        self.task_input.clear()

    def remove_task(self):
        category, ok = QInputDialog.getItem(
            self, "Remove Task", "Select a category:", list(self.tasks.keys()), 0, False
        )
        if not ok:
            return

        if not self.tasks[category]:
            QMessageBox.information(self, "Info", f"No tasks to remove in '{category}'.")
            return

        task, ok = QInputDialog.getItem(
            self, "Remove Task", "Select a task to remove:", self.tasks[category], 0, False
        )
        if not ok:
            return

        self.tasks[category].remove(task)
        self.update_table()

    def update_table(self):
        for category, tasks in self.tasks.items():
            if category == "Urgent & Important(DO FIRST)":
                row, col = 0, 0
            elif category == "Not Urgent & Important(SCHEDULE)":
                row, col = 1, 0
            elif category == "Urgent & Not Important(DELEGATE)":
                row, col = 0, 1
            elif category == "Not Urgent & Not Important(DON'T DO)":
                row, col = 1, 1

            self.update_cell(row, col, category)

    def update_cell(self, row, col, category):
        task_list = "\n".join([f"{i+1}. {t}" for i, t in enumerate(self.tasks[category])])
        cell_text = f"<---{category}--->\n{task_list}" if task_list else f"{category}:\n(No tasks)"
        cell_item = QTableWidgetItem(cell_text)
        cell_item.setFont(QFont("calibri", 12))
         # Set font color to black
        cell_item.setForeground(QColor(0, 0, 0))  # Black font color
        # Set background color based on the category
        if category == "Urgent & Important(DO FIRST)":
            cell_item.setBackground(Qt.red)  # Red for Urgent & Important
        elif category == "Not Urgent & Important(SCHEDULE)":
            cell_item.setBackground(Qt.green)  # Green for Not Urgent & Important
        elif category == "Urgent & Not Important(DELEGATE)":
            cell_item.setBackground(Qt.yellow)  # Yellow for Urgent & Not Important
        elif category == "Not Urgent & Not Important(DON'T DO)":
            cell_item.setBackground(Qt.darkGray)  # White for Not Urgent & Not Important

            
        # Increase the size of the cells in the table
        self.matrix_table.setRowHeight(0, 150)  # Set height for the first row
        self.matrix_table.setRowHeight(1, 150)  # Set height for the second row
        self.matrix_table.setColumnWidth(0, 300)  # Set width for the first column
        self.matrix_table.setColumnWidth(1, 300)  # Set width for the second column



        self.matrix_table.setItem(row, col, cell_item)
        # cell_item.setBackground(Qt.red)

        self.matrix_table.resizeColumnsToContents()
        self.matrix_table.resizeRowsToContents()

    def save_screenshot(self):
          # Get the current date

        # current_date = datetime.now().strftime("%Y-%m-%d")  # Format the date as "YYYY-MM-DD"
#format the current_date like monday - yyyy-mm-dd
        current_date = QDateTime.currentDateTime().toString("dddd - yyyy-MM-dd")

        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Screenshot", current_date , "PNG Files (*.png)", options=options)

        if file_path:
            pixmap = QPixmap(self.size())
            self.render(pixmap)
            pixmap.save(file_path)
            QMessageBox.information(self, "Saved", f"Screenshot saved to {file_path}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = EisenhowerMatrixApp()
    ex.show()
    sys.exit(app.exec_())

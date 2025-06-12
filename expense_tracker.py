import sys
import csv
import os
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QComboBox,
    QDateEdit,
    QGroupBox,
    QHeaderView,
    QMainWindow,
)
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QFont, QIcon

CSV_FILE = "expenses.csv"


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Daily Expense Tracker")
        self.setWindowIcon(QIcon("icon.jpg"))
        self.setGeometry(0, 0, 500, 500)
        self.initUI()
        self.setTheme()
        self.load_Expense()

    def initUI(self):

        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("Expense Tracker")
        title.setFont(QFont("Arial", 22, QFont.Bold))
        # title.setStyleSheet("margin:5px;")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size:30px;" "color:green;" "font-weight:500;")
        layout.addWidget(title)

        input_group = QGroupBox("Add new expense")
        input_layout = QHBoxLayout()
        input_layout.setSpacing(10)

        self.input_amount = QLineEdit()
        self.input_amount.setPlaceholderText("Amount")
        self.input_amount.setFixedWidth(100)

        self.category = QComboBox()
        self.category.setFixedWidth(100)
        # self.category.setPlaceholderText("Category")
        self.category.addItem("Food")
        self.category.addItems(
            ["Shopping", "Transport", "Bills", "Transfers", "Other"]
        )

        self.description = QLineEdit()
        self.description.setFixedWidth(150)
        self.description.setPlaceholderText("Description")

        self.dates = QDateEdit()
        self.dates.setDate(QDate.currentDate())
        self.dates.setCalendarPopup(True)
        self.dates.setFixedWidth(100)

        self.Add_button = QPushButton("Add Expense")
        self.Add_button.clicked.connect(self.add_Expense)

        input_layout.addWidget(self.input_amount)
        input_layout.addWidget(self.category)
        input_layout.addWidget(self.description)
        input_layout.addWidget(self.dates)
        input_layout.addWidget(self.Add_button)

        layout.addWidget(input_group)
        input_group.setLayout(input_layout)

        table_layout = QVBoxLayout()
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(
            ["Amount", "Category", "Description", "Date"]
        )
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        table_layout.addWidget(self.table)
        layout.addWidget(self.table)

        del_layout = QHBoxLayout()
        self.del_button = QPushButton("Delete")
        self.del_button.setFixedWidth(100)
        self.del_button.setToolTip("Delete selected expense")
        self.del_button.clicked.connect(self.delete_Expense)
        del_layout.addStretch()
        del_layout.addWidget(self.del_button)
        layout.addLayout(del_layout)

        summary_layout = QHBoxLayout()
        self.label_total = QLabel("Total Spent: ₹0")
        summary_layout.addWidget(self.label_total)
        summary_layout.addStretch()
        layout.addLayout(summary_layout)

        self.setLayout(layout)

    def setTheme(self):
        self.label_total.setObjectName("totaltext")
        self.setStyleSheet(
            """
        #totaltext{
                font-size:25px;
                font-family:arial;
                font-weight:500;
                color:#3f7373;
            }
        QWidget {
            
            background: qlineargradient(
                x1: 0, y1: 0, x2: 1, y2: 1,
                stop: 0 #f3f4f6,
                stop: 1 #e3e8ef
            );
            font-family: Segoe UI;
            padding: 3px;
        }
        QComboBox {
            background-color: #ffffff;
            border: 1px solid #ccc;
            padding: 6px;
            border-radius: 5px;
            font-size: 14px;
        }
        QComboBox:hover {
            background-color: #f0f0f0;
        }
        QLineEdit {
            background-color: #ffffff;
            border: 1px solid #ccc;
            padding: 6px;
            border-radius: 5px;
            font-size: 14px;
        }
        QLineEdit:focus {
            border: 1px solid #00b894;
        }
        QPushButton {
            background-color: #00b894;
            color: white;
            padding: 8px 12px;
            border: none;
            border-radius: 5px;
            font-size: 14px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #00a884;
        }
        #deleteButton {
            background-color: #ff7675;
            color: white;
            padding: 8px;
            border-radius: 5px;
            font-weight: bold;
            border: none;
        }
        #deleteButton:hover {
            background-color: #d63031;
        }
        QLabel {
            color: #2d3436;
            font-size: 16px;
            margin:5px;
        }
        #total_text {
            font-size: 25px;
            font-family: Arial;
            font-weight: 600;
            color: #0984e3;
        }
        QTableWidget {
            background-color: #ffffff;
            border: 1px solid #ccc;
            font-size: 14px;
            border-radius: 5px;
        }
        QHeaderView::section {
            background-color: #dfe6e9;
            padding: 6px;
            font-weight: bold;
            border: none;
        }
        """
        )

    def load_Expense(self):
        self.table.setRowCount(0)
        total = 0

        if os.path.exists(CSV_FILE):
            with open(CSV_FILE, newline="") as file:
                reader = csv.reader(file)
                for row_index, row in enumerate(reader):
                    self.table.insertRow(row_index)
                    for col_index, col in enumerate(row):
                        self.table.setItem(row_index, col_index, QTableWidgetItem(col))
                    try:
                        total += float(row[0])
                    except ValueError:
                        continue

        self.label_total.setText(f"Total Spent: ₹{total:.2f}")

    def add_Expense(self):
        amount = self.input_amount.text().strip()
        category = self.category.currentText()
        desc = self.description.text().strip()
        date = self.dates.date().toString("yyyy-MM-dd")

        if not amount:
            QMessageBox.warning(self, "Input Error", "Amount is required")
            return

        try:
            amount = float(amount)
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Amount must be a number")

        with open(CSV_FILE, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([amount, category, desc, date])

        self.input_amount.clear()
        self.description.clear()
        self.dates.setDate(QDate.currentDate())
        self.load_Expense()

    def delete_Expense(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Delete Error", "Please select a row to delete.")
            return
        reply = QMessageBox.question(
            self,
            "Delete Expense",
            "Are you sure you want to delete this expense?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            self.table.removeRow(selected)
            expenses = []
            if os.path.exists(CSV_FILE):
                with open(CSV_FILE, mode="r", newline="") as file:
                    reader = csv.reader(file)
                    expenses = list(reader)
            if 0 <= selected < len(expenses):
                expenses.pop(selected)
                with open(CSV_FILE, mode="w", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerows(expenses)
            self.load_Expense()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

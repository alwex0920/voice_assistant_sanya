import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit
import json

class commandManager(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Command Manager')
        self.setGeometry(100, 100, 400, 300)

        self.service_label = QLabel('Команда:')
        self.service_input = QLineEdit()
        self.command_label = QLabel('Действие:')
        self.command_input = QLineEdit()
        self.type_label = QLabel('Введите тип:')
        self.type_input = QLineEdit()
        self.add_button = QPushButton('Добавить')
        self.recent_commands_label = QLabel('Недавно добавленные команды:')
        self.recent_commands_textedit = QTextEdit()
        self.recent_commands_textedit.setReadOnly(True)

        layout = QVBoxLayout()
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.service_label)
        input_layout.addWidget(self.service_input)
        input_layout.addWidget(self.command_label)
        input_layout.addWidget(self.command_input)
        input_layout.addWidget(self.type_label)
        input_layout.addWidget(self.type_input)
        input_layout.addWidget(self.add_button)

        layout.addLayout(input_layout)
        layout.addWidget(self.recent_commands_label)
        layout.addWidget(self.recent_commands_textedit)
        self.setLayout(layout)
        self.add_button.clicked.connect(self.add_command)

    def add_command(self):
        service = self.service_input.text()
        command = self.command_input.text()
        type = self.type_input.text()
        if service and command and type:
            with open('command.json', 'a') as file:
                data = {
                    "keywords": [f"{service}"],
                    "action":{
                        "type": f"{type}",
                        "input": f"{command}"
                        }
                }
                json.dump(data, file)
            self.service_input.clear()
            self.command_input.clear()
            self.type_input.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = commandManager()
    window.show()
    sys.exit(app.exec_())

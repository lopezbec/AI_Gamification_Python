import sys
import os
import threading
import ast
import io
import subprocess
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLabel

"""
Users input code in the text box. 
A simple security check is run checking for no import statements (can be expanded).
Code is saved in a .py script and then the file is run in a subprocess to give it its own scope and prevent effects on the application
The output is saved to a text file, and then read and displaed to the output
A simple time limit on the code execution (3s) is enforced, as well as an limit on the size of the output (1KB)
These serve as basic sanity checks and in combination with the import statements should cover basic accidental misuse from non-malicious users
"""

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.result_display = None
        self.textbox = None
        self.run_button = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.instr_label: QLabel = QLabel(self)
        self.instr_label.setText('Escribe tu líneas de código aquí abajo, y luego has click en el botón de abajo')
        layout.addWidget(self.instr_label)
        
        self.textbox: QTextEdit = QTextEdit(self)
        layout.addWidget(self.textbox)

        self.run_button: QPushButton = QPushButton('Correr', self)
        self.run_button.clicked.connect(self.exec_text_input)
        layout.addWidget(self.run_button)

        self.result_display: QTextEdit = QTextEdit(self)
        self.result_display.setReadOnly(True)
        layout.addWidget(self.result_display)

        self.setLayout(layout)
        self.setWindowTitle('Correr código')
        self.show()


    def close_window(self):
        self.close()
        
    def exec_text_input(self):

        code_str: str = self.textbox.toPlainText()

        if contains_import(code_str): # Small security vulnerability check
            result_str = "Error: Import statements are not allowed"
        else:
            result_str = save_and_run_script(code_str)
        
        self.result_display.setText(result_str)

    
def save_and_run_script(code_str) -> str:
    script_filename = 'user_script.py'
    output_filename = 'script_output.txt'
    max_output_size = 1024 # In bytes (1 MB)
    # Save the script to a file
    with open(script_filename, 'w') as file:
        file.write(code_str)

    try:
        with open(output_filename, 'w') as output_file:
            subprocess.run([sys.executable, script_filename], stdout=output_file, stderr=subprocess.STDOUT, timeout=3)
    except subprocess.TimeoutExpired:
        with open(output_filename, 'a') as output_file:
            output_file.write("\nCode execution exceeded time limit")        

    if os.path.exists(output_filename) and os.path.getsize(output_filename) > max_output_size:
        return 'Output exceeded size limit'

    # Read the output file
    with open(output_filename, 'r') as output_file:
        result_str = output_file.read()

    if os.path.exists(output_filename): # Delete the output file
        os.remove(output_filename)

    return result_str

    # def terminate_with_log(message):
    #     with open(output_filename, 'a') as output_file:
    #         output_file.write(f'\n{message}')
    #     exec_process.terminate()

    # # Terminates the user input execution when the output file exceeds the limit
    # def monitor_output_size():
    #     while exec_process.poll() is None:
    #         if os.path.exists(output_filename) and os.path.getsize(output_filename) > max_output_size:
    #             terminate_with_log("Output size limit exceeded.")
    #             break

    # monitor_thread = threading.Thread(target=monitor_output_size)
    # monitor_thread.start()

    # try: # Terminates the user input execution after the time limit has passed
    #     exec_process.wait(timeout=3)
    # except subprocess.TimeoutExpired:
    #     terminate_with_log("Code execution time limit exceeded.")

    # Checks that the thread has stopped (should always immediately return)
    # monitor_thread.join()



def exec_str(code_str) -> str:
    result: str = ''

    try:
        old_stdout: io.TextIO = sys.stdout
        sys.stdout = io.StringIO()
        output: io.StringIO = sys.stdout

        exec(code_str)

        sys.stdout = old_stdout
        result = output.getvalue()

    except SyntaxError as e:
        result = f'Syntax Error: {e}'
    except Exception as e:
        result = f'Error: {e}'

    return result


    
def contains_import(code_str) -> bool:
    try:
        parsed = ast.parse(code_str)
        for node in ast.walk(parsed):
            if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                return True
            # if isinstance(node, ast.While):
            #     return False
            # if isinstance(node, ast.FunctionDef):
            #     return False
        return False
    
    except SyntaxError:
        return False
    
if __name__ == '__main__':

    app: QApplication = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec())

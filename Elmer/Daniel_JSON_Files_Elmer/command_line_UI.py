import ast
import io
import os
import subprocess
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit
from badge_system.badge_verification import display_badge, is_badge_earned, update_badge_progress

class App(QWidget):

    def __init__(self, current_user:str=''):
        super().__init__()
        self.current_user = current_user
        self.textbox = None
        self.run_button = None
        self.result_display = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.textbox: QTextEdit = QTextEdit(self)
        self.textbox.setPlaceholderText('Escribe tu código aquí...')
        layout.addWidget(self.textbox)

        self.run_button: QPushButton = QPushButton('Correr', self)
        self.run_button.clicked.connect(self.run_script)
        layout.addWidget(self.run_button)

        self.result_display: QTextEdit = QTextEdit(self)
        self.result_display.setReadOnly(True)
        layout.addWidget(self.result_display)

        self.setLayout(layout)
        self.setWindowTitle('Run Python Code')
        self.show()

    def run_script(self):
        full_text = self.textbox.toPlainText()
        code_str, input_str = self.split_code_and_input(full_text)
        result_str = save_and_run_script(code_str, input_str)
        self.result_display.setText(result_str)
        
        #Validation for hello world badge
        if not is_badge_earned(self.current_user, 'hello_world'):
                display_badge('hello_world')
                update_badge_progress(username=self.current_user, badge_name='hello_world')

    def split_code_and_input(self, full_text):
        parts = full_text.split('# input')
        code_str = parts[0].strip()
        input_str = '\n'.join(part.strip() for part in parts[1:])  # Handle multiple inputs
        return code_str, input_str

def save_and_run_script(code_str, input_data=""):
    script_filename = 'user_script.py'
    max_output_size = 1024  # 1KB limit

    with open(script_filename, 'w') as file:
        file.write(code_str)

    result_str = ""
    try:
        process = subprocess.Popen([sys.executable, '-u', script_filename],
                                   stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT,
                                   text=True)
        output, _ = process.communicate(input=input_data, timeout=3)

        if len(output) > max_output_size:
            result_str = 'Output exceeded size limit'
        else:
            result_str = output

    except subprocess.TimeoutExpired:
        process.kill()
        result_str = "\nCode execution exceeded time limit"
    except Exception as e:
        result_str = f"Error running script: {e}"

    if os.path.exists(script_filename):
        os.remove(script_filename)

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

    
def CMD_Practica():
    ex = App()
    return ex

# El siguiente bloque solo se ejecutará si este archivo se ejecuta como un script independiente,
# no cuando se importa como un módulo.
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = CMD_Practica()
    ventana.show()
    sys.exit(app.exec())

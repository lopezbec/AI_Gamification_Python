import sys
import os
import subprocess
import ast
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit
#from badge_system.badge_verification import display_badge, is_badge_earned, update_badge_progress

class App(QWidget):

    def __init__(self,current_user:str=''):
        super().__init__()
        self.current_user = current_user
        self.result_display = None
        self.textbox = None
        self.run_button = None
        self.input_box = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(1)

        self.textbox: QTextEdit = QTextEdit(self)
        self.textbox.setPlaceholderText('Escribe tu código aquí.')
        self.textbox.setMaximumHeight(70)  # Ajustar altura del área de código
        layout.addWidget(self.textbox)

        self.input_box: QTextEdit = QTextEdit(self)
        self.input_box.setPlaceholderText('Proporciona tu entrada aquí antes de presionar Correr.')
        self.input_box.setMaximumHeight(50)  # Ajustar altura del área de entrada

        layout.addWidget(self.input_box)
        self.run_button: QPushButton = QPushButton('Correr', self)
        self.run_button.clicked.connect(self.run_script)
        layout.addWidget(self.run_button)

        self.result_display: QTextEdit = QTextEdit(self)
        self.result_display.setReadOnly(True)
        self.result_display.setMaximumHeight(50)  # Ajustar altura del área de resultados
        layout.addWidget(self.result_display)

        self.setLayout(layout)
        self.setWindowTitle('Run Python Code')
        self.show()

    def run_script(self):
        code_str = self.textbox.toPlainText().strip()
        input_str = self.input_box.toPlainText().strip()

        if contains_import(code_str):  # Chequeo de seguridad
            result_str = "Error: No se permiten declaraciones de importación"
        else:
            result_str = save_and_run_script(code_str, input_str)

        self.result_display.setText(result_str)

        # Validation for hello world badge
        #if not is_badge_earned(self.current_user, 'hello_world'):
            #display_badge('hello_world')
            #update_badge_progress(username=self.current_user, badge_name='hello_world')

def save_and_run_script(code_str, input_str) -> str:
    script_filename = '../../user_script.py'
    output_filename = 'script_output.txt'
    max_output_size = 1024  # En bytes (1 KB)

    # Guardar el script en un archivo
    with open(script_filename, 'w') as file:
        file.write(code_str)

    try:
        with open(output_filename, 'w') as output_file:
            proc = subprocess.Popen(
                [sys.executable, script_filename],
                stdin=subprocess.PIPE,
                stdout=output_file,
                stderr=subprocess.STDOUT,
                text=True
            )
            try:
                proc.communicate(input=input_str, timeout=3)
            except subprocess.TimeoutExpired:
                proc.kill()
                result_str = "\nLa ejecución del código superó el límite de tiempo"
            except EOFError:
                result_str = "\nError: Ingrese las entradas requeridas en el cuadro de entrada."

        # Verificar el tamaño del archivo de salida
        if os.path.exists(output_filename) and os.path.getsize(output_filename) > max_output_size:
            result_str = 'La salida superó el límite de tamaño'
        else:
            # Leer el archivo de salida
            with open(output_filename, 'r') as output_file:
                result_str = output_file.read()

    except Exception as e:
        result_str = f"Ocurrió un error: {e}"

    finally:
        if os.path.exists(output_filename):  # Eliminar el archivo de salida
            os.remove(output_filename)

    return result_str

def contains_import(code_str) -> bool:
    try:
        parsed = ast.parse(code_str)
        for node in ast.walk(parsed):
            if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                return True
        return False
    except SyntaxError:
        return False

def CMD_Practica():
    ex = App()
    return ex

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = CMD_Practica()
    ventana.show()
    sys.exit(app.exec())
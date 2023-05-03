import datetime
import json
import sys
import csv

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QStackedWidget, QRadioButton, QButtonGroup


class JsonWindow(QWidget):
    """
    Clase para crear una ventana que muestra información almacenada en un archivo JSON.

    ...

    Atributos
    ----------
    filename : str
        Nombre del archivo JSON que contiene la información que se mostrará en la ventana.
    page_type : str
        Tipo de página que se está mostrando (Pedagógica o Pregunta).
    styles : dict
        Diccionario que contiene los estilos a aplicar en la ventana.
    json_number : int
        Número que indica a qué archivo JSON pertenece la página que se está mostrando.

    Métodos
    -------
    init_ui()
        Inicializa la interfaz de usuario de la ventana.
    """
    def __init__(self, filename, page_type, styles, json_number):
        """
        Constructor de la clase JsonWindow.

        Parámetros
        ----------
        filename : str
            Nombre del archivo JSON que contiene la información que se mostrará en la ventana.
        page_type : str
            Tipo de página que se está mostrando (Pedagógica o Pregunta).
        styles : dict
            Diccionario que contiene los estilos a aplicar en la ventana.
        json_number : int
            Número que indica a qué archivo JSON pertenece la página que se está mostrando.
        """
        super().__init__()
        self.filename = filename
        self.page_type = page_type
        self.styles = styles
        self.json_number = json_number

        self.init_ui()

    def init_ui(self):
        """
        Inicializa la interfaz de usuario de la ventana.
        """
        # Crear un layout vertical
        self.layout = QVBoxLayout()

        # Leer el archivo JSON y almacenar los datos
        with open(self.filename) as json_file:
            self.data = json.load(json_file)

        # Crear y personalizar el título de la ventana
        title = QLabel(self.data[self.page_type.lower()][0]["title"])
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(
            f"background-color: {self.styles['title_background_color']}; color: {self.styles['title_text_color']}; border: 2px solid {self.styles['title_border_color']}")
        title_font = QFont()
        title_font.setPointSize(self.styles['font_size'])
        title.setFont(title_font)
        # Añadir el título al layout
        self.layout.addWidget(title)

        # Si el tipo de página es "question", agregar bloques de preguntas y respuestas
        if self.page_type.lower() == "question":
            self.radio_buttons = []
            self.button_group = QButtonGroup()

            # Añadir bloques de preguntas al layout
            for idx, block in enumerate(self.data[self.page_type.lower()][0]["blocks"]):
                block_label = QLabel(block["text"])
                block_label.setStyleSheet(f"font-size: {self.styles['font_size']}px")
                self.layout.addWidget(block_label)

            # Añadir botones de radio (opciones de respuesta) al layout
            for idx, answer in enumerate(self.data[self.page_type.lower()][0]["answers"]):
                radio_button = QRadioButton(answer["text"])
                radio_button.setStyleSheet(f"font-size: {self.styles['font_size']}px")
                self.radio_buttons.append(radio_button)
                self.button_group.addButton(radio_button, idx)
                self.layout.addWidget(radio_button)

            # Añadir la etiqueta de retroalimentación al layout
            self.feedback_label = QLabel("")
            self.feedback_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.layout.addWidget(self.feedback_label)

        # Si el tipo de página es "pedagogical", agregar bloques de contenido
        else:
            for block in self.data[self.page_type.lower()][0]["blocks"]:
                block_label = QLabel(block["text"])
                if block["type"] == "Syntax":
                    block_label.setStyleSheet(
                        f"border: {self.styles['syntax_border_width']}px solid {self.styles['syntax_border_color']}; background-color: {self.styles['syntax_background_color']}; font-size: {self.styles['font_size']}px")
                else:
                    block_label.setStyleSheet(f"font-size: {self.styles['font_size']}px")
                # Añadir el bloque al layout
                self.layout.addWidget(block_label)

        # Establecer el layout en el QWidget
        self.setLayout(self.layout)


class MainWindow(QWidget):
    """
        Clase para crear la ventana principal de la aplicación, que contiene páginas cargadas desde archivos JSON.

        ...

        Atributos
        ----------
        styles : dict
            Diccionario que contiene los estilos a aplicar en la ventana.
        log_data : list
            Lista que almacena los eventos de apertura y cierre de las páginas para su posterior registro.
        current_page : int
            Número de página actual que se está mostrando en la ventana principal.

        Métodos
        -------
        init_ui()
            Inicializa la interfaz de usuario de la ventana principal.
        log_event(event)
            Registra un evento de apertura o cierre de página.
        save_log()
            Guarda el registro de eventos en un archivo CSV.
        load_page_order()
            Carga el orden de las páginas desde un archivo JSON.
    """

    def __init__(self):
        super().__init__()

        with open("styles.json") as styles_file:
            self.styles = json.load(styles_file)

        self.log_data = []
        self.init_ui()
        self.current_page = 0

    def init_ui(self):
        """
        Inicializa la interfaz de usuario de la ventana principal.
        """
        self.layout = QVBoxLayout()
        self.setStyleSheet(f"background-color: {self.styles['main_background_color']}")

        self.stacked_widget = QStackedWidget()

        for page in self.load_page_order():
            if page["type"] == "JsonWindow":
                json_window = JsonWindow(page["filename"], page["page_type"], self.styles, page["json_number"])
                self.stacked_widget.addWidget(json_window)

        self.continue_button = QPushButton("Continuar")
        self.continue_button.setStyleSheet(f"background-color: {self.styles['continue_button_color']}; color: white")
        continue_button_font = QFont()
        continue_button_font.setPointSize(self.styles['font_size'])
        self.continue_button.setFont(continue_button_font)
        self.continue_button.clicked.connect(self.switch_page)

        self.submit_button = QPushButton("Enviar")
        self.submit_button.setStyleSheet(f"background-color: {self.styles['continue_button_color']}; color: white")
        submit_button_font = QFont()
        submit_button_font.setPointSize(self.styles['font_size'])
        self.submit_button.setFont(submit_button_font)
        self.submit_button.clicked.connect(self.submit_answer)
        self.submit_button.hide()

        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.submit_button)
        self.button_layout.addWidget(self.continue_button)

        self.layout.addWidget(self.stacked_widget)
        self.layout.addLayout(self.button_layout)

        self.setLayout(self.layout)
        self.showFullScreen()

    def log_event(self, event):
        """
        Registra un evento con su hora en self.log_data.

        Parámetros
        ----------
        event : str
            Descripción del evento a registrar.
        """
        # Obtener la hora actual y almacenarla como una cadena de texto
        event_time = datetime.datetime.now().strftime("%H:%M:%S")
        # Obtener el número del archivo JSON correspondiente a la página actual
        json_number = self.stacked_widget.currentWidget().json_number
        # Añadir el evento y su hora al registro de datos (log_data)
        self.log_data.append({"event": f"Json {json_number} {event}", "time": event_time})

    def save_log(self):

        fieldnames = ['event', 'time']

        with open("Respuestas_Main_Part_1.csv", mode="a", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            # Si el archivo está vacío, escribir el encabezado
            if csv_file.tell() == 0:
                writer.writeheader()

            # Escribir cada registro en el archivo
            for log in self.log_data:
                writer.writerow(log)

            csv_file.write("\n")  # Agregar un salto de línea después de los registros

    def load_page_order(self):
        """
        Carga el orden de las páginas desde el archivo "page_order.json".

        Devoluciones
        -------
        list
            Lista de objetos que representan el orden de las páginas.
        """
        # Abrir el archivo "page_order.json" y cargar los datos en una variable
        with open("page_order.json") as order_file:
            data = json.load(order_file)
            # Devolver la lista que representa el orden de las páginas
            return data["page_order"]

    def submit_answer(self):
        """
        Valida la respuesta seleccionada y muestra retroalimentación al usuario.
        """
        # Obtener el índice de la respuesta seleccionada
        selected_answer_id = self.stacked_widget.currentWidget().button_group.checkedId()
        if selected_answer_id != -1:
            correct_answer_id = None
            # Buscar el índice de la respuesta correcta en la lista de respuestas
            for idx, answer in enumerate(
                    self.stacked_widget.currentWidget().data[self.stacked_widget.currentWidget().page_type.lower()][0][
                        "answers"]):
                if answer["correct"]:
                    correct_answer_id = idx
                    break

            # Si la respuesta seleccionada es correcta, mostrar un mensaje de éxito
            if selected_answer_id == correct_answer_id:
                self.stacked_widget.currentWidget().feedback_label.setText("Respuesta correcta")
                self.stacked_widget.currentWidget().feedback_label.setStyleSheet(
                    f"color: {self.styles['correct_color']}; font-size: {self.styles['font_size']}px")
                self.submit_button.hide()
                self.continue_button.show()
            # Si la respuesta seleccionada es incorrecta, mostrar un mensaje de error
            else:
                self.stacked_widget.currentWidget().feedback_label.setText(
                    "Respuesta incorrecta. Por favor, inténtalo de nuevo.")
                self.stacked_widget.currentWidget().feedback_label.setStyleSheet(
                    f"color: {self.styles['incorrect_color']}; font-size: {self.styles['font_size']}px")
        # Si no se ha seleccionado ninguna respuesta, mostrar un mensaje de advertencia
        else:
            self.stacked_widget.currentWidget().feedback_label.setText("No se ha seleccionado ninguna respuesta")
            self.stacked_widget.currentWidget().feedback_label.setStyleSheet(
                f"color: {self.styles['incorrect_color']}; font-size: {self.styles['font_size']}px")

    def switch_page(self):
        """
            Cambia la página actual por la siguiente en el orden establecido.
        """
        # Obtener el tipo de página actual
        current_page_type = self.stacked_widget.currentWidget().page_type.lower()

        # Si la página actual es la primera página del primer archivo JSON, registra el evento de apertura
        if current_page_type == "pedagogical" and self.stacked_widget.currentWidget().json_number == 1 and self.current_page == 0:
            self.log_event(f"{current_page_type.capitalize()} Page Open Time")

        # Registrar el evento de cierre de la página actual
        self.log_event(f"{current_page_type.capitalize()} Page Close Time")

        # Calcular el índice de la siguiente página
        next_index = self.stacked_widget.currentIndex() + 1

        # Si el siguiente índice es menor que el número total de páginas, continuar navegando
        if next_index < self.stacked_widget.count():
            # Cambiar a la siguiente página
            self.stacked_widget.setCurrentIndex(next_index)

            # Obtener el tipo de página actualizado
            current_page_type = self.stacked_widget.currentWidget().page_type.lower()

            # Registrar el evento de apertura de la nueva página
            self.log_event(f"{current_page_type.capitalize()} Page Open Time")

            # Si la nueva página es una pregunta, mostrar el botón de envío y ocultar el botón de continuar
            if current_page_type == "question":
                self.submit_button.show()
                self.continue_button.hide()
            # Si la nueva página no es una pregunta, ocultar el botón de envío y mostrar el botón de continuar
            else:
                self.submit_button.hide()
                self.continue_button.show()
        # Si se alcanza el final del recorrido de páginas, guardar el registro y cerrar la aplicación
        else:
            self.save_log()
            self.close()

        # Incrementar el número de la página actual
        self.current_page += 1


def main():
    """
        Función principal que crea la ventana de la aplicación y ejecuta el bucle de eventos.
    """
    # Crear una instancia de QApplication
    app = QApplication(sys.argv)
    # Crear e inicializar una instancia de MainWindow
    main_window = MainWindow()
    # Ejecutar el bucle de eventos de la aplicación
    sys.exit(app.exec())


if __name__ == '__main__':
    # Llamar a la función principal si el script se ejecuta como el programa principal
    main()

#TODO ARREGLAR LO DEL TIEMPO QUE SE ABRE Y SE CIERRA EL PEDAGOGICAL DEL PRIMER JSON.

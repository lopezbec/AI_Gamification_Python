try:
    import json
    import os
    import sys
    from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QVBoxLayout, QScrollArea, QFrame
    from PyQt6.QtGui import QPixmap, QFont
    from PyQt6.QtCore import Qt
    from badge_system.badge_verification import load_badges


    insignias_app = load_badges()
except Exception as e:
    print(f"Error in display cabinet class - linea {sys.exc_info()[2].tb_lineno} \n Detalle: {e}")

class BadgeWidget(QFrame):
    def __init__(self, badge, obtained=True):
        super().__init__()
        border_color = '#3498db'
        outer_border_color = '#f39c12' if obtained else '#7f8c8d'  # Dorado si ha sido obtenida
        icon_border_color = '#f39c12' if obtained else '#7f8c8d'  # Dorado para el icono si ha sido obtenida

        self.setStyleSheet(f"""
            QFrame {{
                border: 2px solid {outer_border_color};
                border-radius: 10px;
                padding: 10px;
                background-color: #ecf0f1;
            }}
            QLabel {{
                font-family: 'Lato';
            }}
            QLabel#icon {{
                border: 2px solid {icon_border_color};
                border-radius: 10px;
            }}
            QLabel#description {{
                border: 2px solid {border_color};
                border-radius: 10px;
            }}
        """)
        badge_icon = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img" , badge['badge_icon'])
        question_mark = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img" , "question_mark_icon.png")
        image_file = badge_icon if obtained else question_mark
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Añadir la imagen de la insignia
        image_label = QLabel(self)
        image_label.setObjectName("icon")
        pixmap = QPixmap(os.path.join(os.path.dirname(os.path.abspath(__file__)), image_file))
        image_label.setPixmap(pixmap)
        image_label.setScaledContents(True)
        image_label.setFixedSize(100, 100)
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Añadir el título y la descripción en un solo QLabel
        title_desc_label = QLabel(f"<b>{badge['badge_title']}</b><br>{badge['badge_description']}", self)
        title_desc_label.setObjectName("description")
        title_desc_label.setFont(QFont('Lato', 14))
        title_desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_desc_label.setWordWrap(True)

        # Añadir los elementos al layout
        layout.addWidget(image_label)
        layout.addWidget(title_desc_label)

class BadgeDisplayCabinet(QWidget):
    def __init__(self, nombre_usuario):      
        super().__init__()
        self.insignias = self.load_badges_per_user(nombre_usuario)
        self.initUI()

    def load_badges_per_user(self, nombre_usuario):
        # Cargar todas las insignias disponibles
        all_badges = insignias_app
        
        #insignias ganadas por el usuario
        user_badges_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "badge_progress", f"{nombre_usuario}_badge_progress.json") 
        with open(user_badges_file, "r", encoding='UTF-8') as file:
            user_badges = json.load(file)
        
         # Cargar todas las insignias disponibles
        all_badges = insignias_app
        
        # Insignias ganadas por el usuario
        user_badges_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "badge_progress", f"{nombre_usuario}_badge_progress.json") 
        with open(user_badges_file, "r", encoding='UTF-8') as file:
            user_badges = json.load(file)
        
        # Filtrar las insignias
        earned_badges = []
        for badge in all_badges:
            badge_id = badge['badge_id']
            if badge_id in user_badges and user_badges[badge_id]:
                badge['obtained'] = True
            else:
                badge['obtained'] = False
            earned_badges.append(badge)
        return earned_badges

    def initUI(self):
        # Configuración de la ventana principal
        self.setWindowTitle('Vitrina de Insignias')
        self.setGeometry(100, 100, 800, 600)

        # Crear el área de desplazamiento
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)

        # Crear un widget contenedor para el área de desplazamiento
        container_widget = QWidget()
        scroll_area.setWidget(container_widget)

        # Layout principal
        layout = QVBoxLayout(container_widget)
        container_widget.setLayout(layout)

        # Layout de la cuadrícula de insignias
        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)

         # Añadir insignias al layout
        row, col = 0, 0
        for i, insignia in enumerate(self.insignias):
            badge_widget = BadgeWidget(insignia, obtained=insignia['obtained'])
            grid_layout.addWidget(badge_widget, row, col)

            col += 1
            if col >= 3:  # Cambiar esta cifra para ajustar el número de columnas
                col = 0
                row += 1

        # Añadir el grid layout al layout principal
        layout.addLayout(grid_layout)

        # Layout principal del widget
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)
        self.showMaximized()
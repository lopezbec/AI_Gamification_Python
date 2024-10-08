import csv
import json


def contar_objetos_pages(nombre_archivo):
    punto_extension = "."
    punto_directorio_actual = nombre_archivo.index(punto_extension)  # Obtiene el índice del carácter especificado
    indice = nombre_archivo.find(punto_extension, punto_directorio_actual + 1)
    extension = nombre_archivo[indice+1:]

    if extension == 'json':
        print("ext json")
        with open(nombre_archivo) as archivo:
            data = json.load(archivo)
            # Specify the lesson_number for filtering

            # Find the lesson with the specified lesson_number
            lesson = next((l for l in data["lessons"] if l["lesson_number"] == 1), None)

            if lesson:
                # Get the number of objects in "pages" for the specified lesson_number
                return len(lesson["pages"])
            else:
                return
            
    elif extension == 'csv':
        with open(nombre_archivo) as archivo:
            lector = csv.reader(archivo)
            contador = sum(1 for _ in lector)
            return contador - 1 
    
    else:
        return "no encontrado"

# Ejemplo de uso
nombre_archivo = './assets/csv/Survey.csv'
nombre_objeto = 'lessons'
nombre_array = 'pages'
print(contar_objetos_pages(nombre_archivo))
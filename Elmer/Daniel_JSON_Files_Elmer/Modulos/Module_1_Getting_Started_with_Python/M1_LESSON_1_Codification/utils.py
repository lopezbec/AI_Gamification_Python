import json

class JsonLoader:
    @staticmethod
    def load_json_data(filename):
        with open(filename, encoding='UTF-8') as json_file:
            data = json.load(json_file)
            print(data)
        return data

def count_pages_for_lesson(json_file_path, target_lesson):
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)
        lessons = data.get('lessons', [])

        for lesson in lessons:
            lesson_number = lesson.get('lesson_number', None)
            if lesson_number == target_lesson:
                pages = lesson.get('pages', [])
                page_count = len(pages)
                return lesson_number, page_count

    return None  # Retorna None si no se encuentra la lección

if __name__ == "__main__":
    json_file_path = "C:\\Users\\Admin\\VSCode\\AI_Gamification_Python\\Elmer\\Daniel_JSON_Files_Elmer\\Module 1 - Getting Started with Python\\page_order.json"
    lesson_number, page_count = count_pages_for_lesson(json_file_path, 3)
    if lesson_number is not None:
        print(f'Lección {lesson_number} tiene {page_count} páginas.')
    else:
        print('La lección no fue encontrada.')







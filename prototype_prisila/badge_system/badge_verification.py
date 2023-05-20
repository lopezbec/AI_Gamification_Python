
import csv


class BadgeVerification:
    def __init__(self) -> None:
        super().__init__()

    # def check_badge(page_type):
    #     if page_type == 'multiplechoice' or page_type == 'draganddrop':
            
    #         csv_columns = ['correct_aswer']
    #         final_responses = responses
    #         try:
    #             with open('user_{}.csv'.format(self.username), 'w') as csv_file:
    #                 writer = csv.DictWriter(csv_file, fieldnames=csv_columns, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    #                 writer.writeheader()
    #                 for data in final_responses:
    #                     writer.writerow(data)
    #         except IOError:
    #             print("I/O error")
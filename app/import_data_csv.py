"""
    Script to import book data from .csv file to Model Database DJango
    To execute this script run: 
                                1) docker-compose exec web python manage.py shell
                                2) exec(open('import_data_csv.py').read())
"""

import csv
from physics.models import Zad

CSV_PATH = 'data2.csv'

contSuccess = 0
# Remove all data from Table
Zad.objects.all().delete()

with open(CSV_PATH, newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    print('Loading...')
    for row in spamreader:
        Zad.objects.create(sem=row[0], zad=row[1], page=row[2], identifier=row[3])
        contSuccess += 1
    print(f'{str(contSuccess)} inserted successfully! ')
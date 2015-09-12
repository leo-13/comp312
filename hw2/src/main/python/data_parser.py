__author__ = 'Leonid'
import csv

sweeping_schedule_file = 'sweeping_schedule.csv'
towed_vehicle_file = 'towed_vehicles.csv'

def read_csv(filename):
    csvfile = open('../resources/' + filename, newline='')
    filereader = csv.reader(csvfile)
    return filereader



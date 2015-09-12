__author__ = 'Leonid'
import csv
from datetime import date
from itertools import groupby

sweeping_schedule_file = 'sweeping_schedule.csv'
towed_vehicle_file = 'towed_vehicles.csv'
column1 = 'WARD'
column2 = 'DATES'


def read_csv(filename):
    csvfile = open('../resources/' + filename, newline='')
    filereader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
    return filereader


def get_sweeping_data():
    list = []
    dictreader = read_csv(sweeping_schedule_file)
    for row in dictreader:
        thedict = {}
        for key in row:
            if key == column1:
                thedict[key] = (int(row[key]))
            elif key == column2:
                dates = []
                monthnumber = row['MONTH NUMBER']
                days = row[key].split(',')
                for day in days:
                    dates.append(date(2015, int(monthnumber), int(day)))
                thedict[key] = dates
        list.append(thedict)
    return group_sweep_data_by_ward(list)


def group_sweep_data_by_ward(data):
    groupedlist = []
    for key, group in groupby(data, lambda item: item[column1]):
        thedict = {}
        thedict[column1] = key
        thedict[column2] = []
        for gr in list(group):
            thedict[column2] += gr[column2]
        groupedlist.append(thedict)
    return groupedlist


sweeplist = get_sweeping_data()

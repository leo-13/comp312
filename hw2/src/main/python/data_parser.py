__author__ = 'Leonid'
import csv
from datetime import date
from datetime import datetime
from itertools import groupby

sweeping_schedule_file = 'sweeping_schedule.csv'
towed_vehicle_file = 'towed_vehicles.csv'
ward_column_name = 'WARD'
sweep_dates_column_name = 'DATES'
tow_date_column_name = 'Date'
tow_address_column_name = 'Address'
towing_locations = {
    '10300 S. Doty': 'south',
    '400 E. Lower Wacker': 'downtown',
    '701 N. Sacramento': 'west',
    'Chicago O\'hare International Airport remote lot E.': 'northwest',
    'Police Pound': 'south'
}


def read_csv(filename):
    csvfile = open('../resources/' + filename, newline='')
    filereader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
    return filereader


def get_sweeping_data():
    data_list = []
    dictreader = read_csv(sweeping_schedule_file)
    for row in dictreader:
        rowdict = {}
        for key in row:
            if key == ward_column_name:
                rowdict[key] = int(row[key])
            elif key == sweep_dates_column_name:
                dates = []
                monthnumber = row['MONTH NUMBER']
                days = row[key].split(',')
                for day in days:
                    dates.append(date(2015, int(monthnumber), int(day)))
                rowdict[key] = dates
        data_list.append(rowdict)
    return group_data_by_column(data_list, ward_column_name, sweep_dates_column_name)


def get_towed_data():
    data_list = []
    dictreader = read_csv(towed_vehicle_file)
    for row in dictreader:
        rowdict = {}
        for key in row:
            if key == tow_address_column_name:
                rowdict[key] = towing_locations.get(row[key])
            elif key == tow_date_column_name:
                rowdict[key] = datetime.strptime(row[key], '%m/%d/%Y').date()
        data_list.append(rowdict)
    return group_data_by_column(data_list, tow_address_column_name, tow_date_column_name)


def group_data_by_column(data, groupbycolumnname, secondcolumnname):
    sorteddata = sorted(data, key=lambda item: item[groupbycolumnname])
    groupeddict = {}
    for key, group in groupby(sorteddata, lambda item: item[groupbycolumnname]):
        groupeddict[key] = []
        for gr in group:
            try:
                groupeddict[key] += (gr[secondcolumnname])
            except TypeError:
                groupeddict[key].append(gr[secondcolumnname])
    return groupeddict


list1 = get_towed_data()

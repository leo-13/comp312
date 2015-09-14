__author__ = 'Leonid'
import csv
from datetime import date
from datetime import datetime
from itertools import groupby

sweeping_schedule_file = 'sweeping_schedule.csv'
towed_vehicle_file = 'towed_vehicles.csv'
ward_neighborhood_file = 'ward_neighborhood_mapping.csv'
ward_column_name = 'WARD'
sweep_dates_column_name = 'DATES'
tow_date_column_name = 'Date'
tow_address_column_name = 'Address'
neighborhood_column_name = 'NEIGHBORHOOD'
towing_locations = {
    '10300 S. Doty': 'south',
    '400 E. Lower Wacker': 'downtown',
    '701 N. Sacramento': 'west',
    'Chicago O\'hare International Airport remote lot E.': 'northwest',
    'Police Pound': 'south'
}


def read_csv(filename):
    csv_file = open('../resources/' + filename, newline='')
    file_reader = csv.DictReader(csv_file, delimiter=',', quotechar='"')
    return file_reader


def get_sweeping_data():
    data_list = []
    dict_reader = read_csv(sweeping_schedule_file)
    ward_neighborhood_map = get_ward_neighborhood_map()
    for row in dict_reader:
        row_dict = {}
        for key in row:
            if key == ward_column_name:
                row_dict[neighborhood_column_name] = ward_neighborhood_map.get(int(row[key]))
            elif key == sweep_dates_column_name:
                dates = []
                month_number = row['MONTH NUMBER']
                days = row[key].split(',')
                for day in days:
                    dates.append(date(2015, int(month_number), int(day)))
                row_dict[key] = dates
        data_list.append(row_dict)
    return group_data_by_column(data_list, neighborhood_column_name, sweep_dates_column_name)


def get_towed_data():
    data_list = []
    dict_reader = read_csv(towed_vehicle_file)
    for row in dict_reader:
        row_dict = {}
        for key in row:
            if key == tow_address_column_name:
                row_dict[neighborhood_column_name] = towing_locations.get(row[key])
            elif key == tow_date_column_name:
                row_dict[key] = datetime.strptime(row[key], '%m/%d/%Y').date()
        data_list.append(row_dict)
    return group_data_by_column(data_list, neighborhood_column_name, tow_date_column_name)


def get_ward_neighborhood_map():
    data_dict = {}
    dict_reader = read_csv(ward_neighborhood_file)
    for row in dict_reader:
        data_dict[int(row[ward_column_name])] = row[neighborhood_column_name]
    return data_dict

def group_data_by_column(data, groupby_column_name, second_column_name):
    sorted_data = sorted(data, key=lambda item: item[groupby_column_name])
    grouped_dict = {}
    for key, group in groupby(sorted_data, lambda item: item[groupby_column_name]):
        grouped_dict[key] = []
        for gr in group:
            try:
                grouped_dict[key] += (gr[second_column_name])
            except TypeError:
                grouped_dict[key].append(gr[second_column_name])
    return grouped_dict


list1 = get_towed_data()

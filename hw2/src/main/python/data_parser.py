#!/usr/bin/env python

__author__ = 'Leonid'
import csv
from datetime import date
from datetime import datetime
from itertools import groupby
from collections import OrderedDict

sweeping_schedule_file = 'sweeping_schedule.csv'
towed_vehicle_file = 'towed_vehicles.csv'
ward_neighborhood_file = 'ward_neighborhood_mapping.csv'
ward_column_name = 'WARD'
sweep_dates_column_name = 'DATES'
tow_date_column_name = 'Date'
tow_address_column_name = 'Address'
neighborhood_column_name = 'NEIGHBORHOOD'

# manually divided 'towing to' locations into neighborhoods
towing_locations = {
    '10300 S. Doty': 'south',
    '400 E. Lower Wacker': 'downtown',
    '701 N. Sacramento': 'west',
    'Chicago O\'hare International Airport remote lot E.': 'northwest',
    'Police Pound': 'south'
}

# returns a DictReader for a given csv file
def read_csv(filename):
    csv_file = open('../resources/' + filename, newline='')
    file_reader = csv.DictReader(csv_file, delimiter=',', quotechar='"')
    return file_reader


# returns a list of dictionaries in format { 'neighborhood' : [street cleaning dates] }
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


# returns a list of towed vehicles in format { 'neighborhood' : [towed dates] }
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


# maps wards to neighborhoods
def get_ward_neighborhood_map():
    data_dict = {}
    dict_reader = read_csv(ward_neighborhood_file)
    for row in dict_reader:
        data_dict[int(row[ward_column_name])] = row[neighborhood_column_name]
    return data_dict


# groups data in list of dictionaries { 'key' : [data_list] } by given key. Returns a dictionary { 'key' : [grouped_data_list] }
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


# returns a dictionary of dates with numbers of towed vehicales
def get_number_of_towed_vehicles_by_neighborhood(neighborhood):
    data_dict = {}
    dates = towed_vehicles_dates_by_neighborhood[neighborhood]
    for d in dates:
        data_dict[d] = dates.count(d)
    return data_dict


# returns a dictionary of dates with street cleaning info for each date
def street_cleaning_by_neighborhood(neighborhood):
    data_dict = {}
    towed_dates = towed_vehicles_dates_by_neighborhood[neighborhood]
    cleaning_dates = street_sweeping_schedule_by_neighborhood[neighborhood]
    for d in towed_dates:
        data_dict[d] = d in cleaning_dates
    return data_dict


if __name__ == '__main__':
    towed_vehicles_dates_by_neighborhood = get_towed_data()
    street_sweeping_schedule_by_neighborhood = get_sweeping_data()

    # Get # number of towed vehicles for each neighborhood for last 90 days (west, south, northwest and downtown)
    # Check if there was street cleaning on this dates in this area
    for city_neighborhood in towing_locations.values():
        print('_' * 44 + '\n')
        print('Towed vehicles against street cleaning data for neighborhood ' + city_neighborhood)
        towed_number_by_date = get_number_of_towed_vehicles_by_neighborhood(city_neighborhood)
        towed_number_by_date_sorted = OrderedDict(
            sorted(towed_number_by_date.items(), key=lambda item: item[1], reverse=True))
        south_street_cleaning_by_date = street_cleaning_by_neighborhood(city_neighborhood)
        print('-' * 44)
        print('| {0:11} | {1:12} | {2:15} |'.format('Date', 'Towed Count', 'Street Cleaning'))
        print('-' * 44)
        # for d_date, number in towed_number_by_date.items():
        for d_date, number in towed_number_by_date_sorted.items():
            print(
                '| {0:11} | {1:12} | {2:15} |'.format(str(d_date), str(number),
                                                      str(south_street_cleaning_by_date[d_date]))
            )

    print(
        '\nMy initial goal was to find correlation between number of parking tickets and street cleaning in the ares.')
    print(
        'I wasn\'t able to find parking violations data on Chicago Data Portal, and I decided to go with towed vehicles.')
    print('Here my expectation was that the correlation didn\'t exist, since most of the vehicles just get parking \
    tickets during street cleaning.')
    print('The data supports my hypothesis. On days with large number of towed vehicles there may or may not be\
     street cleaning in the area.')
    print('\nTwo assumptions that I had to make:')
    print('     1. Towed vehicles data did not include \'towed from\' address. It only had \'towed to\' one.')
    print('        Since there were only 5 towing facilities, I split them into groups by neighborhood.')
    print('     2. I wasn\'t able to find data that maps an address with a particular Chicago Ward.')
    print('        So, I manually split the wards buy neighborhood, according to the map.)')

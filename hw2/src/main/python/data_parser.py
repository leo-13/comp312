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

# manually divided 'towing to' locations into neighborhoods
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


def get_number_of_towed_vehicles_by_neighborhood(neighborhood):
    data_dict = {}
    dates = towed_vehicles_dates_by_neighborhood[neighborhood]
    for d in dates:
        data_dict[d] = dates.count(d)
    return data_dict


def street_cleaning_by_neighborhood(neighborhood):
    data_dict = {}
    towed_dates = towed_vehicles_dates_by_neighborhood[neighborhood]
    cleaning_dates = street_sweeping_schedule_by_neighborhood[neighborhood]
    for d in towed_dates:
        data_dict[d] = d in cleaning_dates
    return data_dict


towed_vehicles_dates_by_neighborhood = get_towed_data()
street_sweeping_schedule_by_neighborhood = get_sweeping_data()

# a = street_cleaning_by_neighborhood('south')
# print(a)

# Get # number of towed vehicles for each neighborhood for last 90 days (west, south, northwest and downtown)
# Check if there was street cleaning on this dates in this area

for city_neighborhood in towing_locations.values():
    print('_______')
    print('Towed vehicles against street cleaning data for neighborhood ' + city_neighborhood)
    towed_number_by_date = get_number_of_towed_vehicles_by_neighborhood(city_neighborhood)
    south_street_cleaning_by_date = street_cleaning_by_neighborhood(city_neighborhood)
    print('Date      ', 'Towed #', 'Street Cleaning')
    for d_date, number in towed_number_by_date.items():
        print(str(d_date), repr(number), str(south_street_cleaning_by_date[d_date]))

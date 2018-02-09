import folium
from collections import defaultdict
from geopy.geocoders import ArcGIS


# Creates list of lines with films in file with directory 'file_name'

def file_read(file_name):
    """
    File -> lst
    :param file_name:
    :return:
    """
    with open(file_name, 'r', encoding='iso8859') as file:
        lst = []
        while not file.readline().startswith('"'):
            file.readline()
        for line in file:
            if '------' not in line:
                lst.append(line.strip())
    return lst


# creates dict based on list of film and year in which this films were filmed

def creat_dict(lst, year, amount):
    """
    (lst, year) -> defaultdict
    :param lst:
    :param year:
    :return:
    """
    dict_ret, n = defaultdict(list), 0
    for film in lst:
        splitted_line = film.split('\t')
        if '(' + str(year) in film and n <= amount:
            if splitted_line[-1].startswith('('):
                country = splitted_line[-2]
            else:
                country = splitted_line[-1]
            film = splitted_line[0]
            dict_ret[film].append(country)
            n += 1
    return dict_ret


# give coordinates of a place

def loc_return(place):
    geo_loc = ArcGIS(timeout=100)
    location = geo_loc.geocode(place)
    return location.latitude, location.longitude


def map_creator(dictionary):
    map = folium.Map(location=[40.71455000000003, -74.00713999999994],
                     zoom_start=10)
    dict_of_coordinates = defaultdict(list)
    fg_year = folium.FeatureGroup(name='Movies Dates')
    for k, v in dictionary.items():
        k = k.replace('<', '')
        k = k.replace('>', '')
        k = k.replace("'", '')
        for location in v:
            lt, ln = loc_return(location)
            dict_of_coordinates[location] = (lt, ln)
            fg_year.add_child(folium.Marker(location=[lt, ln],
                                            popup=str(k),
                                            icon=folium.Icon()))

    fg_population = folium.FeatureGroup(name='World Population')
    fg_population.add_child(folium.GeoJson(
        data=open('world.json', 'r', encoding='utf-8-sig').read(),
        style_function=lambda x: {'fillColor': 'green'
        if x['properties']['POP2005'] < 10000000
        else  'orange' if 10000000 <= x['properties'][
            'POP2005'] < 20000000  else  'red'}))
    map.add_child(fg_year)
    map.add_child(fg_population)
    map.add_child(folium.LayerControl())
    map.save("Locations_map.html")


    # this function contains 2 previous for further using of module


def file_to_dict(file_name, year, amount):
    film_list = file_read(file_name)
    film_dict = creat_dict(film_list, year, amount)
    map_creator(film_dict)
    return 1


print(file_to_dict('locations.list', 1895, 10))

import folium
import pandas
import re
import random
from geopy.geocoders import Nominatim


def input_data(data_type, raid="a", message=""):
    """
    (type, str) -> (object)
    Returns the valid for data_type input with message for user
    """
    while True:
        try:
            a = data_type(input(message))
            if not eval(raid):
                raise ValueError
            return a
        except ValueError:
            print("Invalid input. Try again.")


def read_file(path):
    """
    (str) -> (list)
    Returns list of film lines from file.
    """
    lst = []
    with open(path, 'r', encoding='utf-8', errors='ignore') as file:
        line = file.readline()
        while not line.startswith('"'):
            line = file.readline()
        for x in file:
            lst.append(x.strip())
    return lst


def country_dict(lines_list, year):
    """
    (list) -> (dict)
    Returns dict made of list of lines with country as key and name as value.
    """
    lst = []
    for line in lines_list:
        if ('(' + str(year)) in line:
            line = re.sub(r'\([^()]*\)', '', line)
            line = re.sub(r'{[^()]*}', '', line)
            lines = re.split(r'\s\t+', line.strip())
            lst.append((lines[0], lines[1]))
    return lst


def get_locations(lst, max_locat=20):
    locations = []
    geolocator = Nominatim()
    for element in lst:
        try:
            location = geolocator.geocode(element[1])
            locations.append((element[0], (location.latitude,
                                           location.longitude)))
            if len(locations) == max_locat:
                break
        except:
            continue
    return locations


def films_layer(locations):
    films = folium.FeatureGroup(name="films")
    for el in locations:
        popup = folium.Popup(el[0], parse_html=True)
        films.add_child(folium.Marker(location=[el[1][0], el[1][1]],
                                      popup=popup))
    return films


def pop_layer(filename="world.json", name="population", encoding="utf-8-sig"):
    layer = folium.FeatureGroup(name=name)
    layer.add_child(folium.GeoJson(data=open(filename, 'r',
                                             encoding=encoding).read(),
                                   style_function=lambda x: {'fillColor': 'red'
                                   if x['properties']['POP2005'] < 10000000
                                   else 'orange' if 10000000 <=
                                   x['properties']['POP2005'] < 20000000
                                   else 'green'}))
    return layer


def area_layer(filename="world.json", name="area", encoding="utf-8-sig"):
    def fill_color(number):
        if number < 20000:
            return '#FF0000'
        elif 20000 <= number < 60000:
            return '#FF8800'
        elif 60000 <= number < 100000:
            return '#F2FF00'
        elif 100000 <= number < 140000:
            return '#66FF00'
        elif 140000 <= number < 180000:
            return '#00FFFB'
        elif 180000 <= number < 220000:
            return '#CC00FF'
        elif 220000 <= number < 260000:
            return '#FF00C3'
        else:
            return '#007D45'
    layer = folium.FeatureGroup(name=name)
    layer.add_child(folium.GeoJson(data=open(filename, 'r',
                                             encoding=encoding).read(),
                                   style_function=lambda x:
                                       {'fillColor':
                                           fill_color(x['properties']['AREA'])
                                        }))
    return layer


def map_creator(*layers):
    map_f = folium.Map()
    for layer in layers:
        map_f.add_child(layer)
    folium.TileLayer('cartodbdark_matter').add_to(map_f)
    folium.TileLayer('stamentoner').add_to(map_f)
    folium.TileLayer('Mapbox Control Room').add_to(map_f)
    map_f.add_child(folium.LayerControl())
    map_f.save('Blabla.html')


def main():
    year = input_data(int, "1895 < a < 2027", "Input year: ")
    path = input_data(str, message="Input path: ")
    max_mark = input_data(int, "0 < a < 111", "Input max number of markers: ")
    countries = country_dict(read_file(path), year)
    random.shuffle(countries)
    locations = get_locations(countries, max_mark)
    map_creator(area_layer(), pop_layer(), films_layer(locations))


main()

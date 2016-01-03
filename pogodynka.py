# -*- coding: utf-8 -*-
__author__ = 'Andrzej'
import requests, json, sys, getopt

units = "" #default to Kelvin
language= "pl"

map_unit = {"metric":"Celcjusza", "":"Kelvin'a", "imperial":"Farenheit'a"}

def get_json_for_city(query, language, units):
    return json.loads(requests.get(
        'http://api.openweathermap.org/data/2.5/weather?q='+ query + '&units='+units+'&lang='+language+'&id=524901&APPID=104B03CD23633E7F7EB75C9443BA103D').text)

def temperature_units(units):
    return map_unit[units]

def print_json(api_output, exact_match):
    if exact_match:
        print 'Pogoda w ' + api_output['name']
        print str(api_output['main']['temp']) + ' stopni ' + temperature_units(units) + ' , ' +  api_output['weather'][0]['description']
    else:
        print 'Nie znalezlismy danych dla zapytania. Sprobuj ponownie.'

def return_parsed_json(api_output, exact_match):
    if exact_match:
        output = 'Pogoda w ' + api_output['name'] + ":\n"
        output = output + str(api_output['main']['temp']) + ' stopni ' + temperature_units(units) + ' , ' +  api_output['weather'][0]['description']
    else:
        output = 'Nie znalazlem danych dla zapytania. Sprobuj ponownie.'
    return output

def check_match(api_output, city):
    if "message" in api_output and "Error" in api_output["message"]:
        return False
    else:
        return api_output['name'].lower() == city.lower()

def menu():
    print "=====Pogodynka====="
    return raw_input("Prosze wpisac miast dla ktorego chcesz sprawdzic pogode: ")

def usage():
    print "pogodynka.py -u unit_code -l language_code"
    print "pogodynka.py --unit unit_code --lang language_code"
    print "unit_code: default Kelvin, metric for Celscius, imperial for Farenheit"
    print "language_code: default pl, ISO code "

def main(argv):
    try:
      opts, args = getopt.getopt(argv,"l:u:h:",["unit=","lang=","help"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h',"--help"):
            usage()
            sys.exit()
        elif opt in ("-l", "--lang"):
            global language
            language = arg
        elif opt in ("-u", "--unit"):
            global units
            units= arg

if __name__ == '__main__':
    main(sys.argv[1:])
    city = menu()
    json = get_json_for_city(city,language,units)
    print_json(json,check_match(json,city))



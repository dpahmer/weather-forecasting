'''
Weather Program
Takes a location or zip code and returns basic weather data
'''

import requests, json, datetime
f=open('apikey', 'r')
mykey=f.read().strip()
f.close()


def location_getter():
    location = input("Please enter the city for your inquiry. Or city, country.")
    locurl = "https://api.openweathermap.org/geo/1.0/direct?q=" + location + "&limit=1" + mykey
    try:
        response = requests.get(locurl)
        response.raise_for_status()
    except:
        print("That location isn't valid. Please try again next time.")
        return ""

    if len(response.text) < 10:  # Sometimes it comes back blank.
        print("The system doesn't recognize that location. PLease try a different name.")
        return ""
    else:
        loc = json.loads(response.text)
        latlon = "&lat=" + str(loc[0]["lat"]) + "&lon=" + str(loc[0]["lon"])
        try:
            statecode = loc[0]["state"]  # because the state value isn't always present, like for some international cities
        except:
            statecode = ""

        print("You requested weather information for", loc[0]["name"], "located in", statecode, loc[0]["country"])
        return latlon


def ziptocoord():
    zip = input("Please enter the zipcode for your inquiry.")
    locurl = "https://api.openweathermap.org/geo/1.0/zip?zip=" + zip + mykey

    try:
        response = requests.get(locurl)
        response.raise_for_status()
    except:
        print("That location isn't valid. Please try again next time.")
        return ""

    if len(response.text) < 10:
        print("The system doesn't recognize that location. PLease try a different name.")
        return ""

    loc = json.loads(response.text)
    latlon = "&lat=" + str(loc["lat"]) + "&lon=" + str(loc["lon"])
    print("You requested weather information for zipcode", loc["zip"], "located in", loc["name"])
    return latlon


def connect_to_forecast(location, unit):
    website_forecast = "https://api.openweathermap.org/data/3.0/onecall?"
    unitcall = "&units=" + unit
    urlpage_forecast = website_forecast + location + unitcall + mykey
    try:
        response = requests.get(urlpage_forecast)
        response.raise_for_status()
    except:
        return ""

    return response.text


def cleanup(report):
    week = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")

    print("\n Current temperature:", int(report['current']['temp']), "    Current conditions:", report['current']['weather'][0]['description'], "\n")

    print("****   Forecast for the next few days:   ****\n")
    print("Day #   (Day)             (Date)         Low Temp:   High Temp:     Condition:     Chance of rain / snow:")
    for daynum in range(7):
        print(daynum + 1, "   ",
              f"{week[datetime.datetime.utcfromtimestamp(report['daily'][daynum]['dt']).weekday()]:<15}",
              f"{datetime.datetime.utcfromtimestamp(report['daily'][daynum]['dt']).strftime('%m/%d/%Y'):<20}",
              f"{int(report['daily'][daynum]['temp']['min']):>5}", "     ",
              f"{int(report['daily'][daynum]['temp']['max']):>5}", "         ",
              f"{report['daily'][daynum]['weather'][0]['main']:<10}", "           ",
              int(100*(report["daily"][daynum]['pop'])), "%")

    try:
        alerts = report["alerts"][0]["description"]
    except:
        print("No weather alerts in effect")
    else:
        print(alerts)
    print()


def main():

    print("Welcome to the Weather application\n")
    while True:
        selector = input("Enter location for forecast: type 1 for zipcode; type 2 for city name; type Q to quit ")
        if selector.upper() == "Q":
            exit()
        elif selector == "1":
            coordinates = ziptocoord()
        elif selector == "2":
            coordinates = location_getter()
        else:
            continue
        if coordinates != "":
            units = "imperial"
            changeunit = input("Type C for Celsius; if you want Fahrenheit just hit enter ")
            if changeunit.upper() == "C":
                units = "metric"
            try:
                report = json.loads(connect_to_forecast(coordinates, units))
            except:
                print("Something went wrong. Try again. ")
            else:
                cleanup(report)


if __name__ == '__main__':
    main()

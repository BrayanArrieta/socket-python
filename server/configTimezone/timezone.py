import datetime

import pytz

from server.configTimezone.countries import countries


def findCountry(name):
    for country in countries:
        if name == country["name"]:
            return country["timezones"]
    return None


def getCountryTime(name):
    country=findCountry(name)
    if country:
        tz = pytz.timezone(country[0])
        ct = datetime.datetime.now(tz)
        return ct.isoformat()
    return None
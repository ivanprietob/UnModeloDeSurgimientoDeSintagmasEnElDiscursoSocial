import requests
import json
import time
import os

# NYT API KEY
KEY = "NYT_KEY"

# directories to data
URL_DATA = "data/"
URL_ALL_DATA = "allData/"

# index of json data
DATA = "data"

MONTHS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
YEARS = [1930, 1931, 1932, 1933, 1934, 1935, 1936, 1937, 1938, 1939,
         1940, 1941, 1942, 1943, 1944, 1945, 1946, 1947, 1948, 1949,
         1950, 1951, 1952, 1953, 1954, 1955, 1956, 1957, 1958, 1959,
         1960, 1961, 1962, 1963, 1964, 1965, 1966, 1967, 1968, 1969,
         1970, 1971, 1972, 1973, 1974, 1975, 1976, 1977, 1978, 1979,
         1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989,
         1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999,
         2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009,
         2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019,
         2020, 2021, 2022, 2023]


def downloadData():

    for year in YEARS:
        for month in MONTHS:

            url = f"https://api.nytimes.com/svc/archive/v1/{year}/{month}.json?api-key={KEY}"
            resp = requests.get(url)

            if resp.status_code != 200:
                print("[ERROR] Codigo de respuesta:", resp.status_code)
                return

            json_dict = resp.json()

            path = URL_ALL_DATA + str(year) + "/" + str(month) + ".json"

            if os.path.isdir(URL_ALL_DATA + str(year)) is False:
                os.mkdir(URL_ALL_DATA + str(year))

            with open(path, "w") as f:
                json.dump(json_dict, f, indent=2)

            time.sleep(10)

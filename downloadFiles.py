import requests
import json
import time
import os

KEY = "NDYRJAPDZMeZY440WSa4tJSr7ASG33Qh"
URL_DATA = "data/"


def main():
    # months = ["January", "February", "March", "April", "May", "June", "July",
    #           "August", "September", "October", "November", "Dicember"]
    months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    years = [2000, 2001, 2002, 2003, 2004,
             2005, 2006, 2007, 2008, 2009,
             2010, 2011, 2012, 2013, 2014,
             2015, 2016, 2017, 2018, 2019,
             2020, 2021, 2022, 2023]

    for year in years:
        for month in months:

            url = f"https://api.nytimes.com/svc/archive/v1/{year}/{month}.json?api-key={KEY}"
            resp = requests.get(url)

            if resp.status_code != 200:
                print("[ERROR] Codigo de respuesta: ", resp.status_code)
                return

            json_dict = resp.json()

            path = URL_DATA + str(year) + "/" + str(month) + ".json"

            if os.path.isdir(URL_DATA + str(year)) is False:
                os.mkdir(URL_DATA + str(year))

            with open(path, "w") as f:
                json.dump(json_dict, f, indent=2)

            size = len(json_dict["response"]["docs"])
            print(
                f"[INFO] Se han encontrado {size} archivos el {year}/{month}")

            time.sleep(12)


if __name__ == "__main__":
    main()

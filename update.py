import pandas as pd
import os
from datetime import date, timedelta, datetime, time
from dateutil.relativedelta import relativedelta
from dateutil.rrule import rrule, DAILY, MONTHLY
from pandas.tseries.offsets import BDay

from api import last_day_of_month, download_forward_nacional, download_inversiones, download_activos, download_extranjeros, mult_dl, upload_to_sql
from api import download_vf
from api import delete_by_date
today = date.today()

def auto_update():
    start_date = today-timedelta(weeks=8)
    end_date = today
    #descargar mensuales

    dls = [download_forward_nacional, download_inversiones, download_activos, download_extranjeros]    
    for dl in dls:
        mult_dl(dl, start_date, end_date)

    #descargar diarios
    day_count = (end_date - start_date).days + 1
    for single_date in (start_date + timedelta(n) for n in range(day_count)):
        download_vf(single_date)

    upload_to_sql(today-timedelta(weeks=8),today)

    for filename in os.listdir():
        if filename.endswith(".aspx"): 
            os.remove(filename)


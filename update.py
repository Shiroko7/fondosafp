import pandas as pd
import os
from datetime import date, timedelta, datetime, time
from dateutil.relativedelta import relativedelta
from dateutil.rrule import rrule, DAILY, MONTHLY
from pandas.tseries.offsets import BDay

from api import last_day_of_month, download_forward_nacional, download_inversiones, download_activos, download_extranjeros, mult_dl, upload_to_sql_monthly, upload_to_sql_daily
from api import download_vf
from api import daily_delete_by_date, delete_usdclp_dates, monthly_delete_by_date, upload_historic_usd


def auto_update(tipo):
    today = date.today()
    start_date = date(2016, 1, 1)  # today-timedelta(weeks=8)
    end_date = today

    if tipo == 'monthly':
        # descargar mensuales
        dls = [download_forward_nacional, download_inversiones,
               download_activos, download_extranjeros]
        for dl in dls:
            mult_dl(dl, start_date, end_date)
        upload_to_sql_monthly(start_date, today)

    elif tipo == 'daily':
        # descargar diarios
        #day_count = (end_date - start_date).days + 1
        # for single_date in (start_date + timedelta(n) for n in range(day_count)):
        #    download_vf(single_date)

        upload_to_sql_daily(start_date, today)
#
    # for filename in os.listdir():
    #    if filename.endswith(".aspx"):
    #        os.remove(filename)

#from update import auto_update
#


def kill():
    today = date.today()
    start_date = today-timedelta(weeks=8)
    end_date = today
    for fecha in rrule(DAILY, dtstart=start_date, until=end_date):
        daily_delete_by_date(fecha)
    for fecha in rrule(MONTHLY, dtstart=start_date, until=end_date):
        monthly_delete_by_date(last_day_of_month(fecha))
    delete_usdclp_dates(end_date, start_date)


# auto_update("monthly")
auto_update("daily")

# upload_historic_usd()

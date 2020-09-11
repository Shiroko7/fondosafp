import pandas as pd
import os
from datetime import date, timedelta, datetime, time
from dateutil.relativedelta import relativedelta
from dateutil.rrule import rrule, DAILY, MONTHLY
from pandas.tseries.offsets import BDay

from api import last_day_of_month, download_forward_nacional, download_inversiones, download_activos, download_extranjeros, mult_dl, upload_to_sql_monthly, upload_to_sql_daily
from api import download_vf
from api import daily_delete_by_date, delete_usdclp_dates, monthly_delete_by_date, upload_historic_usd


def update_carteras(tipo, start_date, end_date=None, confirmar=False, clear=False):
    if not confirmar or start_date == None:
        return

    if tipo == 'monthly':
        # descargar mensuales
        dls = [download_forward_nacional, download_inversiones,
               download_activos, download_extranjeros]
        for dl in dls:
            mult_dl(dl, start_date, end_date)
        upload_to_sql_monthly(start_date, end_date)

    elif tipo == 'daily':
        # descargar diarios
        day_count = (end_date - start_date).days + 1
        for single_date in (start_date + timedelta(n) for n in range(day_count)):
            download_vf(single_date)

        upload_to_sql_daily(start_date, end_date)
    if clear:
        for filename in os.listdir():
            if filename.endswith(".aspx"):
                os.remove(filename)
    print("Update terminado.")


def update_monthly(month, year, confirmar=False, clear=False):
    if not confirmar or month == None or year == None:
        return
    if (date.today().month == month) and (date.today().year) == year and (date.today().day < 11):
        print("Cartera del mes no disponible aún.")
        return
    fecha = date(year, month, 1)
    # descargar mensuales
    dls = [download_forward_nacional, download_inversiones,
           download_activos, download_extranjeros]
    for dl in dls:
        mult_dl(dl, fecha)
    upload_to_sql_monthly(fecha)

    if clear:
        for filename in os.listdir():
            if filename.endswith(".aspx"):
                os.remove(filename)
    print("Update terminado.")

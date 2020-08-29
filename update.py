import pandas as pd
import os
from datetime import date, timedelta, datetime, time
from dateutil.relativedelta import relativedelta
from dateutil.rrule import rrule, DAILY, MONTHLY
from pandas.tseries.offsets import BDay

from api import last_day_of_month, download_forward_nacional, download_inversiones, download_activos, download_extranjeros, mult_dl, upload_to_sql_monthly, upload_to_sql_daily
from api import download_vf
from api import daily_delete_by_date, delete_usdclp_dates, monthly_delete_by_date, upload_historic_usd


def update_carteras(tipo, start_date, end_date, confirmar=False, clear=False):
    if not confirmar:
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


update_carteras("monthly", date(2016, 8, 1), date(
    2020, 8, 2), confirmar=True, clear=False)

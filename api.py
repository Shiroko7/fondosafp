
import pandas as pd
from datetime import date, timedelta, datetime, time
from dateutil.relativedelta import relativedelta
from dateutil.rrule import rrule, DAILY, MONTHLY
from pandas.tseries.offsets import BDay

#Para leer tablas: excel,csv,html
import numpy as np
import xlrd
import os
#Descargar de la web
import urllib.request
from urllib.request import urlopen
import urllib.parse

#Conexión base de datos
#<>dependencia con psycopg2
import sqlalchemy as db
from sqlalchemy import create_engine  
from sqlalchemy import Column, String,DateTime,Integer,Float,Text
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import sessionmaker

def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + timedelta(days=4)  # this will never fail
    return next_month - timedelta(days=next_month.day)


#descargas
def download_forward_nacional(fecha):
    if fecha == None:
        return
    fecha_x = "".join(str(fecha)[0:7].split("-"))
    url = "https://www.spensiones.cl/apps/carteras/genera_xsl.php?fecpro={0}&listado=27".format(fecha_x)
    #custom token añomesdia
    token = "afp_fw_nacional_{0}.aspx".format(fecha_x)
    
    #actual download 
    try:
        urllib.request.urlretrieve(url, token)
    
        out = "CARTERA DE LOS FONDOS DE PENSIONES EN INSTRUMENTOS FORWARD NACIONALES {0} descargada con éxito".format(str(fecha))
    except:
        out = "Warning: CARTERA DE LOS FONDOS DE PENSIONES EN INSTRUMENTOS FORWARD NACIONALES {0} no se pudo descargar".format(str(fecha))
    print(out)
    
def download_inversiones(fecha):
    if fecha == None:
        return
    fecha_x = "".join(str(fecha)[0:7].split("-"))
    url = "https://www.spensiones.cl/apps/carteras/genera_xsl.php?fecpro={0}&listado=1".format(fecha_x)
    #custom token añomesdia
    token = "afp_inversiones_{0}.aspx".format(fecha_x)
    
    #actual download 
    try:
        urllib.request.urlretrieve(url, token)
    
        out = "CARTERA AGREGADA DE LOS FONDOS DE PENSIONES POR TIPO DE FONDO {0} descargada con éxito".format(str(fecha))
    except:
        out = "Warning: CARTERA AGREGADA DE LOS FONDOS DE PENSIONES POR TIPO DE FONDO {0} no se pudo descargar".format(str(fecha))
    print(out)
    
def download_activos(fecha):
    if fecha == None:
        return
    fecha_x = "".join(str(fecha)[0:7].split("-"))
    url = "https://www.spensiones.cl/apps/carteras/genera_xsl.php?fecpro={0}&listado=3".format(fecha_x)
    #custom token añomesdia
    token = "afp_activos_{0}.aspx".format(fecha_x)
    
    #actual download 
    try:
        urllib.request.urlretrieve(url, token)
    
        out = "ACTIVOS DE LOS FONDOS DE PENSIONES POR TIPO DE FONDO, DIVERSIFICACIÓN POR INSTRUMENTOS FINANCIEROS {0} descargada con éxito".format(str(fecha))
    except:
        out = "Warning: ACTIVOS DE LOS FONDOS DE PENSIONES POR TIPO DE FONDO, DIVERSIFICACIÓN POR INSTRUMENTOS FINANCIEROS {0} no se pudo descargar".format(str(fecha))
    print(out)
    
def download_extranjeros(fecha):
    if fecha == None:
        return
    fecha_x = "".join(str(fecha)[0:7].split("-"))
    url = "https://www.spensiones.cl/apps/carteras/genera_xsl.php?fecpro={0}&listado=24".format(fecha_x)
    #custom token añomesdia
    token = "afp_extranjeros_{0}.aspx".format(fecha_x)
    
    #actual download 
    try:
        urllib.request.urlretrieve(url, token)
    
        out = "CARTERA DE LOS FONDOS DE PENSIONES: INVERSION EN EL EXTRANJERO POR INSTRUMENTO Y ZONA GEOGRAFICA {0} descargada con éxito".format(str(fecha))
    except:
        out = "Warning: CARTERA DE LOS FONDOS DE PENSIONES: INVERSION EN EL EXTRANJERO POR INSTRUMENTO Y ZONA GEOGRAFICA {0} no se pudo descargar".format(str(fecha))
    print(out)

#downloader MENSUAL
def mult_dl(downloader,start_date, end_date):
    if start_date == None or end_date == None:
        return
    for d in rrule(MONTHLY, dtstart=start_date, until=end_date):
        downloader(d) 


#download vf & q
def download_vf(fecha):
    #PARSE DATE
    fecha_x = "".join(str(fecha).split('-'))
    year,month,day = str(fecha).split('-')
    
    #MAKE POST REQUEST
    url = "https://www.spensiones.cl/apps/valoresCuotaFondo/vcfAFP.php?tf="
    fondos = ['A','B','C','D','E']
    req = {"aaaa":year, "mm":month, "dd":day, "btn":"Buscar"}
    req = urllib.parse.urlencode(req).encode('utf-8')
    
    token = "vcf{0}_{1}.aspx"
    for f in fondos:
        #actual download 
        try:
            urllib.request.urlretrieve(url+f, token.format(f,fecha_x),data=req)
            out = "Valores de cuota y patrimonio AFP FONDO: {0} {1} descargados correctamente".format(f,fecha_x)
        except:
            out = "Warning: Valores de cuota y patrimonio AFP FONDO: {0} {0} no se pudo descargar".format(f,fecha_x)
        print(out)
    
def fetch_last_update(fecha):
    #PARSE DATE
    fecha_x = "".join(str(fecha).split('-'))
    year,month,day = str(fecha).split('-')
    
    #MAKE POST REQUEST
    url = "https://www.spensiones.cl/apps/valoresCuotaFondo/vcfAFP.php?tf="
    fondos = ['A']#,'B','C','D','E']
    
    
    for f in fondos:
        #actual download 
        try:
            html = urllib.request.urlopen(url+f).read()
            dlistas = pd.read_html(html,thousands = '.',decimal =',')[1]
            dlistas = list(dlistas.columns)
            confirmado = dlistas[0][2]
            disponible = dlistas[1][2]
            return confirmado, disponible

            
        except Exception as e:
            out = "Warning: Valores de cuota y patrimonio AFP FONDO: {0} {0} no se pudo leer".format(f,fecha_x)
            return out, str(e)

#procesar data 
def forward_nacional(start_date,end_date):
    cols = ['Fecha','Nombre','Fondo_A','Fondo_B','Fondo_C','Fondo_D','Fondo_E','TOTAL']
    df = pd.DataFrame(columns=cols)
    for fecha in rrule(MONTHLY, dtstart=start_date, until=end_date):
        fecha_x = "".join(str(fecha)[0:7].split("-"))
        token = "afp_fw_nacional_{0}.aspx".format(fecha_x)
        #try:
        #leer archivo como string
        file = open(token, 'r',encoding='utf-8')
        data = file.read()
        #buscar tabla dólar
        try:
            df_i = pd.read_html(data, header=0,thousands = '.',decimal =',')[0]
        except:
            continue
        df_i.columns = cols[1:]
        index = df_i[df_i.Nombre == 'MONEDA OBJETO: Dólar estadounidense(US$)'].index[0]
        df_i = df_i.iloc[index:index+7]
        #productos
        wnmc = df_i[df_i['Nombre']=='WNMC'].copy()
        for col in cols[2:]:
            wnmc[col] = wnmc[col].astype(float)
        wnmc['Fecha'] = last_day_of_month(fecha)
        wnmc['Nombre'] = 'Compra'
        wnmc = wnmc[cols]
        
        wnmv = df_i[df_i['Nombre']=='WNMV'].copy()
        for col in cols[2:]:
            wnmv[col] = wnmv[col].astype(float)
        wnmv['Fecha'] = last_day_of_month(fecha)
        wnmv['Nombre'] = 'Venta'
        wnmv = wnmv[cols]
        
        df = df.append(wnmc,ignore_index=True,sort=False)
        df = df.append(wnmv,ignore_index=True,sort=False)
        file.close()
        
    return df

def dif_forward_nacional(df):
    dfc = df[df['Nombre'] == 'Compra']
    dfv = df[df['Nombre'] == 'Venta']
    
    dfc.loc[:,('Fondo_A')] = dfc.loc[:,('Fondo_A')].abs()*-1
    dfc.loc[:,('Fondo_B')] = dfc.loc[:,('Fondo_B')].abs()*-1
    dfc.loc[:,('Fondo_C')] = dfc.loc[:,('Fondo_C')].abs()*-1
    dfc.loc[:,('Fondo_D')] = dfc.loc[:,('Fondo_D')].abs()*-1
    dfc.loc[:,('Fondo_E')] = dfc.loc[:,('Fondo_E')].abs()*-1
    dfc.loc[:,('TOTAL')] = dfc.loc[:,('TOTAL')].astype('float64')*-1
    df = pd.concat([dfc, dfv]).groupby(['Fecha'], as_index=False).agg({'Fondo_A':'sum','Fondo_B':'sum','Fondo_C':'sum','Fondo_D':'sum','Fondo_E':'sum','TOTAL':'sum'})
    df.loc[:,('Dif')] = df.loc[:,('TOTAL')].diff()
    df.loc[:,('Giro')] = df['Dif'] > 0
    df.loc[:,('Giro')] = df['Giro'].apply(lambda x: 'V' if x > 0 else 'C')
    return df
        
        
def inversiones(start_date,end_date):
    cols = ['Nombre','MMUSD_A','Porcentaje_A','MMUSD_B','Porcentaje_B','MMUSD_C','Porcentaje_C','MMUSD_D','Porcentaje_D','MMUSD_E','Porcentaje_E','MMUSD_TOTAL','Porcentaje_TOTAL']
    cols_f = ['Fecha']+cols
    
    df_nac = pd.DataFrame(columns=cols)
    
    df_inter = pd.DataFrame(columns=cols)

    df_total_activos = pd.DataFrame(columns=cols)
    
    for fecha in rrule(MONTHLY, dtstart=start_date, until=end_date):
        fecha_x = "".join(str(fecha)[0:7].split("-"))
        token = "afp_inversiones_{0}.aspx".format(fecha_x)
        #leer archivo como string
        file = open(token, 'r',encoding='utf-8')
        data = file.read()
        #buscar tabla
        try:
            df = pd.read_html(data, header=1,thousands = '.',decimal =',')[0]
        except:
            continue
        df.columns = cols
        df['Fecha'] = last_day_of_month(fecha)

        total_activos = df[df['Nombre'].str.match('TOTAL ACTIVOS')]
        total_activos.loc[:,('Nombre')] = 'TOTAL ACTIVOS'

        index = df[df.Nombre == 'INVERSIÓN EXTRANJERA TOTAL'].index[0]
        df_nacional = df.iloc[:index]
        df_internacional = df.iloc[index:]
        
        nac = df_nacional[df_nacional['Nombre'].str.match('INVERSIÓN NACIONAL TOTAL')]
        nac.loc[:,('Nombre')] = 'INVERSIÓN NACIONAL TOTAL'
        nac_rv = df_nacional[df_nacional['Nombre'].str.match('RENTA VARIABLE')]
        nac_rv.loc[:,('Nombre')] = 'RENTA VARIABLE'
        nac_rf = df_nacional[df_nacional['Nombre'].str.match('RENTA FIJA')]
        nac_rf.loc[:,('Nombre')] = 'RENTA FIJA'
        
        intrumentos_bc = df_nacional[df_nacional['Nombre'].str.match('Instrumentos Banco Central')]
        instrumentos_t = df_nacional[df_nacional['Nombre'].str.match('Instrumentos Tesorería')]
       
        
        instrumentos = {'Fecha':last_day_of_month(fecha),
                        'Nombre':'Instrumentos',
                        'MMUSD_A':intrumentos_bc['MMUSD_A'].astype(float).squeeze()+instrumentos_t['MMUSD_A'].astype(float).squeeze(),
                        'Porcentaje_A':intrumentos_bc['Porcentaje_A'].astype(float).squeeze()+instrumentos_t['Porcentaje_A'].astype(float).squeeze(),
                        'MMUSD_B':intrumentos_bc['MMUSD_B'].astype(float).squeeze()+instrumentos_t['MMUSD_B'].astype(float).squeeze(),
                        'Porcentaje_B':intrumentos_bc['Porcentaje_B'].astype(float).squeeze()+instrumentos_t['Porcentaje_B'].astype(float).squeeze(),
                        'MMUSD_C':intrumentos_bc['MMUSD_C'].astype(float).squeeze()+instrumentos_t['MMUSD_C'].astype(float).squeeze(),
                        'Porcentaje_C':intrumentos_bc['Porcentaje_C'].astype(float).squeeze()+instrumentos_t['Porcentaje_C'].astype(float).squeeze(),
                        'MMUSD_D':intrumentos_bc['MMUSD_D'].astype(float).squeeze()+instrumentos_t['MMUSD_D'].astype(float).squeeze(),
                        'Porcentaje_D':intrumentos_bc['Porcentaje_D'].astype(float).squeeze()+instrumentos_t['Porcentaje_D'].astype(float).squeeze(),
                        'MMUSD_E':intrumentos_bc['MMUSD_E'].astype(float).squeeze()+instrumentos_t['MMUSD_E'].astype(float).squeeze(),
                        'Porcentaje_E':intrumentos_bc['Porcentaje_E'].astype(float).squeeze()+instrumentos_t['Porcentaje_E'].astype(float).squeeze(),
                        'MMUSD_TOTAL':intrumentos_bc['MMUSD_TOTAL'].astype(float).squeeze()+instrumentos_t['MMUSD_TOTAL'].astype(float).squeeze(),
                        'Porcentaje_TOTAL':intrumentos_bc['Porcentaje_TOTAL'].astype(float).squeeze()+instrumentos_t['Porcentaje_TOTAL'].astype(float).squeeze()
                       }
 

        instrumentos = pd.DataFrame(instrumentos,index=[0])

        bonos_bancarios= df_nacional[df_nacional['Nombre'].str.match('Bonos Bancarios')]
        bonos_bancarios.loc[:,('Nombre')] = 'Bonos Bancarios'
        deposito_plazo = df_nacional[df_nacional['Nombre'].str.match('Depósitos a Plazo')]
        deposito_plazo.loc[:,('Nombre')] = 'Depósitos a Plazo'

        inter = df_internacional[df_internacional['Nombre'].str.match('INVERSIÓN EXTRANJERA TOTAL')]
        inter.loc[:,('Nombre')] = 'INVERSIÓN EXTRANJERA'
        inter_rv = df_internacional[df_internacional['Nombre'].str.match('RENTA VARIABLE')]
        inter_rv.loc[:,('Nombre')] = 'RENTA VARIABLE'
        inter_rf = df_internacional[df_internacional['Nombre'].str.match('RENTA FIJA')]
        inter_rf.loc[:,('Nombre')] = 'RENTA FIJA'

        df_total_activos = df_total_activos.append(total_activos,ignore_index=True,sort=False)
        df_nac = df_nac.append(nac,ignore_index=True,sort=False)
        df_nac = df_nac.append(nac_rv,ignore_index=True,sort=False)
        df_nac = df_nac.append(nac_rf,ignore_index=True,sort=False)
        df_nac = df_nac.append(instrumentos,ignore_index=True,sort=False)
        df_nac = df_nac.append(bonos_bancarios,ignore_index=True,sort=False)
        df_nac = df_nac.append(deposito_plazo,ignore_index=True,sort=False)

        df_inter = df_inter.append(inter,ignore_index=True,sort=False)
        df_inter = df_inter.append(inter_rv,ignore_index=True,sort=False)
        df_inter = df_inter.append(inter_rf,ignore_index=True,sort=False)
        file.close()
    
    df_total_activos = df_total_activos[cols_f]
    df_nac = df_nac[cols_f]
    df_inter = df_inter[cols_f]
    
    return df_total_activos,df_nac,df_inter


def activos(start_date,end_date):
    cols = ['Nombre','Porcentaje_A','Porcentaje_B','Porcentaje_C','Porcentaje_D','Porcentaje_E','Porcentaje_TOTAL','MM_TOTAL','MMUSD_TOTAL']
    cols_f = ['Fecha']+cols
    
    df = pd.DataFrame(columns=cols)
    
    for fecha in rrule(MONTHLY, dtstart=start_date, until=end_date):
        fecha_x = "".join(str(fecha)[0:7].split("-"))
        token = "afp_activos_{0}.aspx".format(fecha_x)
        #leer archivo como string
        file = open(token, 'r',encoding='utf-8')
        data = file.read()
        #buscar tabla
        try:
            df_i = pd.read_html(data, header=1,thousands = '.',decimal =',')[0]
        except:
            continue
            
        df_i.columns = cols
        df_i['Fecha'] = last_day_of_month(fecha)
        
        bcp = df_i[df_i['Nombre'].str.match('BCP')]
        btp = df_i[df_i['Nombre'].str.match('BTP')]
        
        bcu = df_i[df_i['Nombre'].str.match('BCU')]
        btu = df_i[df_i['Nombre'].str.match('BTU')]
        
        total = df_i[df_i['Nombre'].str.match('TOTAL EXTRANJERO')]
    
        bp = {
            'Fecha':fecha,
            'Nombre':'Bonos CLP',
            'Porcentaje_A':bcp['Porcentaje_A'].astype(float).squeeze()+btp['Porcentaje_A'].astype(float).squeeze(),
            'Porcentaje_B':bcp['Porcentaje_B'].astype(float).squeeze()+btp['Porcentaje_B'].astype(float).squeeze(),
            'Porcentaje_C':bcp['Porcentaje_C'].astype(float).squeeze()+btp['Porcentaje_C'].astype(float).squeeze(),
            'Porcentaje_D':bcp['Porcentaje_D'].astype(float).squeeze()+btp['Porcentaje_D'].astype(float).squeeze(),
            'Porcentaje_E':bcp['Porcentaje_E'].astype(float).squeeze()+btp['Porcentaje_E'].astype(float).squeeze(),
            'Porcentaje_TOTAL':bcp['Porcentaje_TOTAL'].astype(float).squeeze()+btp['Porcentaje_TOTAL'].astype(float).squeeze(),
            'MM_TOTAL':bcp['MM_TOTAL'].astype(float).squeeze()+btp['MM_TOTAL'].astype(float).squeeze(),
            'MMUSD_TOTAL':bcp['MMUSD_TOTAL'].astype(float).squeeze()+btp['MMUSD_TOTAL'].astype(float).squeeze(),
           }
        
        bu = {
            'Fecha':fecha,
            'Nombre':'Bonos UF',
            'Porcentaje_A':bcu['Porcentaje_A'].astype(float).squeeze()+btu['Porcentaje_A'].astype(float).squeeze(),
            'Porcentaje_B':bcu['Porcentaje_B'].astype(float).squeeze()+btu['Porcentaje_B'].astype(float).squeeze(),
            'Porcentaje_C':bcu['Porcentaje_C'].astype(float).squeeze()+btu['Porcentaje_C'].astype(float).squeeze(),
            'Porcentaje_D':bcu['Porcentaje_D'].astype(float).squeeze()+btu['Porcentaje_D'].astype(float).squeeze(),
            'Porcentaje_E':bcu['Porcentaje_E'].astype(float).squeeze()+btu['Porcentaje_E'].astype(float).squeeze(),
            'Porcentaje_TOTAL':bcu['Porcentaje_TOTAL'].astype(float).squeeze()+btu['Porcentaje_TOTAL'].astype(float).squeeze(),
            'MM_TOTAL':bcu['MM_TOTAL'].astype(float).squeeze()+btu['MM_TOTAL'].astype(float).squeeze(),
            'MMUSD_TOTAL':bcu['MMUSD_TOTAL'].astype(float).squeeze()+btu['MMUSD_TOTAL'].astype(float).squeeze(),
           }
 

        bp = pd.DataFrame(bp,index=[0])
        bu = pd.DataFrame(bu,index=[0])
        
        df = df.append(bp,ignore_index=True,sort=False)
        df = df.append(bu,ignore_index=True,sort=False)
        df = df.append(total,ignore_index=True,sort=False)
        file.close()
        
    df = df[cols_f]
    
    return df

def extranjeros(start_date,end_date):
    cols = ['Nombre','ASIA_EMERGENTE','ASIA_PACIFICO_DESARROLLADA','EUROPA','EUROPA_EMERGENTE','LATINOAMERICA','MEDIO_ORIENTE_AFRICA','NORTEAMERICA','OTROS','MMUSD_TOTAL']
    cols_f = ['Fecha']+cols
    
    df_total_ext = pd.DataFrame(columns=cols)
    
    for fecha in rrule(MONTHLY, dtstart=start_date, until=end_date):
        fecha_x = "".join(str(fecha)[0:7].split("-"))
        token = "afp_extranjeros_{0}.aspx".format(fecha_x)
        #leer archivo como string
        file = open(token, 'r',encoding='utf-8')
        data = file.read()
        #buscar tabla
        try:
            df = pd.read_html(data, header=1,thousands = '.',decimal =',')[0]
        except:
            continue
        df.columns = cols
        df['Fecha'] = last_day_of_month(fecha)
    
        total = df[df['Nombre'].str.match('TOTAL')]
        
        df_total_ext = df_total_ext.append(total,ignore_index=True,sort=False)
        file.close()
        
    df_total_ext = df_total_ext[cols_f]
    
    return df_total_ext



# HISTORICO
def vcfondos_historic(start_date,end_date, fondo):
    start = "".join(str(start_date)[0:4].split("-"))
    end = "".join(str(end_date)[0:4].split("-"))
    token = "vcf"+fondo+start+"-"+end+".xlsx"
    df = pd.read_excel(token)#, index_col=0) 
    return df
    
def valor_fondos_historic(start_date,end_date):
    df_A = vcfondos_historic(start_date, end_date, 'A')
    df_B = vcfondos_historic(start_date, end_date, 'B')
    df_C = vcfondos_historic(start_date, end_date, 'C')
    df_D = vcfondos_historic(start_date, end_date, 'D')
    df_E = vcfondos_historic(start_date, end_date, 'E')
    
    patrimonios =[i for i in list(df_A.columns) if 'Valor Patrimonio' in i]
    
    VF = pd.DataFrame(columns=['Fecha','VF_A','VF_B','VF_C','VF_D','VF_E'])
    VF.loc[:,('Fecha')] = df_A['Fecha']
    VF.loc[:,('VF_A')] = df_A[patrimonios].sum(axis=1)
    VF.loc[:,('VF_B')] = df_B[patrimonios].sum(axis=1)
    VF.loc[:,('VF_C')] = df_C[patrimonios].sum(axis=1)
    VF.loc[:,('VF_D')] = df_D[patrimonios].sum(axis=1)
    VF.loc[:,('VF_E')] = df_E[patrimonios].sum(axis=1)
    return VF


def Q_index_historic(start_date,end_date):
    df_A = vcfondos_historic(start_date, end_date, 'A')
    df_B = vcfondos_historic(start_date, end_date, 'B')
    df_C = vcfondos_historic(start_date, end_date, 'C')
    df_D = vcfondos_historic(start_date, end_date, 'D')
    df_E = vcfondos_historic(start_date, end_date, 'E')
    
    cuotas = [i for i in list(df_A.columns) if 'Valor Cuota' in i]
    patrimonios =[i for i in list(df_A.columns) if 'Valor Patrimonio' in i]

    Q = pd.DataFrame(columns=['Fecha','Q_A','Q_B','Q_C','Q_D','Q_E'])
    Q.loc[:,('Fecha')] = df_A['Fecha']
    fondos = ['A','B','C','D','E']
    df_fondos = [df_A,df_B,df_C,df_D,df_E]
    for f in range(len(fondos)):
        qf = pd.Series(np.zeros(len(Q['Fecha'])),dtype='float64')
        for i in range(len(cuotas)):
            c = df_fondos[f][cuotas[i]]
            c = c.fillna(1)
            
            v = df_fondos[f][patrimonios[i]]
            v = v.fillna(0)
            qf = qf + v/c
            
        Q['Q_'+fondos[f]] = qf
    
    return Q


# DIA A DIA (CASI)
def vcfondos(start_date,end_date):
    cols = ['Fecha','VF_A','VF_B','VF_C','VF_D','VF_E']
    fondos = ['A','B','C','D','E']
    df = pd.DataFrame(columns=cols)
    for fecha in rrule(DAILY, dtstart=start_date, until=end_date):
        fecha_x = "".join(str(fecha.date()).split("-"))
        row = {
            'Fecha':fecha,
            'VF_A': 0.0,
            'VF_B': 0.0,
            'VF_C': 0.0,
            'VF_D': 0.0,
            'VF_E': 0.0,
        }
        for f in fondos:
            token = "vcf{fondo}_{date}.aspx".format(fondo=f,date=fecha_x)
            #try:
            #leer archivo como string
            file = open(token, 'r')
            data = file.read()
            try:
                vf = pd.read_html(data,thousands = '.',decimal =',')[3]
                vf.columns = vf.columns.droplevel()
            
                row['VF_'+f] = float(vf[vf['A.F.P.']=='TOTAL']['Valor del Patrimonio'].squeeze())
            except:
                pass

            file.close()

        
        df_i = pd.DataFrame(row,columns=cols,index=[0])
        df = df.append(df_i,ignore_index=True,sort=False)
       
        
    return df


def vqfondos(start_date,end_date):
    cols = ['Fecha','Q_A','Q_B','Q_C','Q_D','Q_E']
    fondos = ['A','B','C','D','E']
    df = pd.DataFrame(columns=cols)
    for fecha in rrule(DAILY, dtstart=start_date, until=end_date):
        fecha_x = "".join(str(fecha.date()).split("-"))
        row = {
            'Fecha':fecha,
            'Q_A': 0.0,
            'Q_B': 0.0,
            'Q_C': 0.0,
            'Q_D': 0.0,
            'Q_E': 0.0,
        }
        for f in fondos:
            token = "vcf{fondo}_{date}.aspx".format(fondo=f,date=fecha_x)
            #try:
            #leer archivo como string
            file = open(token, 'r')
            data = file.read()
            try:
                vf = pd.read_html(data,thousands = '.',decimal =',')[3]
                vf.columns = vf.columns.droplevel()
                for afp in vf['A.F.P.']:
                    if afp == 'TOTAL':
                        break
                    p = float(vf[vf['A.F.P.']==afp]['Valor del Patrimonio'].squeeze())
                    c = float(vf[vf['A.F.P.']==afp]['Valor Cuota'].squeeze())
                    row['Q_'+f] += p/c
            except:
                pass
            file.close()

        
        df_i = pd.DataFrame(row,columns=cols,index=[0])
        df = df.append(df_i,ignore_index=True,sort=False)
       
        
    return df

#conectarse a la base de datos
#cambiar esto por un log in con input de usuario
database = create_engine('postgres://pfjqxkqzdbefyh:9b90121091b9a7aaba720a1b848f7b707a82c8db9e374e1d7d3b16e96f6f6258@ec2-35-174-127-63.compute-1.amazonaws.com:5432/d3d9vrbrckuu50')  
base = declarative_base()

#ORM entidades de la bd
class FORWARDS_NACIONALES(base):
    __tablename__ = 'forwards_nacionales'
    index = Column(Integer, autoincrement=True, primary_key=True)
    Fecha = Column(DateTime)
    Nombre = Column(String)
    Fondo_A = Column(Float)
    Fondo_B = Column(Float)
    Fondo_C = Column(Float)
    Fondo_D = Column(Float)
    Fondo_E = Column(Float)
    TOTAL = Column(Float)
    
class INVERSION_TOTAL(base):
    __tablename__ = 'inversion_total'
    index = Column(Integer, autoincrement=True, primary_key=True)
    Fecha = Column(DateTime)
    Nombre = Column(String)
    MMUSD_A = Column(Float)
    Porcentaje_A = Column(Float)
    MMUSD_B = Column(Float)
    Porcentaje_B = Column(Float)
    MMUSD_C = Column(Float)
    Porcentaje_C = Column(Float)
    MMUSD_D = Column(Float)
    Porcentaje_D = Column(Float)
    MMUSD_E = Column(Float)
    Porcentaje_E = Column(Float)
    MMUSD_TOTAL = Column(Float)
    Porcentaje_TOTAL = Column(Float)
    
class INVERSION_NACIONAL(base):
    __tablename__ = 'inversion_nacional'
    index = Column(Integer, autoincrement=True, primary_key=True)
    Fecha = Column(DateTime)
    Nombre = Column(String)
    MMUSD_A = Column(Float)
    Porcentaje_A = Column(Float)
    MMUSD_B = Column(Float)
    Porcentaje_B = Column(Float)
    MMUSD_C = Column(Float)
    Porcentaje_C = Column(Float)
    MMUSD_D = Column(Float)
    Porcentaje_D = Column(Float)
    MMUSD_E = Column(Float)
    Porcentaje_E = Column(Float)
    MMUSD_TOTAL = Column(Float)
    Porcentaje_TOTAL = Column(Float)

class INVERSION_INTERNACIONAL(base):
    __tablename__ = 'inversion_internacional'
    index = Column(Integer, autoincrement=True, primary_key=True)
    Fecha = Column(DateTime)
    Nombre = Column(String)
    MMUSD_A = Column(Float)
    Porcentaje_A = Column(Float)
    MMUSD_B = Column(Float)
    Porcentaje_B = Column(Float)
    MMUSD_C = Column(Float)
    Porcentaje_C = Column(Float)
    MMUSD_D = Column(Float)
    Porcentaje_D = Column(Float)
    MMUSD_E = Column(Float)
    Porcentaje_E = Column(Float)
    MMUSD_TOTAL = Column(Float)
    Porcentaje_TOTAL = Column(Float)

class ACTIVOS(base):
    __tablename__ = 'activos'
    index = Column(Integer, autoincrement=True, primary_key=True)
    Fecha = Column(DateTime)
    Nombre = Column(String)
    Porcentaje_A = Column(Float)
    Porcentaje_B = Column(Float)
    Porcentaje_C = Column(Float)
    Porcentaje_D = Column(Float)
    Porcentaje_E = Column(Float)
    Porcentaje_TOTAL = Column(Float)
    MM_TOTAL = Column(Float)
    MMUSD_TOTAL = Column(Float)
    
    
    
class EXTRANJEROS(base):
    __tablename__ = 'extranjeros'
    index = Column(Integer, autoincrement=True, primary_key=True)
    Fecha = Column(DateTime)
    Nombre = Column(String)
    ASIA_EMERGENTE = Column(Float)
    ASIA_PACIFICO_DESARROLLADA = Column(Float)
    EUROPA = Column(Float)
    EUROPA_EMERGENTE = Column(Float)
    LATINOAMERICA = Column(Float)
    MEDIO_ORIENTE_AFRICA = Column(Float)
    NORTEAMERICA = Column(Float)
    OTROS = Column(Float)
    MMUSD_TOTAL = Column(Float)

class VALOR_FONDOS(base):
    __tablename__ = 'valor_fondos'
    index = Column(Integer, autoincrement=True, primary_key=True)
    Fecha = Column(DateTime)
    VF_A = Column(Float)
    VF_B = Column(Float)
    VF_C = Column(Float)
    VF_D = Column(Float)
    VF_E = Column(Float)
    
class Q_INDEX(base):
    __tablename__ = 'q_index'
    index = Column(Integer, autoincrement=True, primary_key=True)
    Fecha = Column(DateTime)
    Q_A = Column(Float)
    Q_B = Column(Float)
    Q_C = Column(Float)
    Q_D = Column(Float)
    Q_E = Column(Float)
    
#create session
Session = sessionmaker(database)  
session = Session()

base.metadata.create_all(database)
#se va a quejar si lo corres más de una vez^


#OPERCIONES QUE MODIFICAN LA BD

#delete rows by date 
def delete_by_date(fecha):
    #estos son mensuales
    input_rows = session.query(FORWARDS_NACIONALES).filter(FORWARDS_NACIONALES.Fecha == fecha).delete()

    input_rows = session.query(INVERSION_NACIONAL).filter(INVERSION_NACIONAL.Fecha == fecha).delete()

    input_rows = session.query(INVERSION_INTERNACIONAL).filter(INVERSION_INTERNACIONAL.Fecha == fecha).delete()

    input_rows = session.query(INVERSION_TOTAL).filter(INVERSION_TOTAL.Fecha == fecha).delete()
    
    input_rows = session.query(ACTIVOS).filter(ACTIVOS.Fecha == fecha).delete()
    
    input_rows = session.query(EXTRANJEROS).filter(EXTRANJEROS.Fecha == fecha).delete()
    
    #estos son diarios
    input_rows = session.query(VALOR_FONDOS).filter(VALOR_FONDOS.Fecha >= fecha, VALOR_FONDOS.Fecha <= fecha + timedelta(days = 30)).delete()
    
    input_rows = session.query(Q_INDEX).filter(Q_INDEX.Fecha >= fecha, Q_INDEX.Fecha <= fecha + timedelta(days = 30)).delete()
    
    session.commit()
            
#UPLOAD DATA
def upload_to_sql(start_date,end_date = None):
    if end_date == None:
        end_date = start_date
    #IMPORTANTE: CADA UPLOAD DE UN DÍA PRIMERO BOTA LO QUE YA ESTA, PARA NO DUPLICAR DATA ACCIDENTALMENTE
    for fecha in rrule(MONTHLY, dtstart=start_date, until=end_date):
        delete_by_date(fecha)
    for fecha in rrule(MONTHLY, dtstart=start_date, until=end_date):
        delete_by_date(last_day_of_month(fecha))

    df_fn = forward_nacional(start_date,end_date)
    df_total_activos,df_nacional,df_internacional = inversiones(start_date,end_date)
    df_activos = activos(start_date,end_date)
    df_extranjeros = extranjeros(start_date,end_date)
    df_vf = vcfondos(start_date,end_date)
    df_q = vqfondos(start_date,end_date)
    
    if not df_fn.empty: 
        df_fn.to_sql("forwards_nacionales",
                       database,
                       if_exists='append',
                       schema='public',
                       index=False,
                       chunksize=500,
                       dtype={"Fecha": DateTime,
                              "Nombre": Text,
                              "Fondo_A": Float,
                              "Fondo_B": Float,
                              "Fondo_C": Float,
                              "Fondo_D": Float,
                              "Fondo_E": Float,
                              "TOTAL": Float}
                   )
    else:
        print("Error inesparado: forwards nacionales")
        
    if not df_total_activos.empty: 
        df_total_activos.to_sql("inversion_total",
                       database,
                       if_exists='append',
                       schema='public',
                       index=False,
                       chunksize=500,
                       dtype={"Fecha": DateTime,
                              "Nombre": Text,
                              "MMUSD_A": Float,
                              "Porcentaje_A": Float,
                              "MMUSD_B": Float,
                              "Porcentaje_B": Float,
                              "MMUSD_C": Float,
                              "Porcentaje_C": Float,
                              "MMUSD_D": Float,
                              "Porcentaje_D": Float,
                              "MMUSD_E": Float,
                              "Porcentaje_E": Float,
                              "MMUSD_TOTAL": Float,
                              "Porcentaje_TOTAL": Float}
                   )
    else:
        print("Error inesparado: inversión total")
        
    if not df_nacional.empty: 
        df_nacional.to_sql("inversion_nacional",
                       database,
                       if_exists='append',
                       schema='public',
                       index=False,
                       chunksize=500,
                       dtype={"Fecha": DateTime,
                              "Nombre": Text,
                              "MMUSD_A": Float,
                              "Porcentaje_A": Float,
                              "MMUSD_B": Float,
                              "Porcentaje_B": Float,
                              "MMUSD_C": Float,
                              "Porcentaje_C": Float,
                              "MMUSD_D": Float,
                              "Porcentaje_D": Float,
                              "MMUSD_E": Float,
                              "Porcentaje_E": Float,
                              "MMUSD_TOTAL": Float,
                              "Porcentaje_TOTAL": Float}
                   )
    else:
        print("Error inesparado: inversión nacional")
        
    if not df_internacional.empty: 
        df_internacional.to_sql("inversion_internacional",
                       database,
                       if_exists='append',
                       schema='public',
                       index=False,
                       chunksize=500,
                       dtype={"Fecha": DateTime,
                              "Nombre": Text,
                              "MMUSD_A": Float,
                              "Porcentaje_A": Float,
                              "MMUSD_B": Float,
                              "Porcentaje_B": Float,
                              "MMUSD_C": Float,
                              "Porcentaje_C": Float,
                              "MMUSD_D": Float,
                              "Porcentaje_D": Float,
                              "MMUSD_E": Float,
                              "Porcentaje_E": Float,
                              "MMUSD_TOTAL": Float,
                              "Porcentaje_TOTAL": Float}
                   )
    else:
        print("Error inesparado: inversión internacional")
        
    if not df_activos.empty: 
        df_activos.to_sql("activos",
                       database,
                       if_exists='append',
                       schema='public',
                       index=False,
                       chunksize=500,
                       dtype={"Fecha": DateTime,
                              "Nombre": Text,
                              "Porcentaje_A": Float,
                              "Porcentaje_B": Float,
                              "Porcentaje_C": Float,
                              "Porcentaje_D": Float,
                              "Porcentaje_E": Float,
                              "Porcentaje_TOTAL": Float,
                              "MM_TOTAL": Float,
                              "MMUSD_TOTAL": Float}
                   )
    else:
        print("Error inesparado: activos")
        
    if not df_extranjeros.empty: 
        df_extranjeros.to_sql("extranjeros",
                       database,
                       if_exists='append',
                       schema='public',
                       index=False,
                       chunksize=500,
                       dtype={"Fecha": DateTime,
                              "Nombre": Text,
                              "ASIA_EMERGENTE": Float,
                              "ASIA_PACIFICO": Float,
                              "EUROPA": Float,
                              "EUROPA_EMERGENTE": Float,
                              "LATINOAMERICA": Float,
                              "MEDIO_ORIENTE_AFRICA": Float,
                              "NORTEAMERICA": Float,
                              "OTROS": Float,
                              "MMUSD_TOTAL": Float}
                   )
    else:
        print("Error inesparado: extranjeros")

    if not df_vf.empty: 
        df_vf.to_sql("valor_fondos",
                       database,
                       if_exists='append',
                       schema='public',
                       index=False,
                       chunksize=500,
                       dtype={"Fecha": DateTime,
                              "VF_A": Float,
                              "VF_B": Float,
                              "VF_C": Float,
                              "VF_D": Float,
                              "VF_E": Float
                             }
                   )
    else:
        print("Error inesparado: valor fondos")
        
    if not df_q.empty: 
        df_q.to_sql("q_index",
                       database,
                       if_exists='append',
                       schema='public',
                       index=False,
                       chunksize=500,
                       dtype={"Fecha": DateTime,
                              "Q_A": Float,
                              "Q_B": Float,
                              "Q_C": Float,
                              "Q_D": Float,
                              "Q_E": Float
                             }
                   )
    else:
        print("Error inesparado: q index")
        
    session.commit()
    
#READ
def query_by_daterange(label,start_date,end_date):
    #elegir tabla
    if label == 'forwards_nacionales':
        input_rows = session.query(FORWARDS_NACIONALES).filter(FORWARDS_NACIONALES.Fecha.between(start_date,end_date))
    elif label == 'inversion_nacional':
        input_rows = session.query(INVERSION_NACIONAL).filter(INVERSION_NACIONAL.Fecha.between(start_date,end_date))
    elif label == 'inversion_internacional':
        input_rows = session.query(INVERSION_INTERNACIONAL).filter(INVERSION_INTERNACIONAL.Fecha.between(start_date,end_date))
    elif label == 'inversion_total':
        input_rows = session.query(INVERSION_TOTAL).filter(INVERSION_TOTAL.Fecha.between(start_date,end_date))
    elif label == 'activos':
        input_rows = session.query(ACTIVOS).filter(ACTIVOS.Fecha.between(start_date,end_date))
    elif label == 'extranjeros':
        input_rows = session.query(EXTRANJEROS).filter(EXTRANJEROS.Fecha.between(start_date,end_date))
    elif label == 'valor_fondos':
        input_rows = session.query(VALOR_FONDOS).filter(VALOR_FONDOS.Fecha.between(start_date,end_date))
    elif label == 'q_index':
        input_rows = session.query(Q_INDEX).filter(Q_INDEX.Fecha.between(start_date,end_date))
    else:
        return None

    df = pd.read_sql(input_rows.statement, input_rows.session.bind)
    df = df.drop(columns='index')
    
    return df


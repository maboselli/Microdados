#!/usr/bin/python3

# Autor: Marco A. Boselli, Universidade federal de Uberlândia.

import pandas as pd
import numpy as np
from datetime import datetime, timedelta


#-----------------------------------------------------------------
# dados que mudam e devem ser entrados:

today_date_str = "".join(str(datetime.now().date()))
today_read_str = "".join(str(datetime.now().date())).replace('-','.')

data_1 = np.datetime64(datetime.now().date() - timedelta(days=18))
data_2 = np.datetime64(datetime.now().date() - timedelta(days=4))

ano = str(datetime.today().year)
mes = '{:02d}'.format(datetime.today().month)


url = 'https://www.vs.saude.ms.gov.br/wp-content/uploads/'
csv_url = url + f'{ano}/{mes}/Microdados-{today_read_str}.csv'

print(f'Dados coletados em: {csv_url}')
print(f'Data: {today_date_str}')
      
cols_list = ['MUNICÍPIO RESIDÊNCIA AJUSTADO', 'DATA AJUSTADA', 'STATUS', 'DATA DO ÓBITO']
#remote 
df = pd.read_csv(csv_url, sep =';', usecols=cols_list)
#local
#df = pd.read_csv('Microdados-2020.08.04.csv', sep = ';', usecols=cols_list)

print('Lido')

df = df.replace('-',np.NaN)
# Muito louco, mas só assim funcionou: 
df['DATA DO ÓBITO'] = pd.to_datetime(df['DATA DO ÓBITO'])
df['DATA DO ÓBITO'] = pd.to_datetime(df['DATA DO ÓBITO'], format="%Y-%m-%d", utc=True)
df['DATA DO ÓBITO'] = df['DATA DO ÓBITO'].dt.tz_convert(None)
#
df['DATA AJUSTADA'] = pd.to_datetime(df['DATA AJUSTADA'])

#df.to_csv('Micordados_hoje.csv')
  
def get_casos(data, df):
    df_interno = df.set_index(['MUNICÍPIO RESIDÊNCIA AJUSTADO', 'DATA AJUSTADA']).sort_index()
    df_data = df_interno.iloc[df_interno.index.get_level_values('DATA AJUSTADA') <= data]
    df_data = df_data.loc[df_data['STATUS'] == 'CONFIRMADO']
    casos = df_data.reset_index().groupby('MUNICÍPIO RESIDÊNCIA AJUSTADO')['STATUS'].count()  
    d1 = df_data.reset_index()
    d1 = d1[d1['DATA DO ÓBITO'] <= data]
    obitos = d1.groupby('MUNICÍPIO RESIDÊNCIA AJUSTADO')['DATA DO ÓBITO'].count()
    return casos, obitos

casos_data1, obitos_data1 = get_casos(data_1, df)
casos_data2, obitos_data2 = get_casos(data_2, df)



col1 = 'Casos-' + str(data_1)
col2 = 'Obitos-' + str(data_1)
col3 = 'Casos-' + str(data_2)
col4 = 'Obitos-' + str(data_2)

nome = f'Microdados_analisados_MS_proc_{today_date_str}.csv'

df_final = pd.DataFrame({col1:casos_data1, col2: obitos_data1, col3:casos_data2, col4: obitos_data2})
df_final.to_csv(nome)

print(f'Dados salvos no arquivo: {nome}')
print('Fim do processo')

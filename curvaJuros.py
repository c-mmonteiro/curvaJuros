from datetime import datetime
import investpy
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from diFuturo import *


#############################################
#Titulos do Brasil
dados_full = pd.DataFrame(columns=['Codigo', 'Taxa', 'Vencimento', 'VRaw'])

titulos = investpy.get_bonds('brazil')

for t_name in titulos['name']:
    information = investpy.get_bond_information(bond=t_name)

    dados = investpy.get_bond_recent_data(bond=t_name)
    dados_full = dados_full.append({'Codigo': t_name, 
    'Taxa': dados['Close'][len(dados['Close'])-1], 
    'Vencimento': information['Maturity Date'][0],
    'VRaw': datetime.strptime(information['Maturity Date'][0], '%d/%m/%Y')},  
    ignore_index=True)
##################################################
#Tesouro direto
dados_td = pd.DataFrame(columns=['Codigo', 'Taxa', 'Vencimento', 'VRaw'])

titulos = investpy.search_quotes(text='tesouro', products=["bonds"], countries=['brazil'])

hoje = datetime.today()

for sr in titulos:
    if sr.symbol[0:3] == "LTN":
        nome = sr.name
        vencimento = datetime.strptime(sr.retrieve_information()['maturityDate'], '%b %d, %Y')
        if hoje < vencimento:
            valor = sr.retrieve_recent_data()['Close'][len(sr.retrieve_recent_data()['Close'])-1]
            dados_td = dados_td.append({'Codigo': nome, 
                'Taxa': (((1000/valor)**(365/(vencimento-hoje).days))-1)*100, 
                'Vencimento': vencimento.strftime('%d/%m/%Y'),
                'VRaw': vencimento},  
                ignore_index=True)
##############################################################
#DI Futuro
curvaDI_hj = diFuturo().get_curva_DI(0)
curvaDI_mes = diFuturo().get_curva_DI(22)

##############################################################
#Plot 

fig, ax = plt.subplots(1,1)

ax.set_title("Curva de Juros BR")
ax.plot(dados_full["VRaw"], dados_full["Taxa"], marker='.', label = 'Titulos')
ax.plot(curvaDI_hj["VRaw"], curvaDI_hj["Taxa"], marker='.', label = 'DI')
ax.plot(curvaDI_mes["VRaw"], curvaDI_mes["Taxa"], marker='.', label = 'DI - 1 Mês')
ax.plot(dados_td["VRaw"], dados_td["Taxa"], marker='.', label = 'TD')

ax.grid()
ax.legend()
ax=plt.xticks(curvaDI_hj["VRaw"], curvaDI_hj["Vencimento"], rotation=90) 

plt.show()

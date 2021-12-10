import MetaTrader5 as mt5
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta


class diFUturo:
    def __init__(self):
        hoje = datetime.today()

        mt5.initialize()

        self.listaSimbolos = mt5.symbols_get("DI1")

        self.vencimentos = []

        for l in self.listaSimbolos:
            if l.expiration_time > hoje.timestamp():
                exist = 0
                for v in self.vencimentos:
                    if v == l.expiration_time:
                        exist = 1
                if exist == 0:
                    self.vencimentos.append(l.expiration_time)
        self.vencimentos.sort()

       # mt5.shutdown()

    def get_curva_DI(self, dia):
        vencimentosDF = pd.DataFrame(columns=['Vencimento', 'Quantidade', 'Simbolo', 'Taxa'])
      #  mt5.initialize()

        for v in self.vencimentos:
            count = 0
            for l in self.listaSimbolos:
                if l.expiration_time == v:
                    nome = l.name
                    vLast = l.last
                    count = count + 1

            if ((dia == 0) and (vLast != 0)):
                vencimento = datetime.utcfromtimestamp(v).strftime('%d/%m/%Y')
                vencimentosDF = vencimentosDF.append(
                    {"Vencimento": vencimento, "VRaw": datetime.strptime(vencimento, '%d/%m/%Y'),  
                    "Quantidade": count, "Simbolo": nome, "Taxa": vLast}, ignore_index=True)
            else:
                selecao = mt5.symbol_select(nome, True)
                if not selecao:
                    print(f'Adição do Symbol: {mt5.last_error()}')
                val = mt5.symbol_info(nome)
                vencimento = datetime.utcfromtimestamp(v).strftime('%d/%m/%Y')
                if val:          
                    vencimentosDF = vencimentosDF.append(
                        {"Vencimento": vencimento, "VRaw": datetime.strptime(vencimento, '%d/%m/%Y'), 
                        "Quantidade": count, "Simbolo": nome, "Taxa": val.last}, ignore_index=True)
                else:
                    vencimentosDF = vencimentosDF.append(
                        {"Vencimento": vencimento, "VRaw": 0, 
                        "Quantidade": count, "Simbolo": nome, "Taxa": 0}, ignore_index=True)
                    print(f'Valor: {mt5.last_error()}')


            mt5.shutdown()
        print(vencimentosDF)
        return vencimentosDF

    def plot_DI_semana(self, n):
        #Se n = 0 -> hoje
        #se n = 1 -> hoje e ontem
        #se n = 2 -> hoje e 1 semana
        #se n = 3 -> hoje, ontem e 1 semana

        curvaDI_hj = self.get_curva_DI(0)
        if ((n==1) or (n==3)):
            curvaDI_ontem = self.get_curva_DI(1)
        if ((n==2) or (n==3)):
            curvaDI_semana = self.get_curva_DI(5)

        fig, ax = plt.subplots(1,1)

        ax.set_title("Curva de Juros BR")
        ax.plot(curvaDI_hj["VRaw"], curvaDI_hj["Taxa"], marker='.', label = 'Hoje')
        if ((n==1) or (n==3)):
            ax.plot(curvaDI_ontem["VRaw"], curvaDI_ontem["Taxa"], marker='.', label = 'Ontem')
        if ((n==2) or (n==3)):
            ax.plot(curvaDI_semana["VRaw"], curvaDI_semana["Taxa"], marker='.', label = 'Semana')

        ax.grid()
        ax.legend()
        ax=plt.xticks(curvaDI_hj["VRaw"], curvaDI_hj["Vencimento"], rotation=90) 

        plt.show()



    








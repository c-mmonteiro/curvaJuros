import MetaTrader5 as mt5
from investpy.utils import data
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta


class diFuturo:
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
        vencimentosDF = pd.DataFrame(columns=['Vencimento', 'VRaw', 'Quantidade', 'Simbolo', 'Taxa'])
      #  mt5.initialize()

        for v in self.vencimentos:
            count = 0
            for l in self.listaSimbolos:
                if l.expiration_time == v:
                    nome = l.name
                    vLast = l.last
                    count = count + 1
            vencimento = datetime.utcfromtimestamp(v).strftime('%d/%m/%Y')
            if vLast != 0:
                if dia == 0:              
                    vencimentosDF = vencimentosDF.append(
                        {"Vencimento": vencimento, "VRaw": datetime.strptime(vencimento, '%d/%m/%Y'),  
                        "Quantidade": count, "Simbolo": nome, "Taxa": vLast}, ignore_index=True)
                else:
                    #selecao = mt5.symbol_select(nome, True)
                    #if not selecao:
                    #    print(f'Adição do Symbol {nome}: {mt5.last_error()}')
                    val = mt5.copy_rates_from(nome, mt5.TIMEFRAME_D1, dia, 1)               
                    if val:
                        if val['close'][0] == 0:
                            print(f'Ativo sem valor no MT5 {nome}')
                        else:         
                            vencimentosDF = vencimentosDF.append(
                                {"Vencimento": vencimento, "VRaw": datetime.strptime(vencimento, '%d/%m/%Y'), 
                                "Quantidade": count, "Simbolo": nome, "Taxa": val['close'][0]}, ignore_index=True)
                    else: 
                        print(f'Valor {nome}: {mt5.last_error()}')


        mt5.shutdown()
        print(vencimentosDF)
        return vencimentosDF



    








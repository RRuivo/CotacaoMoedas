import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter.filedialog import askopenfilename
import pandas as pd
import requests
from datetime import datetime
import numpy as np


requisicao = requests.get(f'https://economia.awesomeapi.com.br/json/all')
#https://docs.awesomeapi.com.br/api-de-moedas
dicionario_moedas = requisicao.json()

lista_moedas = list(dicionario_moedas.keys())


def pegar_cotacao():
    moeda = combobox_selecionarmoeda.get()
    data_cotacao = calendario_moeda.get()
    ano = data_cotacao[-4:]
    mes = data_cotacao[3:5]
    dia = data_cotacao[:2]
    link = f'https://economia.awesomeapi.com.br/json/daily/{moeda}-BRL/?start_date={ano}{mes}{dia}&end_date={ano}{mes}{dia}'
    requisicao_moeda = requests.get(link)
    cotacao = requisicao_moeda.json()
    valor_moeda = cotacao[0]['bid']
    label_textocotacao['text'] = f'A cotação da moeda {moeda} no dia {data_cotacao} foi de:  R${valor_moeda}'


def selecionar_arquivo():
    caminho_arquivo = askopenfilename(title='Selecione o arquivo de moedas')
    var_caminhoarquivo.set(caminho_arquivo)
    if caminho_arquivo:
        label_arquivoselecionado['text'] = f'Arquivo selecionado {caminho_arquivo}'


def atualizar_cotacoes():
    try:
        #Ler o DF de moedas
        df = pd.read_excel(var_caminhoarquivo.get())
        moedas = df.iloc[:,0]
        # pegar data inicial e final das cotações
        data_inicial = calendario_datainicial.get()
        data_final = calendario_datafinal.get()
        ano_inicial = data_inicial[-4:]
        mes_inicial = data_inicial[3:5]
        dia_inicial = data_inicial[:2]

        ano_final = data_final[-4:]
        mes_final = data_final[3:5]
        dia_final = data_final[:2]

        for moeda in moedas:
            link = f'https://economia.awesomeapi.com.br/json/daily/{moeda}-BRL/31?'\
                   f'start_date={ano_inicial}{mes_inicial}{dia_inicial}&' \
                   f'end_date={ano_final}{mes_final}{dia_final}'

            requisicao_moeda = requests.get(link)
            cotacoes = requisicao_moeda.json()
            for cotacao in cotacoes:
                timestamp = int(cotacao['timestamp'])
                bid = float(cotacao['bid'])
                data = datetime.fromtimestamp(timestamp)
                data = data.strftime('%d/%m/%Y')
                if data not in df:
                    df[data] = np.nan

                df.loc[df.iloc[:, 0] == moeda, data] = bid

        df.to_excel('Testes.xlsx')
        label_atualizarcotacoes['text'] = 'Arquivo atualizado com sucesso!'

    except:
        label_atualizarcotacoes['text'] = 'Selecione um arquivo excel no formato correto'

janela = tk.Tk()

janela.title('Ferramenta de cotação de moedas')

#Cotação de 1 moeda

label_cotacaomoeda = tk.Label(text='Cotação de 1 moeda específica', borderwidth=2, relief='solid')
label_cotacaomoeda.grid(row=0, column=0, padx=10, pady=10, sticky='nswe', columnspan=3)

label_selecionarmoeda = tk.Label(text='Selecionar moeda', anchor='e')
label_selecionarmoeda.grid(row=1, column=0, padx=10, pady=10, sticky='nswe', columnspan=2)

combobox_selecionarmoeda = ttk.Combobox(values=lista_moedas)
combobox_selecionarmoeda.grid(row=1, column=2, padx=10, pady=10, sticky='nswe')

label_selecionardia = tk.Label(text='Selecionar o dia que deseja pegar cotação', anchor='e')
label_selecionardia.grid(row=2, column=0, padx=10, pady=10, sticky='nswe', columnspan=2)

calendario_moeda = DateEntry(year=2023, locale='pt_br')
calendario_moeda.grid(row=2, column=2, padx=10, pady=10, sticky='nswe')

label_textocotacao = tk.Label(text='')
label_textocotacao.grid(row=3, column=0, padx=10, pady=10, sticky='nswe', columnspan=2)

botao_pegarcotacao = tk .Button(text='Pegar cotação', command=pegar_cotacao)
botao_pegarcotacao.grid(row=3, column=2, padx=10, pady=10, sticky='nswe')

#Cotação de várias moedas

label_cotacaovariasmoedas = tk.Label(text='Cotação de múltiplas moedas', borderwidth=2, relief='solid')
label_cotacaovariasmoedas.grid(row=4, column=0, padx=10, pady=10, sticky='nswe', columnspan=3)

label_selecionararquivo = tk.Label(text='Selecione um arquivo Excel com as moedas na coluna A', anchor='e')
label_selecionararquivo.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky='nswe')

botao_selecionararquivo = tk.Button(text='Clique para selecionar', command=selecionar_arquivo)
botao_selecionararquivo.grid(row=5, column=2, padx=10, pady=10, sticky='nswe')

var_caminhoarquivo = tk.StringVar()

label_arquivoselecionado = tk.Label(text='Nenhum arquivo selecionado', anchor='e')
label_arquivoselecionado.grid(row=6, column=0, columnspan=3, padx=10, pady=10, sticky='nswe')

label_datainicial = tk.Label(text='Data inicial', anchor='e')
label_datainicial.grid(row=7, column=0, padx=10, pady=10, sticky='nswe')

calendario_datainicial = DateEntry(year=2023, locale='pt_br')
calendario_datainicial.grid(row=7, column=1, padx=10, pady=10, sticky='nswe')

label_datafinal = tk.Label(text='Data final', anchor='e')
label_datafinal.grid(row=8, column=0, padx=10, pady=10, sticky='nswe')

calendario_datafinal = DateEntry(year=2023, locale='pt_br')
calendario_datafinal.grid(row=8, column=1, padx=10, pady=10, sticky='nswe')

botao_atualizacotacoes = tk.Button(text='Atualizar cotações', command=atualizar_cotacoes)
botao_atualizacotacoes.grid(row=9, column=0, padx=10, pady=10, sticky='nswe')

label_atualizarcotacoes = tk.Label(text='')
label_atualizarcotacoes.grid(row=9, column=1, padx=10, pady=10, sticky='nswe', columnspan=2)

botao_fechar =tk.Button(text='Fechar', command=janela.quit)
botao_fechar.grid(row=10, column=2, padx=10, pady=10, sticky='nswe')

janela.mainloop()
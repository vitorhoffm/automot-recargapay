import os
import PySimpleGUI as sg
from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bot import test_get_infos

# Nome do arquivo onde os CNPJs serão armazenados
input_file = 'entrada_cnpjs.txt'
output_file = 'output_cnpjs.txt'
content = ''
cnpjs = []  # Lista para armazenar os CNPJs inseridos
log_text = ""

# Carrega o conteúdo do arquivo no início do programa
if os.path.isfile(input_file):
    with open(input_file, 'r') as arquivo:
        content = arquivo.read()
        cnpjs = [cnpj.strip() for cnpj in content.split('\n') if cnpj.strip()]


if not os.path.isfile(input_file):
    # O arquivo não existe, então você pode criá-lo e adicionar conteúdo
    with open(input_file, 'w') as arquivo:
        arquivo.write('')

if not os.path.isfile(output_file):
    # O arquivo de saída não existe, então você pode criá-lo
    with open(output_file, 'w') as arquivo:
        pass  # Não é necessário escrever nada nele inicialmente


# Layout do menu
menu_def = [
    ['Config', ['Adicionar CNPJ', 'Bot']],
]

# Layout da janela principal
layout = [
    [sg.Menu(menu_def)],
    [sg.Text("Insira um CNPJ:")],
    [sg.InputText(key='cnpj')],
    [sg.Button('Adicionar CNPJ'), sg.Button('Salvar Lista')],
    [sg.Text("CNPJs adicionados:")],
    [sg.Multiline(content, size=(40, 10), key='cnpjs_adicionados')],
]

window = sg.Window('Automot RecargaPay', layout)


appium_server_url = 'http://localhost:4723'
capabilities = dict(
    platformName='Android',
    automationName='uiautomator2',
    deviceName='',
    platformVersion='',
    appPackage='com.recarga.recarga',
    appActivity='com.recarga.recarga:id/action_bar_root',
    #appActivity='com.recarga.recarga.react.ReactHomeActivity',
)


while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break
    elif event == 'Adicionar CNPJ':
        cnpj_digitado = values['cnpj']
        if cnpj_digitado:
            cnpjs.append(cnpj_digitado)
            window['cnpj'].update('')  # Limpa o campo de entrada
            window['cnpjs_adicionados'].update('\n'.join(cnpjs))  # Atualiza a lista de CNPJs na interface
    elif event == 'Salvar Lista':
        # Salva os CNPJs no arquivo
        with open(input_file, 'a') as arquivo:
            arquivo.write('\n'.join(cnpjs))

        sg.popup('CNPJs foram salvos no arquivo.', title='adição de CNPJ')
    elif event == 'Bot':
        window.close()
        layout_bot = [
            [sg.Text("Modelo do Celular'"), sg.InputText(key='deviceName')],
            [sg.Text("Versão do Android'"), sg.InputText(key='platformVersion')],
            [sg.Text("CPF da sua conta'"), sg.InputText(key='CPFvalue')],
            [sg.Button('Iniciar Bot')],
            [sg.Multiline('',size=(40, 10), key='logs_adicionados')],
        ]
        window_bot = sg.Window('Configurações do Bot', layout_bot)

        while True:
            event_bot, values_bot = window_bot.read()

            if event_bot == sg.WINDOW_CLOSED:
                break
            elif event_bot == 'Iniciar Bot':
                # Atualize as configurações do Bot
                capabilities['deviceName'] = values_bot['deviceName']
                capabilities['platformVersion'] = values_bot['platformVersion']

                # Inicialize o driver com as configurações do Bot
                driver = webdriver.Remote(appium_server_url, capabilities)

                # Execute test_get_infos para cada CNPJ
                for cnpj in cnpjs:
                    test_get_infos(driver, cnpj, values_bot['CPFvalue'])
            
                # Feche o driver após concluir todas as execuções
                driver.quit()
                break



# Feche a janela principal
window.close()

from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

import PySimpleGUI as sg

output_file = 'output_cnpjs.txt'


# Função para executar ações do Bot e salvar informações
def test_get_infos(driver, cnpj) -> None:
    # Execute as ações do Bot aqui
   
    time.sleep(60)
    print('bot iniciado')
    try:
        # clica na categoria "Fazer Pix"
        WebDriverWait(driver, 35).until(EC.element_to_be_clickable((By.ID, 'Fazer Pix'))).click()

        # insere o CNPJ da lista
        WebDriverWait(driver, 25).until(EC.element_to_be_clickable((By.CLASS_NAME, 'android.widget.EditText'))).click()
        WebDriverWait(driver, 25).until(EC.element_to_be_clickable((By.CLASS_NAME, 'android.widget.EditText'))).send_keys(cnpj)

        # clica no botão continuar
        WebDriverWait(driver, 25).until(EC.element_to_be_clickable((By.CLASS_NAME, 'android.widget.Button'))).click()
        # ...
        name_pix = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.view.ViewGroup/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup[2]/android.view.ViewGroup[1]/android.view.ViewGroup/android.widget.TextView')))
        name_pix = name_pix.text

        name_cnpj = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.view.ViewGroup/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup[2]/android.view.ViewGroup[2]/android.view.ViewGroup/android.widget.TextView')))
        name_cnpj = name_cnpj.text

        name_instituicao = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.view.ViewGroup/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup[2]/android.view.ViewGroup[3]/android.view.ViewGroup/android.widget.TextView')))
        name_instituicao = name_instituicao.text

        # Salva as informações em um arquivo
        with open(output_file, 'a') as arquivo:
            arquivo.write("====================================\n")
            arquivo.write(f"Nome Pix: {name_pix}\n")
            arquivo.write(f"Nome CNPJ: {name_cnpj}\n")
            arquivo.write(f"Nome Instituição: {name_instituicao}\n")
            arquivo.write("====================================\n")
            arquivo.write("\n")  # Adicione uma linha em branco para separar as informações de cada CNPJ
    except TimeoutException:
        print("O campo de email não apareceu a tempo")
        # Lidar com o caso em que o campo de email não apareceu a tempo (por exemplo, se o usuário não interagir com a página)
        pass




    
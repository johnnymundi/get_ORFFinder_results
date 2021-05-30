# utilizo o selenium para acessar o link do cd search e pegar o elemento textarea que corresponde ao box para digitar a sequência de nucleotídeos
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# o time eh utilizado para dar um tempo para a página com o resultado ser carregada, principalmente naquelas com muito JS
import time

# função que recebe um arquivo fasta e o transforma em uma lista ou dicionário (tô decidindo)


def sequence_list(file):
    # sequences - lista somente com a sequências nucleotídicas
    sequences = []
    # tags - lista somente com o título dado às sequências nucleotídicas
    tags = []
    i = 0
    for line in file:
        line = line.rstrip()
        i += 1
        if '>' not in line:
            sequences.append(line)
        else:
            tags.append(line)

    print("Esse arquivo possui: ", len(tags), " sequências nucleotídicas")
    return sequences, tags


# função que jogar cada sequência no ORFfinder, pega o frame de leitura da primeira ORF e salva num arquivo .txt
# além disso, retorna somente uma lista como frame de leitura do primeiro ORF resultante
def orffinder_search(list):
    # o terceiro argumento é o nome do output
    output = open(sys.argv[2], 'w')
    sequences, tags = sequence_list(list)
    # o output para outra função é result_list:
    result_list = []

    # abre o navegador Chrome
    driver = webdriver.Chrome(
        executable_path="C:/Program Files (x86)/chromedriver.exe")
    # acessa o link do cd search
    driver.get("https://www.ncbi.nlm.nih.gov/orffinder/")

    # loop que vai encontrar a ORF de cada sequência:
    for tag in range(len(sequences)):

        # pega o id correspondente ao elemento textarea onde digitamos à sequência
        textarea = driver.find_elements_by_tag_name('textarea')[0]
        # envia a sequência para o textarea
        textarea.send_keys(sequences[tag])  # arquivo com a sequência

        # clica no botão Submit para ver o resultado da busca
        button = driver.find_element_by_id('button_submit')
        button.click()
        time.sleep(4)  # espera um tempo para aparecer o resultado

        # full endereço xpath da primeira linha da coluna Strand
        direction = driver.find_element_by_xpath(
            "/html/body/div[1]/div[1]/div[4]/div[4]/div[5]/div[3]/div/div[2]/table/tbody/tr[1]/td[2]").text

        # full endereço xpath da primeira linha da coluna Frame
        frame = driver.find_element_by_xpath(
            "/html/body/div[1]/div[1]/div[4]/div[4]/div[5]/div[3]/div/div[2]/table/tbody/tr[1]/td[3]").text

        # salva em result o nome da sequência e na linha seguinte a direção e frame
        # de leitura
        result = str(tags[tag]) + '\n' + str(direction) + str(frame) + '\n'

        # salva no output o result
        output.write(result)
        # salva na lista somente o frame de leitura
        result_list.append(frame)

        # print(result_list) # esse é só pra debug

        # clica em 'Go back to the submitting page...'
        reset = driver.find_element_by_xpath(
            "/html/body/div[1]/div[1]/div[4]/div[4]/div[6]/a")
        reset.click()

    return print(result_list)


# o segundo argumento é o nome do arquivo fasta
fasta_file = open(sys.argv[1], 'r')
orffinder_search(fasta_file)

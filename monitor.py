"""
SITUAÇÃO:	
	Extrair dados de consumo de recursos do servidor e disponibilizá-los em arquivos externos, os quais devem ser consumidos em um segundo momento.

OBJETIVO:
	Auxiliar no controle de consumo de recursos de servidores/desktops.

HISTÓRICO:
	01/01/2021 - Alexsandre Macaulay
"""

import datetime
import time
import psutil

# Importando módulos para obtenção de dados do sistema operacional
#------------------------------------------------------------------

# Instanciando o método today()
#------------------------------------------------------------------

today = datetime.date.today()

# Criando e incializando o arquivo com o consumo de recursos do SO
#------------------------------------------------------------------

file_hist = open(f"Consumo_Recursos_{today}.csv","w")
file_hist.write('"Data";"Ano";"Mes";"Dia";"Horas";"Minutos";"Segundos";"Hora Completa";"RAM(%)";"CPU(%)"\n')
file_hist.close()

# Inicializando a variável que armazena a hora
#------------------------------------------------------------------

time_hours = 0

# Condição para execução. Garante que o programa rode até às 22h
#------------------------------------------------------------------

while time_hours <= 21 :
                                                        #------------------------------------------------------------------
    date_event = datetime.datetime.now()                # Data e hora completa
    date = today.strftime("%d/%m/%Y")                   # Convertendo a data para dd/mm/yyyy
    year = date[6:]                                     # Ano
    month = date[3:5]                                   # Mês
    day = date[0:2]                                     # Dia
    time_event = str(date_event)[-15:-7]                # Hora completa
    time_hours = int(time_event[:2])                    # Hora
    time_minutes = int(time_event[3:5])                 # Minutos
    time_seconds = int(time_event[6:])                  # Segundos
    mem = psutil.virtual_memory()                       # Variável recebe o método virtual_memory() percentual de consumo de RAM
    cpu = psutil.cpu_percent()                          # Variável recebe o método cpu_percent() percentual de consumo de CPU
    cpu_usage = str(cpu).replace(".",",")               # Variável recebe o valor em
    mem_usage = str((mem.percent)).replace(".",",")     # Variável recebe o percentual de consumo de Memória RAM
                                                        #------------------------------------------------------------------

    #------------------------------------------------------------------
    # Abrindo o arquivo e gravando a data, hora, consumo de RAM e CPU
    # Importante ressaltar que existem dois arquivos:
    #
    #   1 - Consumo_Recursos_{today} 
    #       -> Armazena os dados de todo o dia desde às 6h até às 22h.
    #       -> É atualizado a cada minuto
    #
    #   2 - Consumo_Recursos 
    #       -> Armazena os dados do último minuto
    #       -> É sobrescrito a cada minuto
    #------------------------------------------------------------------

    file_hist = open(f"Consumo_Recursos_{today}.csv","a")
    file_hist.write(f'"{date}";"{year}";"{month}";"{day}";"{time_hours}";"{time_minutes}";"{time_seconds}";"{time_hours}:{time_minutes}:{time_seconds}";"{mem_usage}";"{cpu_usage}"\n')
    file_hist.close()

    file_job = open("Consumo_Recursos.csv","w")
    file_job.write('"Data";"Ano";"Mes";"Dia";"Horas";"Minutos";"Segundos";"Hora Completa";"RAM(%)";"CPU(%)"\n')
    file_job.write(f'"{date}";"{year}";"{month}";"{day}";"{time_hours}";"{time_minutes}";"{time_seconds}";"{time_hours}:{time_minutes}:{time_seconds}";"{mem_usage}";"{cpu_usage}"\n')
    file_job.close()

    # Aguardando 60s para retornar ao loop
    #------------------------------------------------------------------

    time.sleep(60)
    

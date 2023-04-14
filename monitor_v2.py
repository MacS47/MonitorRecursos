"""
SITUAÇÃO:	
	Esse projeto foi desenvolvido para comunicar a equipe apropriada, sempre que necessário intervir
	devido a consumo excessivo de recursos do servidor. O código se aproveita de recursos como a 
	procedure de envio de e-mails do banco de dados SQL Server. Todavia, o cerne do script é Python.
	Por meio dele o banco de dados é acessado e informações do servidor em questão são obtidas.

OBJETIVO:
	Auxiliar no controle de consumo de recursos de servidores/desktops.

HISTÓRICO:
	01/01/2022 - Alexsandre Macaulay
"""

import datetime
import time
import psutil
import pyodbc

driver = "DRIVER"
server_name = "SEU_SERVIDOR"
database_name = "SEU DATABASE"
user = "USER"
password = "PASSWORD"
STRING_CONNECTION = "DRIVER={driver};SERVER={server_name};DATABASE={database_name};UID={user};PWD={password}"

# Importando módulos para obtenção de dados do sistema operacional
#------------------------------------------------------------------

# Instanciando o método today()
#------------------------------------------------------------------
today = datetime.date.today()

def store_db(cpu,ram):

    connect = pyodbc.connect(STRING_CONNECTION)
    cursor = connect.cursor()
    cursor.execute("""INSERT INTO NOME_DATABASE.dbo.NOME_TABELA(DATA, TIME, RAM, CPU)
                       VALUES(?,?,?,?)
                    """,(data,time_event,ram,cpu))
    connect.commit()


# Configuração de e-mail de aviso
#------------------------------------------------------------------

def send_mail(cpu, ram):

    connect = pyodbc.connect(STRING_CONNECTION)
    cursor = connect.cursor()
    sql = ("""BEGIN 

  DECLARE @texthtml  NVARCHAR(MAX) ;

 SET @texthtml =  
  N' 
<!DOCTYPE html>
<html lang="en">
    <head>
        <style>
            html{
                font-family: system-ui, -apple-system, BlinkMacSystemFont, ''Segoe UI'', Roboto, Oxygen, Ubuntu, Cantarell, ''Open Sans'', ''Helvetica Neue'', sans-serif;
            }
            .box{
                border: 1px solid #b9b9b9;
                border-radius: 10px;
            }
            .center{
                width: 400px;
                padding: 10px;
                margin: auto;
                text-align: center;
            }
            .card{
                border-radius: 30px;
                width: 40%;
                margin: auto;
                display: inline-block;
                margin: 10px;
            }
            .icon{
                width: 40px;
                padding-top: 15px;
            }
            .title{
                background-color: #f0bb28;
                color: #000000;
                margin-bottom: 15px;
            }
            .paragraph{
                color: #000000;
                margin-bottom: 15px;
            }
            .resource-title{
                color: #000000;
                margin-bottom: 15px;
            }
            .resource{
                width: 400px;
                margin: auto;
                text-align: center;
                margin-bottom: 15px;
            }
            .card{
                border: 1px solid #b9b9b9;
                border-radius: 10px;
                padding-top: 10px;
            }
            .details{
                font-size: 9px;
            }
        </style>
    </head>
    <body>
        <div class="center title box">
            <h1>Aviso</h1>
        </div>
        <div class="center paragraph box ">
            <h3>SERVER NAME</h3>
        </div>
        <div class="center resource-title box">
            <h3>Consumo de recursos</h3>
            <p>"""+str(data) +""" - """+str(time_event)+"""</p>
        </div>
        <div class="resource">
            <div class="card cpu">
                <h3>CPU</h3>
                <h2>"""+str(cpu)+"""%</h2>
            </div>
            <div class="card ram">
                <h3>RAM</h3>
                <h2>"""+str(ram)+"""%</h2>
            </div>
        </div>
        <div class="center footer box">
            <p class="details">Este é um e-mail automático, não responda. Quaisquer dúvidas, entre em contato com seu.suporte@gmail.com.</p>
        </div>
    </body>
</html>';  


        EXEC msdb.dbo.sp_send_dbmail
        @profile_name ='Perfil',
        @recipients='destinatarios@gmail.com',
        @subject = 'Assunto E-mail',
        @body = @texthtml,  
        @body_format = 'HTML';
END
""")

    cursor.execute(sql)
    connect.commit()

# Inicializando a variável que armazena o status do servidor
#------------------------------------------------------------------

environment_not_ok = True

# Condição para execução. Garante que o programa rode até às 22h
#------------------------------------------------------------------

while environment_not_ok:
                                                        #------------------------------------------------------------------
    date_event = datetime.datetime.now()                # Data e hora completa
    data = today.strftime("%d/%m/%Y")                   # Convertendo a data para dd/mm/yyyy
    year = data[6:]                                     # Ano
    month = data[3:5]                                   # Mês
    day = data[0:2]                                     # Dia
    time_event = str(date_event)[-15:-7]                # Hora completa
    time_hours = int(time_event[:2])                    # Hora
    time_minutes = int(time_event[3:5])                 # Minutos
    time_seconds = int(time_event[6:])                  # Segundos
    mem = psutil.virtual_memory()                       # Variável recebe o método virtual_memory() percentual de consumo de RAM
    cpu = psutil.cpu_percent()                          # Variável recebe o método cpu_percent() percentual de consumo de CPU
    cpu_usage = str(cpu).replace(".",",")               # Variável recebe o valor em
    mem_usage = str((mem.percent)).replace(".",",")     # Variável recebe o percentual de consumo de Memória RAM
                                                        #------------------------------------------------------------------

    if mem.percent >= 65:
        store_db(cpu, mem.percent)
        send_mail(cpu, mem.percent)
        environment_not_ok = False
    else:
        environment_not_ok = False

    # Aguardando 60s para retornar ao loop
    #------------------------------------------------------------------
    #time.sleep(180)
    

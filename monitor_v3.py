"""
SITUAÇÃO:	
	Esse projeto foi desenvolvido para notificar a equipe apropriada, sempre que o script precisou
    intervir devido a consumo excessivo de recursos do servidor. O código se aproveita de recursos como a 
	procedure de envio de e-mails do banco de dados SQL Server. Todavia, o cerne do script é Python.
	Por meio dele o banco de dados é acessado e informações do servidor em questão são obtidas e, dependendo
    das circunstâncias ele mesmo realizada o encerramento dos processos onerosos.

OBJETIVO:
	Auxiliar no controle de consumo de recursos de servidores/desktops.

HISTÓRICO:
	01/01/2022 - Alexsandre Macaulay
"""
import datetime, psutil, pyodbc

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


# Método responsável pelo inserção do consumo de recursos na tabela auxiliar no SQL Server
#------------------------------------------------------------------
def store_db(cpu,ram):

    connect = pyodbc.connect(STRING_CONNECTION)
    cursor = connect.cursor()
    cursor.execute("""INSERT INTO NOME_DATABASE.dbo.NOME_TABELA(DATA, TIME, RAM, CPU)
                       VALUES(?,?,?,?)
                    """,(data,time_event,ram,cpu))
    connect.commit()


# Método responsável por enviar o e-mail de aviso
#------------------------------------------------------------------

def send_mail(cpu, ram, to_html):

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
            .text-justify{
                margin: auto;
                margin-bottom: 15px;
                width: 80%;
                text-align: justify;
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
            <h3>NOME SERVIDOR</h3>
        </div>
        <div class="center resource-title box">
            <h3>Consumo de recursos</h3>
            <p>"""+str(data)+""" - """+str(time_event)+"""</p>
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
        <div class="center resource-title box">
            <h3>Processo(s) Encerrado(s)</h3>
            """+str(to_html)+"""
        </div>
        <div class="center resource-title box">
            <h3>Observação</h3>
            <p class="text-justify">&emsp;Esse e-mail é uma notificação sobre a identificação de alto consumo de recursos no servidor NOME SERVIDOR. Os processos responsáveis pela utilização excessiva de recursos foram encerrados.</p>
        </div>
        <div class="center footer box">
            <p class="details">Este é um e-mail automático, não responda. Quaisquer dúvidas, entre em contato com seu.suporte@gmail.com .</p>
        </div>
    </body>
</html>';  

        EXEC msdb.dbo.sp_send_dbmail
        @profile_name ='Perfil',
        @recipients= 'destinatarios@gmail.com',
        @subject = 'Assunto E-mail',
        @body = @texthtml,  
        @body_format = 'HTML';
END
""")
    # Executando o sql e fechando a conexão com o banco de dados
    cursor.execute(sql)
    connect.commit()


# Método responsável por encerrar processos no servidor
#------------------------------------------------------------------
def kill_process():

    # Instanciando o array que armazenara o(s) id(s) do(s) processo(s)
    # com consumo excessivo de recursos
    pid_kill = []

    PROCESS_NAME = "nome_processo.exe"
    
    # Loop para percorrer todos os processos ativos no S.O.
    for procs in psutil.process_iter(['pid','name']):

        # Armazenando o Process Identification
        pid = procs.info.get('pid')

        # Armazenando o nome do processo
        name = procs.info.get('name')

        # Verificando se o nome do processo éPROCESS_NAME        
        if name == PROCESS_NAME:

            # Criando instância psutil.Process(), passando o parâmetro pid na variável p
            p = psutil.Process(pid)
            
            # Verificando se o consumo de RAM do processo atual, ultrapassou 16%
            if (p.memory_percent() > 16): 

                # Armazenando o(s) id(s) do(s) processo(s) encerrado(s)
                pid_kill.append(pid)

                # Encerrando o processo
                p.terminate()

    # Declarando a variável que receberá o(s) processo(s)
    # com alto consumo de recursos, em formato html
    to_html = ''

    # Loop criado para percorrer o array pid_kill e listar todos o id existentes, ou seja
    # todos os processos que foram encerrados
    for p in pid_kill:

        # Armazenando como string, dentro de tags HTML
        to_html += str(f'<p>'+str(p) +""" - """+str(PROCESS_NAME)+'</p>')

    # Retornando o html com o(s) processo(s) encerrado(s)
    return to_html


environment_not_ok = True

# Verificando a variável de controle
if environment_not_ok:
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

    # Verificando se o consumo de RAM ultrapassou os 65%
    if mem.percent >= 65:
        
        # Declarando a variável que receberá o código HTML com a lista de processos encerrados
        to_html = ''

        # Chamando a função que armazena no SQL Server a hora em que o consumo excessivo de RAM foi registrado
        store_db(cpu, mem.percent)

        # Chamando a função que encerra processos com alto consumo e armazenando o seu resultado na variável to_html
        to_html = kill_process()

        # Chamando a função que dispara e-mail de notificação à equipe de responsável
        send_mail(cpu, mem.percent, to_html)

        # Alterando o valor da variável de controle, para encerrar a aplicação com segurança
        environment_not_ok = False
    else:
        # Alterando o valor da variável de controle, para encerrar a aplicação com segurança
        environment_not_ok = False

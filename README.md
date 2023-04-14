# MonitorRecursos

## Sumário

* [Monitor - 1.0](#versão-10)
* [Monitor - 2.0](#versão-20)
* [Monitor - 3.0](#versão-30)

## Versão 1.0

Monitor de recursos em Python criado para auxiliar no monitoramento de recursos de servidores. O script encontrado em `monitor.py` cria um arquivo CSV, caso não exista, ou acrescenta novos dados de consumo. No servidor o qual estava sendo utilizado, o script foi convertido em executável e agendado para ser executado a cada 5 minutos.

## Versão 2.0

Esse script é uma evolução do primeiro, pois ele não gera mais um arquivo CSV onde dados de consumo são armazenados. Ao identificar uma anomalia, uma notificação via e-mail é encaminhada à equipe responsável. Dessa forma a equipe pode definir uma ação a ser tomada com base no estado do servidor.

## Versão 3.0

Essa versão realiza automaticamente a finalização do processo oneroso, afim de liberar recursos no servidor em questão. O código foi criado para propósitos corporativos específicos, mas nada impede que seja customizado para atender necessidades distintas.

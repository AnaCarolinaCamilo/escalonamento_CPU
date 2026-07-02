# Vai conter as funções principais como fcfs() representando First Come First Serve, sjf() Small Job First, rr() Round Robin com Quantum = 2
# As funções vão ser implementadas da seguinte forma:
# FCFS: fila simples
# SFJ: a cada momento que a cpu ficar livre verificar quais processos chegaram e escolher o que tem menor duração
# RR: fila circular usando o quantum especificado, se o processo rodar por 2 unidades de tempo e não terminar,
# volta pra o final da fila dos processos prontos.


from processo import Processo

import copy # para que os outros processos de escalonamento não peguem dados alterados


def escalonador_fcfs(processos_para_fcfs):
    # Garantir que processos estão na ordem de chegada 
    processos_para_fcfs.sort(key=lambda p: p.chegada)

    tempo_atual = 0;
    for p in processos_para_fcfs:
        # Se a CPU ficou ociosa esperando esse projeto chegar 
        if tempo_atual < p.chegada:
            tempo_atual = p.chegada

        p.tempo_inicio = tempo_atual
        tempo_atual += p.duracao
        p.tempo_conclusao = tempo_atual


def escalonador_sfj(processos_para_sjf):
    tempo_atual = 0
    processos_restantes = processos_para_sjf.copy() # lista para controlar quem falta rodar 

    while(processos_restantes):
        # filtra quem já chegou no tempo atual 
        disponiveis = [p for p in processos_restantes if p.chegada <= tempo_atual]

        if not disponiveis:
            # CPU ociosa, avança no relógio
            tempo_atual += 1
            continue
        # pega os processos com menores durações entre os disponíveis
        processo_escolhido = min(disponiveis, key=lambda p:p.duracao)

        # executa o processo 
        processo_escolhido.tempo_inicio = tempo_atual
        tempo_atual += processo_escolhido.duracao
        processo_escolhido.tempo_conclusao = tempo_atual

        # Remove da lista de pendentes 
        processos_restantes.remove(processo_escolhido)

def escalonador_rr(processos_para_rr):
    quantum = 2
    tempo_atual = 0
    fila_prontos = []

    # ordena por chegada inicialmente para saber quem entra primeiro
    processos_ordenados = sorted(processos_para_rr, key=lambda p:p.chegada)
    processos_pendentes = processos_ordenados.copy()

    while processos_pendentes or fila_prontos:
        # coloca na fila quem chegou no tempo_atual 
        # checar quem chegou enquanto a cpu estava rodando
        while processos_pendentes and processos_pendentes[0].chegada <= tempo_atual:
            fila_prontos.append(processos_pendentes.pop(0))

        if not fila_prontos:
            # Caso a cpu esteja ociosa
            tempo_atual += 1
            continue

        # pegar o primeiro da fila 
        p = fila_prontos.pop(0)

        # registrar o tempo de inicio APENAS se for a primeira vez na cpu
        if p.tempo_inicio == -1:
            p.tempo_inicio = tempo_atual
        
        # Descobre quanto tempo ele vai rodar nesse ciclo
        tempo_execucao = min(p.tempo_restante, quantum)

        # avança o tempo e diminui o tempo restante do processo
        tempo_atual += tempo_execucao
        p.tempo_restante -= tempo_execucao

        # verifica se novos processos chegaram DURANTE a execução desse quantum 
        # para colocar na fila ANTES do processo atual voltar para o final dela 

        while processos_pendentes and processos_pendentes[0].chegada <= tempo_atual:
            fila_prontos.append(processos_pendentes.pop(0))
        
        # se o processo ainda não terminou ele volta para o fim da fila
        if p.tempo_restante > 0:
            fila_prontos.append(p)
        else:
            p.tempo_conclusao = tempo_atual

# teste mock para testar o funcionamento dos algoritmos 

import sys
import copy

def imprimir_estatisticas(sigla, processos):
    """
    Calcula as médias e imprime no formato estrito do projeto.
    """
    n = len(processos)
    if n == 0:
        return

    # Soma as métricas de todos os processos
    soma_retorno = sum(p.tempo_retorno() for p in processos)
    soma_resposta = sum(p.tempo_resposta() for p in processos)
    soma_espera = sum(p.tempo_espera() for p in processos)

    # Calcula as médias
    media_retorno = soma_retorno / n
    media_resposta = soma_resposta / n
    media_espera = soma_espera / n

    # Formata com 1 casa decimal
    # Atenção: O Slide 7 usa dois pontos na sigla (ex: "FCFS: 10,0") 
    # enquanto o Slide 6 não usa (ex: "FCFS 30,5"). 
    # Use a string f"{sigla}: " se o professor confirmar o formato do Slide 7.
    linha_saida = f"{sigla} {media_retorno:.1f} {media_resposta:.1f} {media_espera:.1f}"
    
    # Substitui o ponto pela vírgula para bater com os exemplos do PDF
    linha_saida_formatada = linha_saida.replace('.', ',')
    
    print(linha_saida_formatada)

if __name__ == "__main__":
    # 1. Leitura de toda a entrada padrão até o Fim do Arquivo (EOF)
    dados_entrada = sys.stdin.read().split()
    
    lista_original = []
    pid_contador = 0
    
    # 2. Agrupa os números de 2 em 2 (chegada e duração)
    for i in range(0, len(dados_entrada), 2):
        chegada = int(dados_entrada[i])
        duracao = int(dados_entrada[i+1])
        
        # Cria o objeto Processo e adiciona na lista base
        novo_processo = Processo(pid_contador, chegada, duracao)
        lista_original.append(novo_processo)
        pid_contador += 1

    # Se o arquivo estiver vazio, encerra
    if not lista_original:
        sys.exit()

    # 3. Cria cópias independentes para não misturar os dados entre os algoritmos
    processos_fcfs = copy.deepcopy(lista_original)
    processos_sjf = copy.deepcopy(lista_original)
    processos_rr = copy.deepcopy(lista_original)

    # 4. Executa os algoritmos
    escalonador_fcfs(processos_fcfs)
    escalonador_sfj(processos_sjf)
    escalonador_rr(processos_rr)

    # 5. Imprime a saída formatada na ordem solicitada
    imprimir_estatisticas("FCFS", processos_fcfs)
    imprimir_estatisticas("SJF", processos_sjf)
    imprimir_estatisticas("RR", processos_rr)
        


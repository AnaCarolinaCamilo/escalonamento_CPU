# Definir a classe/ estrutura de dados dos processos 
# Aqui serão definidos os atributos básicos como
# tempo de chegada
# Duração
# ID
# E atributos dinâmicos como tempos restante, tempo de início e de conclusão
# Isso facilitará um escalonamento como Round Robin

class Processo:
    def __init__(self, pid, chegada, duracao):
        # informações base 
        self.pid = pid                # Identificador (0, 1, 2, etc.)
        self.chegada = chegada        # Momento em que chega na fila
        self.duracao = duracao        # Tempo total necessário na CPU
        
        # informações para controle da execução
        self.tempo_restante = duracao # Vai diminuindo durante o Round Robin
        
        # informações para calcular as métricas no final
        self.tempo_inicio = -1        # -1 significa que ainda não foi executado
        self.tempo_conclusao = 0      # Registra quando o processo terminou de vez

    # Métodos auxiliares para calcular as métricas solicitadas
    def tempo_resposta(self):
        # Tempo desde a chegada até a primeira vez na CPU
        return self.tempo_inicio - self.chegada

    def tempo_retorno(self):
        # Tempo total desde a chegada até a finalização
        return self.tempo_conclusao - self.chegada

    def tempo_espera(self):
        # Tempo total aguardando = Retorno - Tempo de CPU que ele realmente usou
        return self.tempo_retorno() - self.duracao
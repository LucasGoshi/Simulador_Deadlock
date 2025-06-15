# Simulador Integrado: Deadlock + Disco + RAM + Fragmentacao
# Lucas Campos Goshi, Renato, Leonardo, Guilherme, Nicolas

import multiprocessing

class Disco:
    def _init_(self, blocos):
        # Inicializa o disco com uma lista de blocos vazios (None)
        self.blocos = [None] * blocos

    def alocar(self, dado):
        import random
        # Identifica blocos livres (valores None)
        livres = [i for i, b in enumerate(self.blocos) if b is None]
        if livres:
            # Escolhe uma posição livre aleatoriamente e grava o dado
            i = random.choice(livres)
            self.blocos[i] = dado
            print(f"[HD] Gravado {dado} na posição {i}")
        else:
            print("[HD] Disco cheio")

    def desfragmentar(self):
        # Agrupa os dados ocupados para mover para o início do disco
        ocupados = [b for b in self.blocos if b is not None]
        # Reescreve os blocos com os dados ocupados seguidos de blocos vazios
        for i in range(len(self.blocos)):
            self.blocos[i] = ocupados[i] if i < len(ocupados) else None
        print("[HD] Disco desfragmentado")

    def fragmentacao(self):
        # Calcula a taxa de fragmentação do disco
        usados = [i for i in self.blocos if i is not None]
        if not usados:
            return 0.0  # Nenhum dado alocado
        blocos_fragmentados = 0
        # Conta as transições entre dados diferentes adjacentes
        for i in range(1, len(self.blocos)):
            if self.blocos[i] != self.blocos[i-1] and self.blocos[i] is not None:
                blocos_fragmentados += 1
        return blocos_fragmentados / len(usados)
    
class RAM:
    def _init_(self, total):
        self.total = total      # Total de memória disponível (em MB)
        self.usado = 0          # Quantidade de memória atualmente em uso

    def alocar(self, mb):
        """
        Tenta alocar uma quantidade de memória (em MB).
        Se houver espaço suficiente, aloca e retorna True.
        Caso contrário, retorna False e exibe mensagem de erro.
        """
        if self.usado + mb <= self.total:
            self.usado += mb
            print(f"[RAM] Alocado {mb}MB. Em uso: {self.usado}MB")
            return True
        else:
            print(f"[RAM] Falha ao alocar {mb}MB. Memória insuficiente.")
            return False

    def liberar(self, mb):
        """
        Libera uma quantidade de memória (em MB).
        Garante que o valor não fique negativo.
        """
        self.usado = max(0, self.usado - mb)
        print(f"[RAM] Liberado {mb}MB. Em uso: {self.usado}MB")

def usar_cpu():
    """
    Loop infinito da CPU que representa um processo que consome recursos computacionais.
    """
    while True:
        pass  # Executa continuamente, simulando processamento intenso

if _name_ == "_main_":
    print("== Teste: uso da CPU ==")
    
    # Inicia um processo por núcleo disponível na máquina
    for i in range(multiprocessing.cpu_count()):
        p = multiprocessing.Process(target=usar_cpu)
        p.start()

    print(f"[✓] {multiprocessing.cpu_count()} processos de uso de CPU iniciados.")
    print("[!] Pressione CTRL+C para interromper o teste.")

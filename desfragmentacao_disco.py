# Simulador Integrado: Deadlock + Disco + RAM + Fragmentacao
# Lucas Campos Goshi, Renato, Leonardo, Guilherme, Nicolas

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

if _name_ == "_main_":
    print("== Teste: Disco ==")
    disco = Disco(10)
    for i in range(5):
        disco.alocar(f"P{i}")
    print(f"Fragmentação: {disco.fragmentacao()*100:.1f}%")
    disco.desfragmentar()
    print(f"Fragmentação: {disco.fragmentacao()*100:.1f}%\n")

    print("== Teste: RAM ==")
    ram = RAM(500)  # Total de 500MB disponíveis
    ram.alocar(100)
    ram.alocar(250)
    ram.alocar(200)  # Deve falhar
    ram.liberar(150)
    ram.alocar(200)  # Agora deve funcionar
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

# Teste individual da classe Disco
if _name_ == "_main_":
    disco = Disco(10)  # Cria um disco com 10 blocos
    for i in range(5):
        disco.alocar(f"P{i}")  # Aloca 5 processos simulados
    print(f"Fragmentação: {disco.fragmentacao()*100:.1f}%")  # Exibe fragmentação antes
    disco.desfragmentar()  # Realiza desfragmentação
    print(f"Fragmentação: {disco.fragmentacao()*100:.1f}%")  # Exibe fragmentação depois

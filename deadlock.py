"""
Lucas Campos Goshi
Renato Sussumu Takahashi Junior
Leonardo Gomes Velani
Guilherme Covaleki
Nicolas Lopes Ferracioli
"""

import threading
import time

# Recursos compartilhados
R1 = threading.Lock()
R2 = threading.Lock()
R3 = threading.Lock()

# Função genérica para qualquer processo
def processo(nome, recursos, nome_rec):
    print(f"{nome} → está tentando pegar {nome_rec[0]}")

    acquired_first = recursos[0].acquire(timeout=5)

    if not acquired_first:
        print(f"{nome} não conseguiu {nome_rec[0]}. Saindo.\n")
        return

    print(f"{nome} pegou {nome_rec[0]}")
    time.sleep(1)

    # Verifica se há mais de um recursos
    if len(recursos) > 1:
        print(f"{nome} → está tentando pegar {nome_rec[1]}")

        acquired_second = recursos[1].acquire(timeout=5)
        
        if not acquired_second:
            print(f"{nome} não conseguiu {nome_rec[1]}. Liberando {nome_rec[0]}.\n")
            recursos[0].release()
            return

        print(f"{nome} pegou {nome_rec[1]}. Executando...\n")
        time.sleep(2)

        recursos[1].release()
        recursos[0].release()
    else:
        print(f"{nome} executando com {nome_rec[0]}...\n")
        time.sleep(2)
        recursos[0].release()

    print(f"{nome} terminou. Recursos liberados.\n")

# Criando os processos
P1 = threading.Thread(target=processo, args=("P1", [R1, R2], ["R1", "R2"]))
P2 = threading.Thread(target=processo, args=("P2", [R2, R1], ["R2", "R1"]))
P3 = threading.Thread(target=processo, args=("P3", [R3], ["R3"])) 

# Iniciando os processos
print("Iniciando a simulação...\n")
P1.start()
P2.start()
P3.start()
time.sleep(6)

# Detector de Deadlocks
if P1.is_alive() and P2.is_alive():
    print("\nDEADLOCK DETECTADO!")
    print("Interrompendo processos...\n")
    P1.join()
    P2.join()
    print("Simulação interrompida! Deadlock resolvido.")
else:
    print("Execução concluída sem deadlock.")

# Processos onde não serão deadlock
P3.join()

grafo_espera = {
    "P1": ["P2"],  # P1 está esperando por P2
    "P2": ["P1"],  # P2 está esperando por P1
    "P3": []       # P3 não espera por ninguém
}

def tem_ciclo(grafo):
    visitado = set()
    pilha = set()

    def dfs(no):
        visitado.add(no)
        pilha.add(no)
        for vizinho in grafo.get(no, []):
            if vizinho not in visitado:
                if dfs(vizinho):
                    return True
            elif vizinho in pilha:
                return True
        pilha.remove(no)
        return False

    for no in grafo:
        if no not in visitado:
            if dfs(no):
                return True
    return False

# Exemplo de uso:
if tem_ciclo(grafo_espera):
    print("Deadlock detectado!")
else:
    print("Sem deadlock.")

# Suponha que P1 está esperando por R2, que está com P2
grafo_espera["P1"] = ["P2"]

# Se P2 também está esperando por R1, que está com P1
grafo_espera["P2"] = ["P1"]

# Agora, tem_ciclo(grafo_espera) retornará True (deadlock)

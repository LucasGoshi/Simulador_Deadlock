""" 
Lucas Campos Goshi
Renato Sussumu Takahashi Junior
Leonardo Gomes Velani
Guilherme Covaleki
Nicolas Lopes Ferracioli 
"""

# Importação para criar e gerenciar Threads e a outra para controlar o tempo
import threading
import time

# Lock - garante que apenas uma thread por vez possa acessar um recurso compartilhado (Processo de Cooperação).
R1 = threading.Lock()
R2 = threading.Lock()
R3 = threading.Lock()  # Novo recurso exclusivo para P3

def processo(nome, primeiro_recurso, segundo_recurso, nome_r1, nome_r2):
    print(f"{nome} → está tentando pegar {nome_r1}")

    acquired_first = primeiro_recurso.acquire(timeout=5)
    if not acquired_first:
        print(f"{nome} não conseguiu {nome_r1}. Saindo.\n")
        return

    print(f"{nome} pegou {nome_r1}")
    time.sleep(1)

    print(f"{nome} → está tentando pegar {nome_r2}")

    acquired_second = segundo_recurso.acquire(timeout=5)
    if not acquired_second:
        print(f"{nome} não conseguiu {nome_r2}. Liberando {nome_r1}.\n")
        primeiro_recurso.release()
        return

    print(f"{nome} pegou {nome_r2}. Executando...\n")
    time.sleep(2)

    segundo_recurso.release()
    primeiro_recurso.release()
    print(f"{nome} terminou. Recursos liberados.\n")

# Criando os processos (threads)
P1 = threading.Thread(target=processo, args=("P1", R1, R2, "R1", "R2"))
P2 = threading.Thread(target=processo, args=("P2", R2, R1, "R2", "R1"))
P3 = threading.Thread(target=processo_simples, args=("P3", R3, "R3"))  # Processo independente

# Iniciar os processos
print("Iniciando a simulação...\n")
P1.start()
P2.start()
P3.start()
time.sleep(6)

# Detector de Deadlock entre P1 e P2
if P1.is_alive() and P2.is_alive():
    print("\nDEADLOCK DETECTADO!")
    print("Interrompendo processos...\n")
    P1.join()
    P2.join()
    print("Simulação interrompida! Deadlock resolvido.")
else:
    print("Execução concluída sem deadlock.")

# Aguarda o término de P3 (não envolvido no deadlock)
P3.join()

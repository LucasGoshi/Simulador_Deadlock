import multiprocessing
import threading
import time
import random

def fragmentar_disco(disco_virtual, disco_cheio_evento):
    while True:
        time.sleep(2)
        dado = f"D{random.randint(100, 999)}"
        indices_livres = [i for i, bloco in enumerate(disco_virtual) if bloco is None]

        if indices_livres:
            i = random.choice(indices_livres)
            disco_virtual[i] = dado
            print(f"[Fragmentador] Gravou {dado} na posição {i}")
        else:
            print("[Fragmentador] Disco cheio. Parando fragmentação.")
            disco_cheio_evento.set()
            break

if _name_ == "_main_":
    multiprocessing.freeze_support()
    manager = multiprocessing.Manager()
    disco_virtual = manager.list([None] * 20)
    disco_cheio_evento = multiprocessing.Event()

    fragmentador = threading.Thread(target=fragmentar_disco, args=(disco_virtual, disco_cheio_evento))
    fragmentador.start()
    fragmentador.join()

    print("Estado final do disco:", list(disco_virtual))
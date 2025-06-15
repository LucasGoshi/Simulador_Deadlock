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

def desfragmentar_disco(disco_virtual, disco_cheio_evento, desfragmentado_evento):
    while True:
        time.sleep(5)
        dados = [b for b in disco_virtual if b is not None]

        for i in range(len(disco_virtual)):
            disco_virtual[i] = dados[i] if i < len(dados) else None

        print("[Desfragmentador] Disco desfragmentado.")
        print("Estado atual:", list(disco_virtual))

        if disco_cheio_evento.is_set() and all(b is not None for b in disco_virtual):
            print("[Desfragmentador] Finalizado. Disco 100% cheio e desfragmentado.\n")
            desfragmentado_evento.set()
            break

if _name_ == "_main_":
    multiprocessing.freeze_support()
    manager = multiprocessing.Manager()
    disco_virtual = manager.list([None] * 20)

    disco_cheio_evento = multiprocessing.Event()
    desfragmentado_evento = multiprocessing.Event()

    fragmentador = threading.Thread(target=fragmentar_disco, args=(disco_virtual, disco_cheio_evento))
    desfragmentador = threading.Thread(target=desfragmentar_disco, args=(disco_virtual, disco_cheio_evento, desfragmentado_evento))

    fragmentador.start()
    desfragmentador.start()

    desfragmentado_evento.wait()
    print("Simulação concluída.")

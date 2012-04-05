from huffman_functions import Huff, Unhuff

if __name__ == "__main__":

    op_control = {
        'e': Huff,
        'd': Unhuff
    }

    op = raw_input("Vuoi comprimere o decomprimere? (e/d): ")
    in_file = raw_input("Nome del file d'ingresso: ")
    out_file = raw_input("Nome del file d'uscita: ")
    choice = raw_input("Vuoi calcolare frequenze o usare statistiche? (f/s): ")

    # Perform operation
    op_control[op](in_file, out_file, choice)
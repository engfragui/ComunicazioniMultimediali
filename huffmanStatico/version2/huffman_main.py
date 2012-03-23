from huffman_functions import Huff, Unhuff

def main():

    op_control = {
            'e': Huff,
            'd': Unhuff
            }

    op = raw_input("Vuoi comprimere o decomprimere? (e/d): ")
    in_file = raw_input("Inserisci il nome del file in ingresso: ")
    out_file = raw_input("Inserisci il nome del file in uscita: ")

    # Perform operation
    op_control[op](in_file, out_file)

if __name__ == "__main__":

    main()
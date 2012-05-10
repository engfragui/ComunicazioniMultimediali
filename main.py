#prima di far partire il file bisogna:
#creare una cartella con nome esempio
#mettere all'interno della cartella il file esempio.txt
#insomma: cartella e file si devono chiamare allo stesso modo
#alla fine dell'esecuzione, nella cartella compariranno i file generati dal programma

import rle
import huf

import os

if __name__ == "__main__":

    print "Benvenuto!\n"

    file = raw_input("Inserisci il nome del file: ")

    #preparo nomi dei file
    file_split = file.split(".")
    file_name = file_split[0]
    #run length encoding
    file_com_rl = file_name + "_com_rl.txt"
    file_dec_rl = file_name + "_dec_rl.txt"
    #huffman statico con frequenze calcolate ad hoc
    file_com_hf = file_name + "_com_hf.txt"
    file_dec_hf = file_name + "_dec_hf.txt"
    #huffman statico con utilizzo di statistiche fisse
    file_com_hs = file_name + "_com_hs.txt"
    file_dec_hs = file_name + "_dec_hs.txt"

    #entro nella cartella
    os.chdir(file_name)

    #faccio partire rle
    rle.main(file, file_com_rl, file_dec_rl)
    #faccio partire huffman con calcolo frequenze
    huf.main(file, file_com_hf, file_dec_hf, True) #True perche' gli dico di fare con calcolo frequenze
    #faccio partire huffman usanto statistiche fisse
    huf.main(file, file_com_hs, file_dec_hs, False) #True perche' gli dico di fare con statistiche fisse
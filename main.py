#prima di far partire il file bisogna:
#creare una cartella con nome esempio
#mettere all'interno della cartella il file esempio.txt
#insomma: cartella e file si devono chiamare allo stesso modo
#alla fine dell'esecuzione, nella cartella compariranno i file generati dal programma

#per fare i colori
#print '\033[95m' + "prova" + '\033[0m' #fucsia
#print '\033[94m' + "prova" + '\033[0m' #blu
#print '\033[92m' + "prova" + '\033[0m' #verde
#print '\033[91m' + "prova" + '\033[0m' #rosso


import all
import rle
import huf

import os

if __name__ == "__main__":

    print "\nBenvenuto!\n"

    file = raw_input("Inserisci il nome del file: ")

    print ""

    language = raw_input("Scegli una lingua (ita/eng): ")

    #preparo nomi dei file
    file_split = file.split(".")
    file_name = file_split[0]
    #huffman statico con frequenze calcolate ad hoc
    file_com_hf = file_name + "_com_hf.txt"
    file_dec_hf = file_name + "_dec_hf.txt"
    #huffman statico con utilizzo di statistiche fisse
    file_com_hs = file_name + "_com_hs.txt"
    file_dec_hs = file_name + "_dec_hs.txt"
    #run length encoding
    file_com_rl = file_name + "_com_rl.txt"
    file_dec_rl = file_name + "_dec_rl.txt"

    #entro nella cartella
    os.chdir(file_name)

    #utility che conta il numero dei caratteri
    print "\nFile originale"
    all.dim(file)

    #faccio partire huffman con calcolo frequenze
    huf.main(file, file_com_hf, file_dec_hf) #non specifico language -> calcolo frequenze

    #faccio partire huffman usanto statistiche fisse
    huf.main(file, file_com_hs, file_dec_hs, language) #specifico language -> statistiche fisse

    #faccio partire rle
    rle.main(file, file_com_rl, file_dec_rl)
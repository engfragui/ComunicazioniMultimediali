class rle:

    def encode(self, file_input, file_output):

        f = open(file_input, 'r') #apro file di input in lettura
        o = open(file_output, 'w') #apro file di output in scrittura
        t = f.read() #leggo tutto il file
        counter = 0
        lastChar = t[0]
        strout = ""
        for c in t: #scorro tutti i caratteri contenuti nel file
            if lastChar == c: #se il carattere precedente e' UGUALE a quello attuale
                counter += 1 #incremento contatore
            else: #se carattere precedente e' DIVERSO da quello attuale
                strout += lastChar + str(counter) + ";" #scrivo quello precedente
                lastChar = c #inizializzo il carattere attuale
                counter = 1
        strout += lastChar + str(counter) + ";" #scrivo anche l'ultimo carattere
        o.write(strout) #scrivo l'output in ASCII (in questo modo e' visibile) sul file_output
        o.close() #chiudo file_output
        f.close() #chiudo file_input

    def decode(self, file_input, file_output):

        f = open(file_input, 'r') #apro file di input in lettura
        o = open(file_output, 'w') #apro file di output in scrittura
        t = f.read() #leggo tutto il file
        lastChar = ""
        strout = ""
        char = ""
        counter = 0
        state = 0
        for c in t: #scorro tutti i caratteri contenuti nel file
            if state == 0: #se lo stato e' ancora a 0
                char = c #leggo il carattere (la lettera)
                state = 1 #metto lo stato a 1
            else: #ovvero se lo stato e' a 1
                if c != ';': #se non sono ancora arrivata al ;
                    lastChar += c #leggo (e appendo) i caratteri (ottengo il numero)
                else: #sono arrivata a ;
                    counter = int(lastChar) #converto in intero il numero
                    i = 0
                    while i < counter: #finche' i e' piu' piccolo del numero che devo scrivere
                        strout += char #scrivo un carattere
                        i += 1 #aumento il contatore
                    lastChar = ""
                    char = ""
                    state = 0;

        o.write(strout) #scrivo l'output sul file_output
        o.close() #chiudo file_output
        f.close() #chiudo file_input

def main(file, file_com_rl, file_dec_rl):

    print "--Run Length Encoding"

    print "---Compressione del file"

    erle = rle()
    erle.encode(file, file_com_rl)

    print "---Decompressione del file"

    drle = rle()
    drle.decode(file_com_rl, file_dec_rl)
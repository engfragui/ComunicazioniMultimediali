import all

from bitarray import bitarray
import binascii
import time

class rle:

    def newstrout(self,counter,lastChar):

        counter_bin = '%(#)08d' % {"#" : int(bin(counter)[2:])} #converto il counter in una stringa di 1 e 0
        ba = bitarray(counter_bin) #dalla stringa ricavo l'oggetto bitarray
        return ba.tobytes() + lastChar #scrivo il carattere precedente preceduto dal counter salvato come singolo byte

    def encode(self, file_input, file_output):

        f = open(file_input, 'r') #apro file di input in lettura
        o = open(file_output, 'w') #apro file di output in scrittura
        t = f.read() #mi carico in memoria tutto il file per evitare continue operazioni di lettura
        counter = 0
        lastChar = t[0]
        strout = ""

        for c in t: #scorro tutti i caratteri contenuti nel file

            if lastChar == c: #se il carattere precedente e' uguale a quello attuale
                counter += 1 #incremento il contatore
                if counter==256: #quando ho letto 256 caratteri tutti uguali devo scrivere i primi 255 su file e memorizzare il 256esimo
                    strout += self.newstrout(255,lastChar)
                    counter = 1

            else: #se carattere precedente e' diverso da quello attuale
                strout += self.newstrout(counter,lastChar)
                lastChar = c #inizializzo il carattere attuale
                counter = 1

        strout += self.newstrout(counter,lastChar) #scrivo anche l'ultimo carattere
        o.write(strout) #scrivo l'output in ASCII (in questo modo e' visibile) sul file_output
        o.close() #chiudo file_output
        f.close() #chiudo file_input


    def decode(self, file_input, file_output):

        f = open(file_input, 'r') #apro file di input in lettura
        o = open(file_output, 'w') #apro file di output in scrittura
        t = f.read() #leggo tutto il file
        strout = ""
        state = 0

        for c in t: #scorro tutti i caratteri contenuti nel file

            if state == 0: #state = 0 --> c e' il counter
                ba = bitarray()
                ba.frombytes(c) #dal byte mi ricavo l'oggetto bitarray
                if ba[0]: #ossia se il primo carattere della stringa di bit e' a 1 (numero > di 127) non posso convertire in string
                    ba[0] = 0 #azzero il primo carattere
                    counter_int = int(binascii.b2a_hex(ba.tostring()),16) #converto prima in esadecimale e poi in decimale
                    counter_int += 128 #aggiungo 10000000(bin) = 128(dec) che avevo tolto all'inizio
                else:
                    counter_int = int(binascii.b2a_hex(ba.tostring()),16) #converto prima in esadecimale e poi in decimale
                state = 1 #metto lo stato a 1

            else: #state = 1 --> c e' il carattere
                for i in range(0,counter_int): #per un numero counter_int di volte
                    strout += c #scrivo il carattere
                state = 0

        o.write(strout) #scrivo l'output sul file_output
        o.close() #chiudo file_output
        f.close() #chiudo file_input


def main(file, file_com_rl, file_dec_rl):

    print "\nRUN LENGTH ENCODING"

    print "Codifica"
    now = time.time()
    #compressione del file
    erle = rle()
    erle.encode(file, file_com_rl)
    print "\t" + str(time.time() - now) + "\tseconds"
    all.dim(file_com_rl)

    print "Decodifica"
    now = time.time()
    #decompressione del file
    drle = rle()
    drle.decode(file_com_rl, file_dec_rl)
    print "\t" + str(time.time() - now) + "\tseconds"
    all.dim(file_dec_rl)

    all.check(file,file_dec_rl)
import heapq
import struct
from collections import defaultdict

def char_freq(file_obj, mode): #Costruisce tabelle delle frequenze a partire dai caratteri presenti nel file
    #mode=True calcolo io le frequenze, mode=False uso statistiche

    freq = defaultdict(int) #lista di elementi in cui il primo e' il carattere, il secondo la frequenza

    if mode: #se devo calcolare io le frequenze dei vari caratteri

        for line in file_obj:
            for ch in line:
                freq[ch] += 1

    else: #se devo usare statistiche prefissate

        freq['\n'] = 1
        freq[' '] = 1
        freq[','] = 906
        freq['.'] = 1319
        freq[';'] = 11

        freq['A'] = 1
        freq['B'] = 111111
        freq['C'] = 11111
        freq['D'] = 108
        freq['E'] = 40
        freq['F'] = 49
        freq['G'] = 0
        freq['H'] = 0
        freq['I'] = 92
        freq['L'] = 17
        freq['M'] = 142
        freq['N'] = 174
        freq['O'] = 0
        freq['P'] = 183
        freq['Q'] = 52
        freq['R'] = 0
        freq['S'] = 142
        freq['T'] = 0
        freq['U'] = 36
        freq['V'] = 93
        freq['Z'] = 0

        freq['a'] = 4783
        freq['b'] = 728
        freq['c'] = 2414
        freq['d'] = 1657
        freq['e'] = 6779
        freq['f'] = 390
        freq['g'] = 783
        freq['h'] = 337
        freq['i'] = 5844
        freq['j'] = 76
        freq['l'] = 3452
        freq['m'] = 2570
        freq['n'] = 3487
        freq['o'] = 2536
        freq['p'] = 1378
        freq['q'] = 723
        freq['r'] = 3317
        freq['s'] = 5001
        freq['t'] = 5045
        freq['u'] = 5311
        freq['v'] = 926
        freq['z'] = 0

    print "ecco la tabella delle frequenze:"
    print freq.items()

    print "ecco la HuffStructure:"
    print HuffStructure(freq.iteritems())

    return HuffStructure(freq.iteritems()) #generazione della tabella delle frequenze

def write_header(f_out_obj, frequency_table, mode): #Funzione che scrive l'header sul file

    if mode: #frequenze calcolate

        header = (struct.pack('I', frequency_table[chr(i)].freq) for i in xrange(256))
        #I significa unsigned int (ovvero utilizzo 4 bit per ogni carattere)
        #per ogni carattere ascii (256) ho salvato quante volte compare nel mio file

        f_out_obj.write(''.join(header))

    else: #uso statistiche

        print "Non faccio nulla"

def read_header(f_in, mode): #Funzione che legge l'header del file

    if mode: #frequenze calcolate

        header = f_in.read(1024) #leggo 1024 byte di header (256 caratteri x 4 byte ciascuno)
        #questo header non e' leggibile dall'utente finale

        unpacked_header = struct.unpack('256I', header)

        print unpacked_header

        return HuffStructure(((chr(ch_indx), freq) for ch_indx, freq in enumerate(unpacked_header) if freq))

    else: #uso statistiche

        return char_freq(f_in, mode)

def codify_to_huffman(f_in, f_out, codes): #Codifica il file sulla base dell'albero dei codici generato poco fa

    bstr = ''.join([codes[ch] for line in f_in for ch in line]) #mi salvo il file di input
    print "bstr" + str(bstr)
    bstr_len_by8, remaining = divmod(len(bstr), 8) #divido la lunghezza di bstr per 8

    bstrs = [bstr[i << 3:(i + 1) << 3] for i in xrange(bstr_len_by8)]
    obstrs = [int(obstr, 2) for obstr in bstrs]

    if remaining: #dobbiamo completare l'ultimo byte e farlo arrivare a 8 bit

        obstrs.append(int(bstr[-remaining:].ljust(8, '0'), 2))

    #Scriviamo il codice per identificare l'ultimo byte
    obstrs.append((8 - remaining) % 8)
    f_out.write(struct.pack('%dB' % len(obstrs), *obstrs))


def dec2bin(dec_list):
    """
    Converts a sequence of decimal numbers to binary representation
    and return a big string of 0's and 1's.
    """
    # calculate and store binary codes for the 256 symbols
    bincodes = dict((k, ''.join(['1' if ((1 << i) & k) else '0' \
                           for i in xrange(7, -1, -1)])) for k in xrange(256))

    return ''.join([bincodes[dec] for dec in dec_list])


def read_encoded(file_obj):
    """Reads a file compressed by huffman algorithm."""
    content = [ch for line in file_obj for ch in line]

    bstr = dec2bin(struct.unpack('%dB' % len(content), ''.join(content)))
    bstr = bstr[:-8 -int(bstr[-8:], 2)] # remove end code and extra bits

    # return a big string of 0's and 1's
    return bstr


def decode_huffman(f_out_obj, root, binstr):
    """Expects a file object and a binstr that is returned from
    read_encoded."""
    start = root

    for b in binstr:
        root = root.left if b == '0' else root.right

        if root.left is None and root.right is None:
            # found a leaf node, you found a symbol then
            f_out_obj.write(root.data)
            root = start


class HuffNode(object): #Rappresentazione di un nodo nell'albero

    def __init__(self, freq, data, left=None, right=None):
        self.freq = freq
        self.data = data
        self.left = left
        self.right = right

    def __cmp__(self, other_node): #Confronta i nodi in base alla frequenza (se hanno stessa frequenza va in base all'ordine alfabetico)

        res = cmp(self.freq, other_node)
        if res == 0 and hasattr(other_node, 'data'):
            #Se i caratteri hanno la stessa frequenza, li confronta in base all'ordine alfabetico
            res = cmp(self.data, other_node.data)

        return res

class HuffStructure(dict): #Albero dei caratteri

    def __init__(self, *args, **kwargs):
        self.update(*args, **kwargs)

        self.codes = {} # symbols' code
        self.tree_built = False

        # cache for ordered items (?)
        self.cached = False
        self._cached = None

    def __setitem__(self, key, value):

        #Se val non e' un HuffNode, con huffstruct[key] = val viene creato un nuovo HuffNode
        #Se val e' un HuffNode, con huffstruct[key] = val si risetta un nuovo valore per quella key

        if not isinstance(value, HuffNode):
            value = HuffNode(value, key)

        dict.__setitem__(self, key, value)

        # since the dict was updated, the cache is not valid anymore.
        self.cached = False

    def __getitem__(self, key):

        #Restituisce un nuovo new HuffNode con frequenza 0 e key come data nel caso in cui si voglia accedere a una chiave inesistente

        if dict.__contains__(self, key):
            value = dict.__getitem__(self, key)
        else:
            value = HuffNode(0, key)

            #Un nuovo nodo e' stato creato, quindi la cache non e' piu' valida
            self.cached = False

        return value

    def __delitem__(self, key):

        #Dopo la cancellazione di un elemento, la cache non e' piu' valida

        dict.__delitem__(self, key)
        self.cached = False

    def update(self, *args, **kwargs):

        #Si aspetta args[0] come un iterable con valori (x, y)

        for k, v in args[0]:
            self[k] = v

        self.cached = False

    def ordered_items(self):

        #Restituisce gli oggetti ordinati in base alla frequenza, cosi' poi sara' piu' facile e veloce costruire l'albero

        print "ordered_items"

        return self._cached_order()

    def build_tree(self): #Costruisce albero dei caratteri

        items = self.ordered_items()
        #items = lista di tuple (nodo, carattere) ordinata in base alla frequenza ed eventualmente all'ordine alfabetico
        print "Ecco la lista items:"
        print items

        while len(items) > 1: #finche' ci sono caratteri nella lista

            #Estraggo i due nodi con la frequenza piu' bassa
            node_left = heapq.heappop(items)
            node_right = heapq.heappop(items)
            print "pop del nodo " + node_left[1] + " che ha frequenza " + str(node_left[0].freq)
            print "e del nodo " + node_right[1] + " che ha frequenza " + str(node_right[0].freq)
            
            freq_sum = node_left[0].freq + node_right[0].freq #calcolo la somma delle loro frequenze
            repr_str = node_left[1] + node_right[1] #do come data del nodo la concatenazione dei due caratteri

            #Credo nuovo nodo, mettendo a sinistra e destra i due elementi poppati poco fa
            father = HuffNode(freq_sum, repr_str)
            father.left = node_left[0]
            father.right = node_right[0]

            #Aggiungo il padre alla lista dei nodi
            heapq.heappush(items, (father, repr_str))

            print "Ecco la lista items:"
            print items

        self.tree_built = True

        return items.pop()[0] #Restituisco la radice dopo aver costruito l'albero

    def generate_codes(self, root, code=''): #Genera ricorsivamente i codici per i caratteri a partire dall'albero

        if not self.tree_built:
            self.build_tree()

        if root.left is None and root.right is None: #Sono giunta ad una foglia (il codice per il simbolo e' completo)
            self.codes[root.data] = code
            print "carattere " + root.data + " ha codice " + code
        else:
            self.generate_codes(root.left, code + '0')
            self.generate_codes(root.right, code + '1')

    def _cached_order(self):

        #Restituisce gli elementi cached ordinati oppure li ordina e poi li mette in cache

        print "_cached_order"

        if self.cached:
            items = self._cached
        else:
            #costruisce gli elementi come tuple (frequenza, carattere) cosi' heapq estrarra' prima gli elementi con frequenza piu' bassa

            items = [(item[1], item[0]) for item in dict(self).iteritems()]

            heapq.heapify(items)
            self._cached = items
            self.cached = True

        return items


class HuffBase(object): #Classe base da cui ereditano Huff e Unhuff

    def __init__(self, file_in, file_out, encoding):

        if encoding:
            in_mode = 'r'
            out_mode = 'wb'
        else: #decoding
            in_mode = 'rb'
            out_mode = 'w'

        #apro i file
        self.file_in = open(file_in, in_mode)
        self.file_out = open(file_out, out_mode)

        self.root = None

    def _gen_codes(self): #Costruisce albero dei caratteri e genera codici per ciascun carattere

        self.root = self.freq_table.build_tree()
        self.freq_table.generate_codes(self.root)

    def _cleanup(self):

        #Chiude i file dopo averli utilizzati

        self.file_in.close()
        self.file_out.close()

class Huff(HuffBase): #Classe che si occupa della compressione del file

    def __init__(self, file_in, file_out, mode): #mode=True se calcolo frequenze, mode=False se uso statistiche

        HuffBase.__init__(self, file_in, file_out, True) #encoding=True

        self.freq_table = char_freq(self.file_in, mode) #creo tabella delle frequenze
        write_header(self.file_out, self.freq_table, mode) #se devo, scrivo l'header contenente le frequenze dei caratteri
        self._gen_codes() #genero codice per ciascun carattere
        self.file_in.seek(0) #mi metto all'inizio del file di input
        self._encode_input() #codifico il file
        self._cleanup() #chiudo i file

    def _encode_input(self):
        codify_to_huffman(self.file_in, self.file_out, self.freq_table.codes)


class Unhuff(HuffBase): #Classe che si occupa della decompressione

    def __init__(self, file_in, file_out, mode): #mode=True se calcolo frequenze, mode=False se uso statistiche

        HuffBase.__init__(self, file_in, file_out, False) #encoding=False
        
        self.freq_table = read_header(self.file_in, mode) #se devo, leggo tabella delle frequenze dall'header. se no, uso statistiche. in ogni caso, genero albero
        self._gen_codes() #genero codice per ciascun carattere
        self._decode_input() #decodifico il file
        self._cleanup() #chiudo i file

    def _decode_input(self):
        binstr = read_encoded(self.file_in)
        decode_huffman(self.file_out, self.root, binstr)


def main(file, file_com_huf, file_dec_huf, mode): #mode e' True se calcolo frequenze io, False se uso le statistiche

    if mode:
        print "--Huffman statico con calcolo delle frequenze"
    else:
        print "--Huffman statico con uso delle statistiche"

    print "---Compressione del file"
    Huff(file, file_com_huf, mode) #compressione

    print "---Decompressione del file"
    Unhuff(file_com_huf, file_dec_huf, mode) #decompressione
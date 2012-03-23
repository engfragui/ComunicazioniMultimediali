import heapq
import struct
from collections import defaultdict


def char_freq(file_obj):
    """Build a frequency table from chars read from input file."""
    freq = defaultdict(int)
    for line in file_obj:
        for ch in line:
            freq[ch] += 1

    return HuffStructure(freq.iteritems())


def read_header(f_in):
    """Reads a huffman header."""
    header = f_in.read(1024) # 256 symbols, 4 bytes each
    unpacked_header = struct.unpack('256I', header)

    return HuffStructure(((chr(ch_indx), weight) for ch_indx, \
                            weight in enumerate(unpacked_header) if weight))


def write_header(f_out_obj, frequency_table):
    """Write to file output a huffman header."""
    header = (struct.pack('I', frequency_table[chr(i)].weight) \
                for i in xrange(256))
    f_out_obj.write(''.join(header))


def codify_to_huffman(f_in, f_out, codes):
    """codes are the generated codes for input data."""
    bstr = ''.join([codes[ch] for line in f_in for ch in line])
    bstr_len_by8, remaining = divmod(len(bstr), 8)

    bstrs = [bstr[i << 3:(i + 1) << 3] for i in xrange(bstr_len_by8)]
    obstrs = [int(obstr, 2) for obstr in bstrs]

    if remaining:
        # we need to complete last byte, so make sure it is a good 8-bit
        # string
        obstrs.append(int(bstr[-remaining:].ljust(8, '0'), 2))

    # write the code that identifies end of huffman encoding
    # this is actually the last byte in the file.
    obstrs.append((8 - remaining) % 8) # last byte code
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


class NoSymbols(Exception):
    """Raised when trying to build a tree for an empty input file."""


class HuffNode(object):
    """Representation of a node in a 'Huffman tree'."""

    def __init__(self, weight, data, left=None, right=None):
        self.weight = weight
        self.data = data
        self.left = left
        self.right = right

    def __cmp__(self, other_node):
        """Compare nodes by their weight, if they weight the same, compare
        them by their data."""
        res = cmp(self.weight, other_node)
        if res == 0 and hasattr(other_node, 'data'):
            # symbols have same weight, compare by lexical order then
            res = cmp(self.data, other_node.data)

        return res


class HuffStructure(dict):
    """Data structure used in this Huffman implementation."""
    def __init__(self, *args, **kwargs):
        self.update(*args, **kwargs)

        self.codes = {} # symbols' code
        self.tree_built = False

        # cache for ordered items
        self.cached = False
        self._cached = None

    def __setitem__(self, key, value):
        """When doing huffstruct[key] = val, a new HuffNode is created,
        if val is not a HuffNode, where val is its weight and key its data.
        If val is a HuffNode, set a new node to the key."""
        if not isinstance(value, HuffNode):
            value = HuffNode(value, key)

        dict.__setitem__(self, key, value)
        # since the dict was updated, the cache is not valid anymore.
        self.cached = False

    def __getitem__(self, key):
        """Return a new HuffNode with 0 weight and key as its data, in
        case of trying to access an inexistant key."""
        if dict.__contains__(self, key):
            value = dict.__getitem__(self, key)
        else:
            value = HuffNode(0, key)
            # new node created, cache is invalid
            self.cached = False

        return value

    def __delitem__(self, key):
        """Upon item deletion we need to invalidate cache."""
        dict.__delitem__(self, key)
        self.cached = False

    def update(self, *args, **kwargs):
        """
        Custom dict update, expects args[0] to be an iterable with (x, y)
        values.
        """
        for k, v in args[0]:
            self[k] = v

        self.cached = False

    def ordered_items(self):
        """Return items ordered by weight, so it is easier and faster
        to build the tree later."""
        return self._cached_order()

    def build_tree(self):
        """Build tree from ordered items."""
        if not len(self):
            raise NoSymbols("input file is empty.")

        items = self.ordered_items()

        while len(items) > 1:
            # get the two first nodes, the ones with lowest weight
            node_left = heapq.heappop(items)
            node_right = heapq.heappop(items)
            
            weight_sum = node_left[0].weight + node_right[0].weight
            repr_str = node_left[1] + node_right[1]

            # construct a binary tree
            father = HuffNode(weight_sum, repr_str)
            father.left = node_left[0]
            father.right = node_right[0]

            # add father back to the heap
            heapq.heappush(items, (father, repr_str))

        self.tree_built = True
        return items.pop()[0] # root

    def generate_codes(self, root, code=''):
        """Generate codes from built tree by travessing it."""
        if not self.tree_built:
            self.build_tree()

        if root.left is None and root.right is None:
            # a leaf node here, the code for this symbol should be complete
            self.codes[root.data] = code
        else:
            self.generate_codes(root.left, code + '0')
            self.generate_codes(root.right, code + '1')

    def _cached_order(self):
        """Return cached items ordered, or, order them now and cache."""
        if self.cached:
            items = self._cached
        else:
            # construct items as tuples of (nodeweight, symbol) so heapq will
            # extract items with the lowest weight first
            items = [(item[1], item[0]) for item in dict(self).iteritems()]

            heapq.heapify(items)
            self._cached = items
            self.cached = True

        return items


class HuffBase(object):
    """Base class for encoding and decoding Huffman files."""

    def __init__(self, file_in, file_out, encoding=True):
        if encoding:
            in_mode = 'r'
            out_mode = 'wb'
        else:
            in_mode = 'rb'
            out_mode = 'w'

        self.file_in = open(file_in, in_mode)
        self.file_out = open(file_out, out_mode)

        self.root = None

    def _gen_codes(self):
        """Build tree and generate codes for current nodes on it."""
        self.root = self.freq_table.build_tree()
        self.freq_table.generate_codes(self.root)

    def _cleanup(self):
        self.file_in.close()
        self.file_out.close()


class Huff(HuffBase):
    def __init__(self, file_in, file_out):
        name = file_in
        HuffBase.__init__(self, file_in, file_out)

        self.freq_table = char_freq(self.file_in)
        write_header(self.file_out, self.freq_table)
        self._gen_codes()

        self.file_in.seek(0)
        self._encode_input()
        self._cleanup()

    def _encode_input(self):
        codify_to_huffman(self.file_in, self.file_out, self.freq_table.codes)


class Unhuff(HuffBase):
    def __init__(self, file_in, file_out):
        HuffBase.__init__(self, file_in, file_out, False)
        
        self.freq_table = read_header(self.file_in)
        self._gen_codes()
        self._decode_input()
        self._cleanup()

    def _decode_input(self):
        binstr = read_encoded(self.file_in)
        decode_huffman(self.file_out, self.root, binstr)

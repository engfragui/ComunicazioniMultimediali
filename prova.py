from bitarray import bitarray

a = bitarray('00100001')
abyte = a.tobytes()
print abyte
print len(a)
print a.length()

print a.tostring()

b = bitarray()
b.frombytes(abyte)
print b.tostring()
def modAdd(x, y, mod=26):
    return (x+y)%mod


def charToNum(char):
    offset=ord('a') if char.islower() else ord('A') if char.isupper() else None
    if offset is None:
        raise ValueError("charToNum only works with alphabetic chars (a-z, A-Z)")
    return ord(char)-offset


def numToChar(num, uppercase=True):
    if not 0 <= num < 26:
        raise ValueError("numToChar only accepts ints between 0 and 26")
    offset=ord('A') if uppercase else ord('a')
    return chr(num+offset)

def letterAdd(char, amt):
    return numToChar(modAdd(charToNum(char), amt), uppercase=char.isupper())




try:
    import numpy
except:
    pass
else:
    ### The following functions adapted from from http://stackoverflow.com/questions/4287721/easiest-way-to-perform-modular-matrix-inversion-with-python
##    def generalizedEuclidianAlgorithm(a, b):
##        if b > a:
##            #print a, b
##            return generalizedEuclidianAlgorithm(b,a);
##        elif b == 0:
##            return (1, 0);
##        else:
##            #print a,b
##            (x, y) = generalizedEuclidianAlgorithm(b, a % b);
##            return (y, x - (a / b) * y)
##    
##    def inverseMod(a, p):
##        a = a % p
##        if (a == 0):
##            return 0
##        (x,y) = generalizedEuclidianAlgorithm(p, a % p);
##        return y % p
##    
##    def identityMatrix(n):
##        mat=numpy.zeros((n, n))#, dtype=numpy.int32)
##        for x in range(n):
##            mat[x, x]=1
##        return mat
##    
##    def inverseMatrix(matrix, q):
##        n = len(matrix)
##        A = numpy.matrix([[ matrix[j, i] for i in range(0,n)] for j in range(0, n)])#, dtype = numpy.int32)
##        Ainv = numpy.matrix(identityMatrix(n))#, dtype = numpy.int32)
##        for i in range(0, n):
##            factor = inverseMod(A[i,i], q)
##            A[i] = A[i] * factor % q
##            Ainv[i] = Ainv[i] * factor % q
##            for j in range(0, n):
##                if (i != j):
##                    factor = A[j, i]
##                    A[j] = (A[j] - factor * A[i]) % q
##                    Ainv[j] = (Ainv[j] - factor * Ainv[i]) % q
##                    # print A, Ainv
##                    # print i, j, factor
##        return Ainv
    def modMatInv(A,p):       # Finds the inverse of matrix A mod p
      n=len(A)
      A=numpy.matrix(A)
      adj=numpy.zeros(shape=(n,n))
      for i in range(0,n):
        for j in range(0,n):
          adj[i][j]=((-1)**(i+j)*int(round(numpy.linalg.det(minor(A,j,i)))))%p
      return (modInv(int(round(numpy.linalg.det(A))),p)*adj)%p
    
    def modInv(a,p):          # Finds the inverse of a mod p, if it exists
      for i in range(1,p):
        if (i*a)%p==1:
          return i
      raise ValueError(str(a)+" has no inverse mod "+str(p))
    
##    def minor(A,i,j):    # Return matrix A with the ith row and jth column deleted
##      A=numpy.array(A)
##      minor=numpy.zeros(shape=(len(A)-1,len(A)-1))
##      p=0
##      for s in range(0,len(minor)):
##        if p==i:
##          p=p+1
##        q=0
##        for t in range(0,len(minor)):
##          if q==j:
##            q=q+1
##          minor[s][t]=A[p][q]
##          q=q+1
##        p=p+1
    
    ###
    
    #adapted from http://stackoverflow.com/questions/3858213/numpy-routine-for-computing-matrix-minors
    def minor(arr,i,j):
        # ith row, jth column removed
        return arr[numpy.array(list(range(i))+list(range(i+1,arr.shape[0])))[:,numpy.newaxis],
                   numpy.array(list(range(j))+list(range(j+1,arr.shape[1])))]
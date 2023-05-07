import sys

class TreeNode:
    def __init__(self, value = 0, prefix = '', filhos = []):
        self.value = value
        self.prefix = prefix
        self.filhos = filhos

class TrieTree:
    def __init__(self):
        self.root = TreeNode()
        self.num = 1
    def compress(self, s, file):
        currentNode = self.root
        for x in s:
            wasFound = False
            #print(currentNode.prefix)
            for y in currentNode.filhos:
                if x == y.prefix:
                    currentNode = y
                    wasFound = True
                    break
            if wasFound == False:
                newNode = TreeNode(self.num, x, [])
                self.num += 1
                currentNode.filhos.append(newNode)
                k = currentNode.value
                file.write(k.to_bytes(4, byteorder='big', signed=False))
                file.write(x.encode('utf8', 'strict'))
                #print(len(currentNode.filhos))
                currentNode = self.root
                #print(currentNode.value, currentNode.prefix, len(currentNode.filhos))
                #for k in currentNode.filhos: print(k.prefix)
                
    def decompress(self, file):
        dictionary = {}
        dictionary[0] = [0, '']
        #print(dictionary)
        index = 1;
        decompText = ""
        while True:
            prefix = file.read(4)
            prefix = int.from_bytes(prefix, "big")
            suffix = file.read(1)
            #print(suffix)
            if prefix == b'' or suffix == b'':
                break
            nBytes = ord(suffix)
            nBytes = bin(nBytes)[2:].rjust(8, '0')
            #print(nBytes)
            if nBytes[0:3] == '110':
                suffix += file.read(1)
            elif nBytes[0:4] == '1110':
                suffix += file.read(2)
            elif nBytes[0:5] == '1110':
                suffix += file.read(3)
            suffix = suffix.decode("utf8")
            #print(prefix, suffix)
            dictionary[int(index)] = [int(prefix), suffix]
            #print(dictionary)
            index += 1
            while prefix != 0:
                #print(dictionary[int(prefix)])
                suffix += dictionary[int(prefix)][1]
                prefix = dictionary[int(prefix)][0]
                
            suffix = suffix[::-1]
            decompText += suffix
            
            
        decompText = decompText[:-1]
        return decompText
            

                
    def printTree(self, currentNode):
        print(currentNode.value, currentNode.prefix, len(currentNode.filhos))
        for x in currentNode.filhos:
            print(x.value, "E filho de", currentNode.value)
            self.printTree(x)
        return

def main():
    
    print(len(sys.argv))
    print(sys.argv)
    T = TrieTree()
    if len(sys.argv) < 3:
        print("Not enough arguments were given")
        return
    elif len(sys.argv) > 4:
        print("Too many arguments were given")
        return
    if sys.argv[1] == '-c':
        inFile = open(sys.argv[2], "r", encoding="utf8")
        #outFile = open("out.z78", "w")
        text = inFile.read()
        text += '$'
        if len(sys.argv) == 4:
            outFile = open(sys.argv[3], "wb")
        else: #Means len(sys.argv) = 3
            aux = (sys.argv[2]).split('.')[0]
            aux += '.z78'
            outFile = open(aux, "wb")
        with outFile as file:
            T.compress(text, file)
        return
    elif sys.argv[1] =='-x':
        if len(sys.argv) == 4:
            outFile = open(sys.argv[3], "w")
        else: #Means len(sys.argv) = 3
            aux = (sys.argv[2]).split('.')[0]
            aux += '.txt'
            outFile = open(aux, "w")
        with open(sys.argv[2], "rb") as file:
            outFile.write(T.decompress(file))
        return
    else:
        print("The second argument you input is not an accepted one. Please use -c or -x.")
        return
    
    '''
    inFile = open("dom_casmurro.txt", "r", encoding="utf8")
    #outFile = open("out.z78", "w")
    T = TrieTree()
    text = inFile.read()
    text += '$'
    with open("out.z78", "wb") as file:
        T.compress(text, file)
        
        
    outFile = open("out.txt", "w")
    with open("out.z78", "rb") as file:
        outFile.write(T.decompress(file))
    
    #T.printTree(T.root)
    print(T.num)
    inFile.close()
    #outFile.close()
    '''
    
if __name__ == '__main__':
    main()
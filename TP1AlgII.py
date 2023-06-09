import sys

class TreeNode:
    def __init__(self, value = 0, prefix = '', sons = []):
        self.value = value
        self.prefix = prefix
        self.sons = sons

class TrieTree:
    def __init__(self):
        self.root = TreeNode(0, '', [])
        self.num = 1
        
    def countNum(self, s, file):
        currentNode = self.root
        for x in s:
            wasFound = False
            for y in currentNode.sons:
                if x == y.prefix:
                    currentNode = y
                    wasFound = True
                    break
            if wasFound == False:
                newNode = TreeNode(self.num, x, [])
                self.num += 1
                currentNode.sons.append(newNode)
                currentNode = self.root
        numBPI = (self.num.bit_length() + 7) // 8
        if numBPI > 100:
            print("The text has too many prefixes, and I am honestly impressed by it.")
            print("Like, there are more than 5 quintillions of them.")
            print("I do hope this never needs to get to be printed, and the code will not work as expected.")
        file.write(numBPI.to_bytes(1, byteorder='big', signed=False))
        return int(numBPI)
        
    def compress(self, s, file, numBPI):
        self.num = 1
        currentNode = self.root
        for i in range(0,len(s)):
            wasFound = False
            #print(currentNode.prefix)
            for y in currentNode.sons:
                if s[i] == y.prefix:
                    currentNode = y
                    wasFound = True
                    if i == len(s)-1:
                        file.write((y.value).to_bytes(numBPI, byteorder='big', signed=False))
                        file.write(s[i].encode('utf8', 'strict'))
                    break
            if wasFound == False:
                newNode = TreeNode(self.num, s[i], [])
                self.num += 1
                currentNode.sons.append(newNode)
                k = currentNode.value
                file.write(k.to_bytes(numBPI, byteorder='big', signed=False))
                file.write(s[i].encode('utf8', 'strict'))
                currentNode = self.root
                
    def decompress(self, file):
        dictionary = {}
        dictionary[0] = [0, '']
        numBPI = int.from_bytes(file.read(1), 'big') #Number of bytes per int
        index = 1;
        decompText = ""
        while True:
            prefix = file.read(numBPI)
            prefix = int.from_bytes(prefix, "big")
            suffix = file.read(1)
            if prefix == b'' or suffix == b'':
                break
            nBytes = ord(suffix)
            nBytes = bin(nBytes)[2:].rjust(8, '0')
            if nBytes[0:3] == '110':
                suffix += file.read(1)
            elif nBytes[0:4] == '1110':
                suffix += file.read(2)
            elif nBytes[0:5] == '11110':
                suffix += file.read(3)
            suffix = suffix.decode("utf8")
            dictionary[int(index)] = [int(prefix), suffix]
            index += 1
            while prefix != 0:
                suffix += dictionary[int(prefix)][1]
                prefix = dictionary[int(prefix)][0]
                
            suffix = suffix[::-1]
            decompText += suffix
            
        return decompText
            
                
    def printTree(self, currentNode):
        print(currentNode.value, currentNode.prefix, len(currentNode.sons))
        for x in currentNode.sons:
            print(x.value, "is son of ", currentNode.value)
            self.printTree(x)
        return

def main():
    T = TrieTree()
    if len(sys.argv) < 3:
        print("Not enough arguments were given")
        return
    elif len(sys.argv) == 4:
        print("Sorry, the input is not in an accepted format.")
        return
    elif len(sys.argv) > 5:
        print("Too many arguments were given")
        return
    if sys.argv[1] == '-c':
        inFile = open(sys.argv[2], "r", encoding="utf8")
        text = inFile.read()
        if len(sys.argv) == 5:
            outFile = open(sys.argv[4], "wb")
        else: #Means len(sys.argv) == 3
            aux = (sys.argv[2]).split('.')[0]
            aux += '.z78'
            outFile = open(aux, "wb")
        helperTrie = TrieTree()
        BPI = helperTrie.countNum(text, outFile)
        T.compress(text, outFile, BPI)
        return
    elif sys.argv[1] =='-x':
        if len(sys.argv) == 5:
            outFile = open(sys.argv[4], "w")
        else: #Means len(sys.argv) == 3
            aux = (sys.argv[2]).split('.')[0]
            aux += '.txt'
            outFile = open(aux, "w")
        with open(sys.argv[2], "rb") as file:
            outFile.write(T.decompress(file))
        return
    else:
        print("The second argument you input is not an accepted one. Please use -c or -x.")
        return
    
    
if __name__ == '__main__':
    main()
    

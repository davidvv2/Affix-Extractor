class TrieNode:
    def __init__(self, myCharName):
        self.endToken = False  # True only when the node represents the end of the word
        self.ChildNodes = []  # This is a list of children nodes that this node has
        self.char = myCharName  # Setting the name character of this node
        self.count = 1  # used to count to calculate the transitional probability

    def getChildNodes(self):
        return self.ChildNodes

    def getNodeChar(self):
        # This method simply returns its name character
        return self.char

    def getChildNode(self, childChar):
        # Search through the list of ChildNodes
        # until you find the node with the character 'childChar'
        # and then return that childNode
        # But if you don't find it, return None
        for child in self.ChildNodes:
            if child.char == childChar:
                return child
        return None

    def addEntry(self, substring, count=1):
        # If you reached the end of the substring
        # set the end token to True, and finally return True.
        if substring == "":
            # print("I am " + self.char + " and I have nothing to add")
            self.endToken = True
            return True
        # Take the first character of the substring
        firstchar = substring[0]
        # check whether this character already exists as a childNode
        currChildNode = self.getChildNode(firstchar)
        # if NOT, then create a new node, name it for that character,
        if currChildNode == None:
            currChildNode = TrieNode(firstchar)
            currChildNode.count = count
            # and store the new node as one of the childNodes
            self.ChildNodes.append(currChildNode)
        # Once the child node is identified, pass on the remainder of the substring
        # to the child node so that it continues to process it
        else:
            currChildNode.count += count
        restofword = substring[1:]
        return currChildNode.addEntry(restofword, count)

    def hasWord(self, substring):
        # create it
        if substring == "":
            return False
        firstchar = substring[0]
        currChildNode = self.getChildNode(firstchar)
        if currChildNode is not None:
            restofword = substring[1:]
            if restofword == "" and currChildNode.endToken is True:
                return True
            if currChildNode.hasWord(restofword) is True:
                return True
        return False


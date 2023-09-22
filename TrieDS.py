import TrieNode


class TrieDS:
    def __init__(self):
        self.RootNode = TrieNode.TrieNode('')

    def addWord(self, word, count=1):
        return self.RootNode.addEntry(word, count)

    def hasWord(self, word):
        return self.RootNode.hasWord(word)

    # calculates transitional probability from parent to child
    def calculateProbability(self, X, Y):
        pstring = list(X)
        pnode = self.RootNode
        for char in pstring:
            pnode = pnode.getChildNode(char)
        childnode = pnode.getChildNode(Y)
        return childnode.count / pnode.count

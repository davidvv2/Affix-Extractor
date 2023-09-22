import TrieDS as tds

if __name__ == '__main__':
    corpus = {}
    word_count = 0
    suffix = {}
    prefix = {}

    # opens file
    file = open("Output/dictionary.txt", "rt", encoding='utf8')
    lines = file.readlines()

    # Builds corpus from file
    # example of a line from file ("tajjeb   234")
    for line in lines:
        word = line.split('\t')[0].strip()
        value = line.split('\t')[1].strip()
        corpus[word] = int(value)
        word_count = int(value)

    goodwords = corpus.keys()

    MyReverseTrie = tds.TrieDS()
    MyTrie = tds.TrieDS()

    for word in goodwords:
        MyTrie.addWord(word, corpus[word])
        rword = word[::-1]
        MyReverseTrie.addWord(rword, corpus[word])

    suffixs = []
    prefixs = []
    for word in goodwords:
        beta = list(word)  # used to search for suffixes
        rbeta = list(word[::-1])  # used to search for prefixes
        # initialise a,b,alpha ra,rb,ralpha by popping from lists beta and rbeta
        if len(beta) >= 3:
            alpha = ""
            a = beta.pop(0)
            b = beta.pop(0)

            ralpha = ""
            ra = rbeta.pop(0)
            rb = rbeta.pop(0)
        if len(beta) == 2:
            alpha = ""
            a = ""
            b = beta.pop(0)

            ralpha = ""
            ra = ""
            rb = rbeta.pop(0)
        if len(beta) == 1:
            continue
        while rbeta:
            pre = rb + ''.join(rbeta)
            if pre not in prefixs:
                prefix[pre] = 0
                prefixs = prefix.keys()
            if MyReverseTrie.hasWord(ralpha + ra):
                if int(MyReverseTrie.calculateProbability(ralpha, ra)) == 1:
                    if MyReverseTrie.calculateProbability(ralpha + ra, rb) < 1:
                        prefix[pre] += 19
                        ralpha += ra
                        ra = rb
                        rb = rbeta.pop(0)
                        continue
            prefix[pre] -= 1
            ralpha += ra
            ra = rb
            rb = rbeta.pop(0)

        while beta:
            suf = b + ''.join(beta)
            if suf not in suffixs:
                suffix[suf] = 0
                suffixs = suffix.keys()
            if MyTrie.hasWord(alpha + a):
                if int(MyTrie.calculateProbability(alpha, a)) == 1:
                    if MyTrie.calculateProbability(alpha + a, b) < 1:
                        suffix[suf] += 19
                        alpha += a
                        a = b
                        b = beta.pop(0)
                        continue
            suffix[suf] -= 1

            alpha += a
            a = b
            b = beta.pop(0)

            if not beta:
                suf = b
                if suf not in suffixs:
                    suffix[suf] = 0
                    suffixs = suffix.keys()
                if MyTrie.hasWord(alpha + a):
                    if int(MyTrie.calculateProbability(alpha, a)) == 1:
                        if MyTrie.calculateProbability(alpha + a, b) < 1:
                            suffix[suf] += 19
                suffix[suf] -= 1

    # prunes suffix list
    for key in list(suffixs):
        # split suffix
        beginning = key[0]
        rest = key[1:]

        while rest:
            try:
                if beginning in suffix.keys() and rest in suffix.keys():
                    # if a morpheme is composed of two other morpheme compare the scores of the morphemes if the longer
                    # morpheme has a lower score then remove from list
                    if suffix[beginning] > suffix[key] or suffix[rest] > suffix[key]:
                        del suffix[key]
                    # if the other way around  then remove the two smaller morphemes
                    else:
                        del suffix[beginning]
                        del suffix[rest]

                elif beginning in suffix.keys():
                    if suffix[beginning] > suffix[key]:
                        del suffix[key]
                    else:
                        del suffix[beginning]
                elif rest in suffix.keys():
                    if suffix[rest] > suffix[key]:
                        del suffix[key]
                    else:
                        del suffix[rest]
            except:
                pass
            beginning += rest[0]
            rest = rest[1:]

    file = open("Output/suffixes.txt", "w", encoding='utf8')
    for key in suffix.keys():
        if suffix[key] > 19:
            file.write(key + "\tscore: " + str(suffix[key]) + "\n")
    file.close()
    print("Finished saving suffixes to file...")

    for key in list(prefixs):
        beginning = key[0]
        rest = key[1:]

        while rest:
            try:
                if beginning in prefix.keys() and rest in prefix.keys():
                    if prefix[beginning] > prefix[key] or prefix[rest] > prefix[key]:
                        del prefix[key]
                    else:
                        del prefix[beginning]
                        del prefix[rest]
                elif beginning in prefix.keys():
                    if prefix[beginning] > prefix[key]:
                        del prefix[key]
                    else:
                        del prefix[beginning]
                elif rest in prefix.keys():
                    if prefix[rest] > prefix[key]:
                        del prefix[key]
                    else:
                        del prefix[rest]
            except:
                pass
            beginning += rest[0]
            rest = rest[1:]

    file = open("Output/prefixes.txt", "w", encoding='utf8')
    for key in prefix.keys():
        if prefix[key] > 0:
            file.write(key[::-1] + "\tscore: " + str(prefix[key]) + "\n")
    file.close()
    print("Finished saving prefixes to file...")
    print("Finished!")

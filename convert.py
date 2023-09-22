import glob


class Convert:
    def convert(self):
        path = "./Corpus"
        unique_words = []
        dictionary = {}

        text_files = glob.glob(path+"/*.txt")
        if len(text_files) == 0:
            print("ERROR NO CORPUS FOUND!!!\nEXITING...")
            return
        print("loading corpus")
        for file in text_files:
            for line in open(file, 'rt', encoding='utf8'):
                list = line.split('\t')
                # if line is not in the standard corpus format then skip
                if len(list) != 4:
                    continue
                word = list[0].lower()
                tag = list[1].lower()
                stem = list[2].lower()

                # only considers verbs that have a stem associated with them
                if 'verb' not in tag:
                    continue
                if stem == "null":
                    continue

                # add word
                if word in unique_words:
                    dictionary[word] += 1
                elif word not in unique_words:
                    unique_words.append(word)
                    dictionary[word] = 1
                # add stem to dict
                if stem in unique_words:
                    dictionary[word] += 1
                else:
                    unique_words.append(stem)
                    dictionary[stem] = 1
        print("Finished loading Corpus")
        file = open("Output/dictionary.txt", "w", encoding='utf8')
        print("Saving corpus")
        for key in dictionary.keys():
            if dictionary[key] > 50:
                file.write(key + "\t" + str(dictionary[key]) + "\n")
        file.close()
        print("Finished saving corpus")


if __name__ == '__main__':
    con = Convert()
    con.convert()

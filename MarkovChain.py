import os, re, random, sys


# Removing stop words from the string
def remove_stopwords(l):
    stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself',
                 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself',
                 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that',
                 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'now',
                 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as',
                 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through',
                 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off',
                 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how',
                 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not',
                 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should']
    return [w for w in l if w not in stopwords]


# Cleaning the string by removal of punctuations and other characters
def clean(s):
    return " ".join(re.findall(r'\w+', s, flags=re.UNICODE)).lower()


# Generating grams for the string 
def generate_ngram(bits, ngram):
    grams = {}
    for i in range(1, ngram + 1):
        words = []
        count = 0
        main_count = 0
        for w in range(len(bits)-i):
            main_count += 1
            new_w = ''
            g = w
            for x in range(i):
                new_w = new_w + ' ' + bits[g]
                g += 1
            words.append(new_w.strip())
            count += 1
        grams[i] = words
    return grams


# Obtaining processed grams
def prob_ngram(data, grams):
    count = 0
    start = 0
    end = len(data)-1
    for line in data:
        if "START OF THIS PROJECT" in line:
            start = count
        if "END OF THIS PROJECT" in line:
            end = count
        count += 1
    arr = ''.join(data[start:end]).replace("_", "")
    string = clean(arr)
    bits = string.split()
    bits = remove_stopwords(bits)
    return generate_ngram(bits, grams)


# Determining uni bi and trigrams
def generate_ngram_probablity(ngram_probs):
    unigrams, bigrams, trigrams = {}, {}, {}
    length = len(ngram_probs[1])
    for u in ngram_probs[1]:
        if u in unigrams.keys():
            unigrams[u] += 1/length
        else:
            unigrams[u] = 1/length

    for b in ngram_probs[2]:
        temp = b.split()
        if temp[0] in bigrams.keys():
            if temp[1] in bigrams[temp[0]].keys():
                bigrams[temp[0]][temp[1]] += 1/(unigrams[temp[0]]*length)
            else:
                bigrams[temp[0]][temp[1]] = 1/(unigrams[temp[0]]*length)
        else:
            bigrams[temp[0]] = {}
            bigrams[temp[0]][temp[1]] = 1/(unigrams[temp[0]]*length)


    for t in ngram_probs[3]:
        temp = t.split()
        x, y = temp[0], temp[1]
        temp[0:2] = [' '.join(temp[0:2])]
        if temp[0] in trigrams.keys():
            if temp[1] in trigrams[temp[0]].keys():
                trigrams[temp[0]][temp[1]] += 1/(bigrams[x][y]*unigrams[x]*length)
            else:
                trigrams[temp[0]][temp[1]] = 1/(bigrams[x][y]*unigrams[x]*length)
        else:
            trigrams[temp[0]] = {}
            trigrams[temp[0]][temp[1]] = 1/(bigrams[x][y]*unigrams[x]*length)
    return [unigrams, bigrams, trigrams]


# Generating sentences from the determined model
def generate_sentence(gram_probs, result):
    r = open(result, "a+")
    for _ in range(10):
        first = random.choice(list(gram_probs[0]))
        second = random.choice(list(gram_probs[1][first]))
        sentence_prob = gram_probs[0][first] * gram_probs[1][first][second]
        temp_sentence = first + " " + second
        for _ in range(18):
            new_pair = first + " " + second
            pred_word = random.choice(list(gram_probs[2][new_pair]))
            first = second
            second = pred_word
            sentence_prob *= gram_probs[2][new_pair][pred_word]
            temp_sentence += " " + pred_word
        r.write(temp_sentence + ", Probability: " + str(sentence_prob) + "\n")


# Generating sentences for multiple authors
def generate_sentence_pair(gram_probs1, gram_probs2, result):
    r = open(result, "a+")
    r.write("Below are the generated 10 sentences for each author along with their probabilities \n")
    r.write("Prob1 is the determined probability for author1 and Prob2 is the determined probability for author2 \n")
    for count, gram_probs in enumerate([gram_probs1, gram_probs2]):
        r.write("\n\nSentences generated for author " + str(count+1)+ "\n")
        for _ in range(10):
            first = random.choice(list(gram_probs[0]))
            second = random.choice(list(gram_probs[1][first]))
            try: sentence_prob1 = gram_probs1[0][first] * gram_probs1[1][first][second]
            except: sentence_prob1 = 1e-4
            try: sentence_prob2 = gram_probs2[0][first] * gram_probs2[1][first][second]
            except: sentence_prob2 = 1e-4
            temp_sentence = first + " " + second
            for _ in range(18):
                new_pair = first + " " + second
                pred_word = random.choice(list(gram_probs[2][new_pair]))
                first = second
                second = pred_word
                try: sentence_prob1 *= gram_probs1[2][new_pair][pred_word]
                except: sentence_prob1 *= 1e-4
                try: sentence_prob2 *= gram_probs2[2][new_pair][pred_word]
                except: sentence_prob2 *= 1e-4
                temp_sentence += " " + pred_word
            r.write(temp_sentence + ", Prob1: " + str(sentence_prob1) + ", Prob2: " + str(sentence_prob2) + "\n")


# Writing probablities to file
def get_prob_file(probs, prob_file):
    p = open(prob_file, "a+")
    p.write("String and its respective probabilitites are given below\n")
    for gram in probs:
        for key, value in gram.items():
            try:
                for k, v in value.items():
                    p.write(key + " " + k + "\t" + str(v) + "\n")
            except:
                p.write(key + "\t" + str(value) + "\n")


# Gathering book data
def get_book_data(books1, auth1):
    cur_directory = os.getcwd()
    data = ''
    for book in books1:
        loc = cur_directory +"\\" + auth1 + "\\" + book
        data = data + str(open(loc, "r", encoding="utf-8").read().split("\n"))
    return data


def main():
    try:
        auth1, auth2, prob1, prob2, result = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
    except:
        auth1, auth2, prob1, prob2, result = sys.argv[1], '', sys.argv[2], '', sys.argv[3]

    try: os.remove(prob2)
    except: pass
    try: os.remove(prob1)
    except: pass
    try: os.remove(result)
    except: pass

    books1 = os.listdir(auth1)
    books2 = [] if not auth2 else os.listdir(auth2)
    data1 = get_book_data(books1, auth1)
    data2 = '' if not books2 else get_book_data(books2, auth2)
    ngram_probs1 = prob_ngram(data1, 3)
    ngram_probs2 = [] if not data1 else prob_ngram(data2, 3)
    gram_probs1 = generate_ngram_probablity(ngram_probs1)
    gram_probs2 = [] if not ngram_probs2 else generate_ngram_probablity(ngram_probs2)

    get_prob_file(gram_probs1, prob1)
    if prob2:
        get_prob_file(gram_probs2, prob2)
        generate_sentence_pair(gram_probs1, gram_probs2, result)
    else:
        generate_sentence(gram_probs1, result)


if __name__ == '__main__':
    main()

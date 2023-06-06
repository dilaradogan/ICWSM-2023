import re
import csv
import sys
import random
import math
import os
import gensim
model = gensim.models.KeyedVectors.load_word2vec_format('C:\\Users\\PycharmProjects\\fasttext\\wiki-news-300d-1M.vec')
index = 0
addTime = 1
keyword_list = ['atheism', 'climate', 'feminism', 'clinton', 'abortion']
keyWord = keyword_list[0]
pos_list = []
tasks = ['AT', 'CC', 'FM', 'HC', 'LA']
for index in range(0, 5):
    for addTime in range(1, 5):
        for keyWordIndex in range(0, 5):
            keyWord = keyword_list[keyWordIndex]
            with open('C:\\Users\\PycharmProjects\\fasttext\\mutated_tweets\\shuffle_word\\'+tasks[index]+'\\'+str(addTime)+'_test_preprocessed.csv', mode='w', newline='') as csv_file:
                fieldnames = ['Tweet', 'Stance', 'Index', 'Original Tweet']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                with open('C:\\Users\\PycharmProjects\\fasttext\\mutated_tweets\\shuffle_word\\'+tasks[index]+'\\test_preprocessed.csv') as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=',')
                    line_count = 0
                    for row in csv_reader:
                        if line_count == 0:
                            #print(f'Column names are {", ".join(row)}')
                            writer.writeheader()
                            line_count += 1
                        else:
                            #print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
                            newTweet = row[0] #+ "#free"
                            #print(pos_list)
                            #size_list = len(pos_list)
                            char_index = 0
                            k = 0
                            word_list = newTweet.split()  #
                            hashtag_var = re.findall(r'#', newTweet)
                            p_list = []
                            kare_start = 0
                            for i in range(0, len(word_list)):
                                if (word_list[i] == '#'):
                                    if (kare_start == 0):
                                        kare_start = 1
                                    else:
                                        kare_start = 0
                                elif (kare_start == 0 and word_list[i] != ' ' and len(word_list[i])>3):
                                    p_list.append(i)

                            ran_list = []
                            kw = 0
                            mydict = {}
                            for w in p_list:
                                if (word_list[w] in model.vocab):
                                    mydict[w] = 1 - model.similarity(keyWord, word_list[w])
                                else:
                                    mydict[w] = 1.0
                                print(word_list[w] + ": " + str(mydict[w]) + "\n")
                                kw = kw + 1
                            sorted_x = sorted(mydict.items(), key=lambda kv: kv[1])
                            print(sorted_x)
                            for i in sorted_x:
                                if (k < addTime):
                                    orijinalWord = word_list[i[0]]
                                    if(len(word_list[i[0]]) == 4):
                                        word = word_list[i[0]][1:len(word_list[i[0]]) - 1]
                                        # print(word)
                                        shuffled = ''.join(random.sample(word, len(word)))
                                        # print(shuffled)
                                        word_list[i[0]] = word_list[i[0]][0] + shuffled + word_list[i[0]][len(word_list[i[0]]) - 1:]
                                        # print(word_list[r])
                                        if(orijinalWord != word_list[i[0]]):
                                            k = k + 1
                                    elif(len(word_list[i[0]]) > 4):
                                        word = word_list[i[0]][1:4]
                                        # print(word)
                                        shuffled = ''.join(random.sample(word, len(word)))
                                        # print(shuffled)
                                        word_list[i[0]] = word_list[i[0]][0] + shuffled + word_list[i[0]][4:]
                                        # print(word_list[r])
                                        if (orijinalWord != word_list[i[0]]):
                                            k = k + 1
                                else:
                                    break
                            # newTweet = newTweet.replace(' ', '', removeTime)
                            # print(newTweet+"\n")
                            newTweet = ' '.join([str(elem) for elem in word_list])
                            line_count += 1
                            writer.writerow({'Tweet': newTweet, 'Stance': row[1], 'Index': row[2], 'Original Tweet': row[3]})

                    print(f'Processed {line_count} lines.')
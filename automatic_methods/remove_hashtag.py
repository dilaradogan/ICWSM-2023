import re


# function to print all the hashtags in a text
def extract_hashtags(text):
    # the regular expression
    regex = "(# [a-zA-Z0-9 ]* #$)"#"#( \w+)" # "(# \w+ #$)"

    # extracting the hashtags
    hashtag_list = re.findall(regex, text)
    text2 = re.sub(' '+regex, '',text)
    print(text2)
    # printing the hashtag_list
    print("The hashtags in \"" + text + "\" are :")
    for hashtag in hashtag_list:
        print(hashtag)
    return text2#len(hashtag_list)
import csv
import sys
import os
index = int(sys.argv[1])
times = int(sys.argv[2])
hashtag_index = index*4
n = "remove_hashtag"
tasks = ['AT', 'CC', 'FM', 'HC', 'LA']
hashtag_list = ['#peace', '#free', '#life', '#thoughts', '#world','#weather','#life','#morning','#human','#life','#world','#thoughts', '#usa','#decision','#time','#future', '#freedom','#in','#my','#opinion' ]
with open('C:\\Users\\mutated_tweets\\remove_hashtag\\'+tasks[index]+'\\'+str(times)+'_test_preprocessed.csv', mode='w', newline='') as csv_file:
    fieldnames = ['Tweet', 'Stance', 'Index', 'Original Tweet']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    with open('C:\\Users\\mutated_tweets\\remove_hashtag\\'+tasks[index]+'\\test_preprocessed.csv') as csv_file:
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
                k= 0
                while k < times:
                    newTweet = extract_hashtags(newTweet)
                    k = k + 1
                #print(newTweet+"\n")
                line_count += 1
                writer.writerow({'Tweet': newTweet, 'Stance': row[1], 'Index': row[2], 'Original Tweet': row[3]})

        print(f'Processed {line_count} lines.')
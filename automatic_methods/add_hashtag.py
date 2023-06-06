import csv
import sys
import os
index = int(sys.argv[1])
hashtag_index = index*4
n = int(sys.argv[2])+1
tasks = ['AT', 'CC', 'FM', 'HC', 'LA']
hashtag_list = ['#peace', '#free', '#life', '#thoughts', '#world', '#weather', '#life', '#morning', '#human', '#life', '#world', '#thoughts', '#usa', '#decision', '#time', '#future', '#MondayMotivation', '#goals', '#opinion', '#thoughts']
with open('C:\\Users\\methods\\Preprocessing\\Data_SemE_P\\mutated_tweets\\add_hashtag\\'+tasks[index]+'\\'+str(n-1) +'_test_preprocessed.csv', mode='w', newline='') as csv_file:
    fieldnames = ['Tweet', 'Stance', 'Index', 'Original Tweet']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    with open('C:\\Users\\methods\\Preprocessing\\Data_SemE_P\\mutated_tweets\\add_hashtag\\'+tasks[index]+'\\test_preprocessed.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                writer.writeheader()
                line_count += 1
            else:
                #print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
                newTweet = row[0] #+ "#free"
                for i in range(hashtag_index, hashtag_index+n-1):
                    newTweet = newTweet + " " + hashtag_list[i]
                print(newTweet+"\n")
                line_count += 1
                writer.writerow({'Tweet': newTweet, 'Stance': row[1], 'Index': row[2], 'Original Tweet': row[3]})

        print(f'Processed {line_count} lines.')
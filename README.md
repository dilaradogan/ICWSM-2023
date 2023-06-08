# Catch Me If You Can: Deceiving Stance Detection and Geotagging Models to Protect Privacy of Individuals on Twitter

In this work, we investigate what individuals can do to avoid being detected by NLP models while using social media platforms. We ground our investigation in two exposure-risky tasks, stance detection and geotagging. We explore a variety of simple techniques for modifying text, such as inserting typos in salient words, paraphrasing, and adding dummy social media posts.


## Contents related to the stance detection system

The contents of the directories under the repo are summarized below.

- It contains the codes that enable the 7 methods we use to change the automatic data under "automatic_methods" to be applied on the test data.

- "automatic_mutated_data" contains the data obtained from the results of 7 methods under automatic_methods.
- "manual_mutated_data", on the other hand, contains test data that has been modified by the data manipulation methods that we define as manual methods by the user. The test files were created in such a way as to express "the subject_which user" made changes.

- "original_data" contains data separated by subject of training and test sets on which no text modification has been performed.

- "st_qualitative_experimental_results.py" is the system code that provides the results of the test data we have created with various manual and automatic methods.

## Contents related to the geotagging system

- For the geotagging task, we have used the implementation of GCN and MLP-TXT+NET10 shared by Rahimi, Cohn, and Baldwin (2018)

  
https://github.com/afshinrahimi/geographconv

- The data we use for the geotagging task, including train, dev and test, are given under the "geolocation_data" directory.

- The methods used in automatic text change in the Stance detection task are also used in the geotagging task.

## Citation

  
    @article{
      title={Catch Me If You Can: Deceiving Stance Detection and Geotagging Models to Protect Privacy of Individuals on Twitter’ Social Behaviors},
      author={Dilara Dogan, Bahadir Altun, Muhammed Said Zengin, Mucahid Kutlu, Tamer Elsayed},
      booktitle={Proceedings of the International AAAI Conference on Web and Social Media},
      year={2023}
    }
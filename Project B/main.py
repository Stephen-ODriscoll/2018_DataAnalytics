import re
import time
from math import log
import numpy as np
import matplotlib.pyplot as plt


'''     Author:           Stephen O'Driscoll
        Student Number:   R00146853             '''


def main():
    start_time = time.time()

    # Read in positive and negative training files and make them lower case
    doc_train_pos = read("train/trainPos.txt")
    doc_train_neg = read("train/trainNeg.txt")

    # Returns a dictionary with unique words as keys and their frequencies as values, also returns total words processed
    dict_count_pos, total_count_pos = process(doc_train_pos)
    dict_count_neg, total_count_neg = process(doc_train_neg)

    # Create a list of all unique words used in either positive or negative or both
    vocab_complete = set()
    vocab_complete.update(dict_count_pos.keys(), dict_count_neg.keys())

    # Use Naive Classification to calculate probability of each word being positive or negative
    dict_prob_pos = calculate(dict_count_pos, total_count_pos, vocab_complete)
    dict_prob_neg = calculate(dict_count_neg, total_count_neg, vocab_complete)

    # Display the number of positive and negative words as well as how long it took to get this far
    display_counts(total_count_pos, total_count_neg, start_time)

    print()     # Blank line

    # Calculate and display the accuracy for positive and negative training files
    accuracy_train_pos = analyse("Positive Training Analysis", doc_train_pos, dict_prob_pos, dict_prob_neg)
    accuracy_train_neg = analyse("Negative Training Analysis", doc_train_neg, dict_prob_pos, dict_prob_neg)

    print()     # Blank line

    # Calculate and display the accuracy for positive and negative testing files
    accuracy_test_pos = analyse("Positive Testing Analysis", read("test/testPos.txt"), dict_prob_pos, dict_prob_neg)
    accuracy_test_neg = analyse("Negative Testing Analysis", read("test/testNeg.txt"), dict_prob_pos, dict_prob_neg)

    # Create bar chart based on results of every accuracy test and print total time program has taken
    visualize(accuracy_train_pos, accuracy_train_neg, accuracy_test_pos, accuracy_test_neg)
    print("\nTotal time taken: " + str(time.time() - start_time))
    exit(0)


# Analyse each document and return final accuracy
def analyse(title, document, dict_prob_pos, dict_prob_neg):

    start_time = time.time()
    count_pos, count_neg = classify(document, dict_prob_pos, dict_prob_neg)
    return display(title, count_pos, count_neg, start_time)


# Reads files and makes all letters lower case
def read(directory):
    return open(directory).read().lower()


# Returns a string with special characters removed. Ignores letters and numbers
def clean(to_clean):
    return re.sub(r'[^\w]', ' ', to_clean)


# returns a dictionary of unique words and their frequencies in a given document - Multinomial Model
def process(document):

    words = clean(document).split()         # Clean
    vocab = set(words)
    dictionary = dict.fromkeys(vocab, 0)    # put all unique words in dictionary with 0 as value
    total = 0

    # If a words length is 2 or less ignore. I experimented and found this was the best way to remove meaningless words
    # It has consistently given me the highest accuracy at a good speed
    for word in words:
        if len(word) > 2:
            count = dictionary.get(word)
            dictionary[word] = count + 1        # Get unique word and increment frequency at every occurrence
            total += 1

    # Send back processed words with total words checked
    return dictionary, total


# Uses Naive Bayes Multinomial Text Classification to calculate probability each word is positive/negative
def calculate(dictionary, total_count, vocab):
    result = {}

    # (count(w,c) + 1) / (count(c) + |V|)
    for word in vocab:
        if word not in dictionary:
            result[word] = 1 / (total_count + len(vocab))

        else:
            result[word] = (dictionary[word] + 1) / (total_count + len(vocab))

    return result


# Decides whether a tweet is positive or negative based on it's algorithm
def classify(document, dict_prob_pos, dict_prob_neg):

    # Number of positive and negative tweets to be incremented when a decision is made
    count_pos = 0
    count_neg = 0
    tweets = document.split("\n")       # Split document into tweets

    # Iterate through each tweet
    for tweet in tweets:

        prob_pos = 1
        prob_neg = 1
        words = clean(tweet).split()    # Clean out special characters

        # Same as before, I experimented and found this worked best at cleaning out meaningless words
        for word in words:
            if len(word) > 2:

                # If word exists is positive or negative assign probability using log
                if word in dict_prob_pos:
                    word_prob_pos = dict_prob_pos[word]
                    prob_pos += log(word_prob_pos)

                if word in dict_prob_neg:
                    word_prob_neg = dict_prob_neg[word]
                    prob_neg += log(word_prob_neg)

        # If final positive score is greater than negative increment positive
        if prob_pos > prob_neg:
            count_pos += 1

        # Check the opposite as well. It is very unlikely but a tweet can be neutral if scores are the same
        # I have checked and this never occurs with the given files but I left the check in anyway
        elif prob_pos < prob_neg:
            count_neg += 1

    return count_pos, count_neg


# Simply display data
def display(title, count_pos, count_neg, start_time):

    total = count_pos + count_neg
    percent_pos = count_pos / total * 100
    percent_neg = count_neg / total * 100
    accuracy = 0.0

    print(title + ":")

    # If title starts with word Positive we know to display positive accuracy
    if title.startswith('P'):
        print("\tPositive Accuracy:" + str(percent_pos) + "%")
        accuracy = percent_pos

    # Else we display negative accuracy
    elif title.startswith('N'):
        print("\tNegative Accuracy:" + str(percent_neg) + "%")
        accuracy = percent_neg

    # Display the time it took for this portion of the file
    print("\tTime Taken: " + str(time.time() - start_time) + " seconds")
    return accuracy


# Display counts for positive and negative words and setup time
def display_counts(count_pos, count_neg, start_time):

    print("\nPositive Count: " + str(count_pos))
    print("Negative Count: " + str(count_neg))
    print("Time Taken to Read, Process and Calculate: " + str(time.time() - start_time) + " seconds")


# Display bar chart visualization
def visualize(accuracy_train_pos, accuracy_train_neg, accuracy_test_pos, accuracy_test_neg):

    data = ('Train Positive', 'Train Negative',
            'Test Positive', 'Test Negative')

    plot = [accuracy_train_pos, accuracy_train_neg,
            accuracy_test_pos, accuracy_test_neg]
    y_pos = np.arange(len(data))
    plt.bar(y_pos, plot, align='center', alpha=0.1)
    plt.xticks(y_pos, data)
    plt.ylabel("Percentage")
    plt.xlabel("Data")
    plt.title("Program Accuracy")
    plt.show()


main()      # Call main, start program

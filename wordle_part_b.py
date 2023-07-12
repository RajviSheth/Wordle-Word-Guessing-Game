import re
import pandas as pd
import random


def read_file(file_name):
    """
    Reading the input file and fetching and storing it in a dataframe called 'raw_data'

    :param file_name: The name of the input file
    :return: raw_data
    """
    raw_data = pd.read_csv(file_name, header=None)
    return raw_data


class Node:
    # Constructor For the Node class that initializes the attributes of the Node Class
    def __init__(self, data, target, depth=0, max_depth=10):
        self.data = data
        self.target = target
        self.depth = depth
        self.max_depth = max_depth
        self.left = None
        self.right = None
        self.threshold = None
        self.attribute = None
        self.label = None

        self.split()


def calc_prob(raw_data):
    """
    This method calculates the probabilities for each alphabet
    :param raw_data: the data frame of the file read
    :return: alphabet_prob, words
    """
    words = raw_data[0].tolist()
    alphabet_prob = {}

    pattern = re.compile(r'^[a-zA-Z]+$')

    for word in words:
        if type(word) != type('str'):
            words.remove(word)
        elif not pattern.match(word):
            words.remove(word)
    # calculating the frequency count for each alphabet occurring in how many words
    for word in words:
        word = word.lower()
        alpha_set = set([])
        for alphabet in word:
            if alphabet not in alpha_set:
                if alphabet in alphabet_prob:
                    alphabet_prob[alphabet] += 1
                    alpha_set.add(alphabet)
                else:
                    alphabet_prob[alphabet] = 1
                    alpha_set.add(alphabet)
    return alphabet_prob, words


def cost_function(alphabet_prob, words):
    """
    This method calculates the probabilities for each word and return the word with max probability and having
    all unique alphabets as the first guess
    :param alphabet_prob: the dictionary containing count for each alphabet
    :param words: The list of all potential words from the file
    :return: word_probability, max_indexes, first_guess_words_list, first_guessed_word
    """
    word_probability = []
    total_words = len(words)
    word_dict = {}

    for word in words:
        word = word.lower()
        alpha_set = set([])
        probability = 1

        # calculating the probability for each word based on the alphabet in that word
        for alphabet in word:
            if alphabet not in alpha_set:
                probability_of_alphabet = alphabet_prob[alphabet]/total_words
                # multiplying each alphabet probability for the entire word
                probability *= probability_of_alphabet
                alpha_set.add(alphabet)
        word_probability.append(probability)

    # sorting the values of the probabilities to get the maximum probability
    max_indexes = sorted(range(len(word_probability)), key=lambda i: word_probability[i], reverse=True)

    first_guess_words_list = []

    for value in max_indexes:
        word = words[value]
        # checking if the word has all the unique alphabets
        if len(set(word)) == len(word):
            first_guess_words_list.append(word)

    # getting the first word from the list which has all unique alphabets
    first_guessed_word = first_guess_words_list[0]

    print(f'The first word is "{first_guessed_word}" ')

    # print(f'The top 20 best first words are: {first_guess_words_list[1:21]}')

    return first_guessed_word


class DecisionTree:
    def __init__(self):
        self.root = None

    def train(self, data):
        self.root = Node(data.iloc[:, :-1], data.iloc[:, -1])
        return self.root


def convert_word_to_list(guessed_word, incorrect_letters, correct_letter_incorrect_position, correct_position_letters):
    """
    This method generates the feedback list for the word
    :param correct_position_letters:
    :param correct_letter_incorrect_position:
    :param incorrect_letters:
    :param guessed_word:
    :return:
    """
    word_list = list(guessed_word)

    # Create a list to store the feedback
    feedback_list = []

    # Loop through the word list and ask for feedback
    for i in range(len(word_list)):
        feedback = int(input("Enter the feedback for letter '{}' ? (0/1/2)".format(word_list[i])))
        feedback_list.append(feedback)

    # print("Word:", guessed_word)
    # print("Feedback:", feedback_list)

    for i in range(len(word_list)):
        # and word_list[i] not in correct_position_letters
        if feedback_list[i] == 0:
            incorrect_letters.append(word_list[i])
        elif feedback_list[i] == 1:
            correct_letter_incorrect_position.append((word_list[i], i))
        elif feedback_list[i] == 2 and (word_list[i], i) not in correct_position_letters:
            # print((word_list[i], i))
            correct_position_letters.append((word_list[i], i))

    # print("Incorrect letters:", incorrect_letters)
    # print("Incorrect positions of correct letters:", correct_letter_incorrect_position)
    # print("Correct letters with positions:", correct_position_letters)

    return feedback_list, incorrect_letters, correct_letter_incorrect_position, correct_position_letters


def new_guess(incorrect_letters, correct_letter_incorrect_position, correct_position_letters, words):
    """
    This method, finds the new guessed word based on the feedback from the previous word and this
    method is called recursively for all the guesses
    :param incorrect_letters: all the letter that have got a feedback of 0
    :param correct_letter_incorrect_position: tuples of letters and their positions where feedbback is 1
    :param correct_position_letters: tuples of letters and their positions where feedbback is 2
    :param words: list of all words
    :return: next_word
    """
    # Create a new list of candidate words
    candidates = []
    for w in words:
        # Strip any newline characters
        w = w.strip().lower()

        # Check if the word contains any letters that already got a 0 feedback, if yes, them skip that word
        if any(letter in w for letter in incorrect_letters):
            continue

        # Check if any letter at the incorrect position is at the same position in the candidate word, if yes, skip the word
        if any(idx == pos for letter, pos in correct_letter_incorrect_position for idx, char in enumerate(w) if
               char == letter):
            continue

        # Check if any letter is at a position where we have already found a correct letter
        if correct_position_letters:
            candidates_with_correct_positions = [w]
            for letter, pos in correct_position_letters:
                # print('candidates_with_correct_positions: ', candidates_with_correct_positions)
                candidates_with_correct_positions = [c for c in candidates_with_correct_positions if c[pos] == letter]
            # print('candidates_with_correct_positions: ', candidates_with_correct_positions)
            candidates += candidates_with_correct_positions
            continue

        # Check if the word has the correct letters at the correct positions
        if all(w[pos] == letter for letter, pos in correct_position_letters):
            candidates.append(w)
        else:
            # Check if all letters at the correct position are in the same position in the candidate word
            for letter, pos in correct_position_letters:
                if letter in w:
                    if w[pos] != letter:
                        break
            else:
                # appends to the probable words list since it has passed all the criteria
                candidates.append(w)

    # Select a random word from the candidates list
    if candidates:
        next_word = random.choice(candidates)
        print("Next guess:", next_word)
        return next_word
    # if no word found in candidates, exit the code
    else:
        print("No matching words found.")
        exit()


def main():
    # Set the maximum number of guesses
    max_guesses = 6
    # Sets the initial number of guesses
    num_guesses = 1
    # Creates a list of letters that get feedback as 0
    incorrect_letters = []
    # Creates a list of (letters, position) that get feedback as 1
    correct_letter_incorrect_position = []
    # Creates a list of (letters, position) that get feedback as 2
    correct_position_letters = []

    # read the words file
    raw_data = read_file('words.txt')

    # gets the words and the probabilities of the words
    alphabet_prob, words = calc_prob(raw_data)

    # Gets the first word guessed based on probabilities
    next_word = cost_function(alphabet_prob, words)
    while num_guesses <= max_guesses:
        # This call gets all the updated lists for the guessed word
        feedback_list, incorrect_letters, correct_letter_incorrect_position, correct_position_letters = convert_word_to_list(next_word, incorrect_letters, correct_letter_incorrect_position, correct_position_letters)

        # if the correct word is guessed already, code ends
        if all(f == 2 for f in feedback_list):
            print("Congratulations, you have correctly guessed the word!")
            break

        # this call gets the updated next_word and then that word is again recursively passed in the while loop
        next_word = new_guess(incorrect_letters, correct_letter_incorrect_position, correct_position_letters, words)
        num_guesses += 1


if __name__ == '__main__':
    main()
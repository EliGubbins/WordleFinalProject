import heapq
from collections import defaultdict
import random
import sys


def get_letter_frequencies(words):
    position_freq = [defaultdict(int) for _ in range(5)]
    overall_freq = defaultdict(int)

    for word in words:
        for i, char in enumerate(word):
            position_freq[i][char] += 1
            overall_freq[char] += 1

    return position_freq, overall_freq

def score_word(word, position_freq, overall_freq):
    #return a score for each word based on the frequency of each letter in each postion
    score = 0
    seen = set()
    for i, char in enumerate(word):
        if char not in seen:
            score += overall_freq[char] * 0.5
        score += position_freq[i][char]
        seen.add(char)
    return score

def get_feedback(guess, target):
    feedback = ['b'] * 5
    target_chars = list(target)

    # check if its in the right place/green
    for i in range(5):
        if guess[i] == target[i]:
            feedback[i] = 'g'
            target_chars[i] = None

    # check if its the right letter but in the wrong place/yellow
    for i in range(5):
        if feedback[i] == 'b' and guess[i] in target_chars:
            feedback[i] = 'y'
            target_chars[target_chars.index(guess[i])] = None

    return feedback

def filter_words(words, guess, feedback):
    filtered = []

    for word in words:
        valid = True
        for i in range(5):
            if feedback[i] == 'g':
                if word[i] != guess[i]:
                    valid = False
                    break
            elif feedback[i] == 'y':
                if guess[i] not in word or word[i] == guess[i]:
                    valid = False
                    break
            elif feedback[i] == 'b':
                count_in_feedback = sum(
                    1 for j in range(5) if guess[j] == guess[i] and feedback[j] != 'b'
                )
                if word.count(guess[i]) > count_in_feedback:
                    valid = False
                    break
        if valid:
            filtered.append(word)

    return filtered

def best_first_search(word_list, target):
    position_freq, overall_freq = get_letter_frequencies(word_list)
    heap = []

    for word in word_list:
        score = -score_word(word, position_freq, overall_freq)
        heapq.heappush(heap, (score, word))

    guessed_words = set()
    attempts = 0
    history = []

    while heap and attempts < 6:
        _, guess = heapq.heappop(heap)

        if guess in guessed_words:
            continue
        guessed_words.add(guess)

        feedback = get_feedback(guess, target)
        history.append((guess, feedback))

        if feedback == ['g'] * 5:
            return history

        word_list = filter_words(word_list, guess, feedback)
        position_freq, overall_freq = get_letter_frequencies(word_list)

        heap = []
        for word in word_list:
            if word not in guessed_words:
                score = -score_word(word, position_freq, overall_freq)
                heapq.heappush(heap, (score, word))

        attempts += 1

    return history

def benchmark():
    pass

def random_word():
    pass

def prompted_input():
    pass



if __name__ == "__main__":
    with open('nyt-answers.txt') as f:
        word_list = [word.strip().lower() for word in f if len(word.strip()) == 5]
    match sys.argv[1].lower():
        case 'bench':
            pass
        case 'random':
            pass
        case 'input':
            pass
        case 'help':
            print("""
        
available arguements:
bench - run a benchmark on all valid words
random - run a test on a random word
input - run a test on a valid input
help - see valid arguments
""")
        case _:
            print("argument not recognized, maybe try help to see valid arguments")
            quit()

    target = num
    best_first_search(word_list, target)
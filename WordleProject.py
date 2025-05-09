import heapq
from collections import defaultdict

from numpy.ma.core import append


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

def wordle(word_list, target):
    position_freq, overall_freq = get_letter_frequencies(word_list)
    heap = []

    for word in word_list:
        score = -score_word(word, position_freq, overall_freq)
        heapq.heappush(heap, (score, word))

    guessed_words = set()
    attempts = 0
    history = []

    while heap:
        _, guess = heapq.heappop(heap)

        if guess in guessed_words:
            continue
        guessed_words.add(guess)

        feedback = get_feedback(guess, target)
        history.append((guess, feedback))

        if feedback == ['g'] * 5:
            return attempts+1

        word_list = filter_words(word_list, guess, feedback)
        position_freq, overall_freq = get_letter_frequencies(word_list)

        heap = []
        for word in word_list:
            if word not in guessed_words:
                score = -score_word(word, position_freq, overall_freq)
                heapq.heappush(heap, (score, word))
        attempts += 1


    return attempts

if __name__ == "__main__":
    count = 0
    total_attempts = 0
    attempt_list = []

    with open('nyt-answers.txt') as f:
        word_list = [word.strip().lower() for word in f if len(word.strip()) == 5]
    length = len(word_list)

    for target in word_list:
        current_attempt = wordle(word_list, target)
        total_attempts += current_attempt
        attempt_list.append(current_attempt)
        count +=1
        print(f'{target} --- {current_attempt} --- {count}/{length}')


    one = attempt_list.count(1)
    two = attempt_list.count(2)
    three = attempt_list.count(3)
    four = attempt_list.count(4)
    five = attempt_list.count(5)
    six = attempt_list.count(6)
    seven = attempt_list.count(7)
    eight = attempt_list.count(8)
    nine = attempt_list.count(9)

    avg = total_attempts / length
    print("------------------------")
    print(f"Average attempts: {avg:.2f}")
    print(f"""
    1: {one}---{one/count*100:.2f}%
    2: {two}---{two/count*100:.2f}% 
    3: {three}---{three/count*100:.2f}% 
    4: {four}---{four/count*100:.2f}% 
    5: {five}---{five/count*100:.2f}%
    6: {six}---{six/count*100:.2f}%
    below failed to get it in 6
    7: {seven}---{seven/count*100:.2f}%   
    8: {eight}---{eight/count*100:.2f}% 
    9: {nine}---{nine/count*100:.2f}% 
    """)





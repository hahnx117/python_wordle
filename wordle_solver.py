"""
Wordle word guesser.
Takes in a guess with the color values and returns a modified word list, e.g.

word: stand
response: NGYNN

N: Not in word
G: Green 
Y: Yellow

Zip these together to form a dictionary,
dict = {
    's': 'N',
    't': 'G',
    ...
}
"""

import sys
import random
import string

def green_check(player_guess, wordle_response, full_word_dict):
    """Mark words FALSE where green characters not in the correct spot."""
    for j in range(len(player_guess)):
        if wordle_response[j].upper() == 'G':
            for key in full_word_dict:
                if key[j] != player_guess[j]:
                    full_word_dict[key] = False

def yellow_check(player_guess, wordle_response, full_word_dict):
    """Mark words FALSE that are without yellow characters or with yellow characters in the incorrect spot."""
    for j in range(len(player_guess)):
        if wordle_response[j].upper() == 'Y':
            for key in full_word_dict:
                if player_guess[j] not in key:
                    full_word_dict[key] = False
                elif key[j] == player_guess[j]:
                    full_word_dict[key] = False

def grey_check(player_guess, wordle_response, full_word_dict):
    """Mark words FALSE with letters that arent in the target word at all."""
    for j in range(len(player_guess)):
        if wordle_response[j].upper() == 'N':
            for key in full_word_dict:
                if (player_guess[j] in key) and (player_guess.count(player_guess[j]) >= 2) and (full_word_dict[key] == True):
                    full_word_dict[key] = True
                elif player_guess[j] in key and player_guess.count(player_guess[j]) == 1:
                    full_word_dict[key] = False
                #else:
                #    print("Hard to handle double letters.")


def whats_left():
    """Print values it could be if less than a certain amount."""
    possible_list = []
    unique_list = []

    for key in full_word_dict:
        if full_word_dict[key]:
            possible_list.append(key)
            if len(set(key)) == 5:
                unique_list.append(key)
    
    print(f'\nThere are {len(possible_list)} possibilities.')

    if len(possible_list) == 1:
        print(f'The answer is {possible_list[0]}. Nice!\n')
        with open('answer_list.txt', 'a') as f:
            f.write(f'{possible_list[0]}\n')
        sys.exit(0)
    elif len(possible_list) == 0:
        print(f"There's been a problem. Check out the dict.")
        from pprint import pprint
        pprint(full_word_dict)
    elif len(possible_list) <= 100:
        print(possible_list)
        if unique_list:
            print(f'\nThe unique words are:')
            print(unique_list)
            print(f'\nYou should try {random.choice(unique_list)}')
        else:
            print(f'\nYou should try {random.choice(possible_list)}')
    else:
        print('The full list is too long to print.')
        print(f'\nYou should try {random.choice(unique_list)}')
    

def best_guess():
    """Take the remaining words and return the word that yields the lowest remaining possibilities.
    Score count how many times the letters of the alphabet occur.
    e.g. if a occurs 5 times, 'a': 5.
    Then score the remaining words by adding the letter scores."""
    remainder_list = []
    score_list = []
    alphabet_dict = {}

    # create list of word remainders
    for key in full_word_dict:
        if full_word_dict[key] == True:
            remainder_list.append(key)
    
    # create dictionary of alphabet characters
    for letter in list(string.ascii_lowercase):
        alphabet_dict[letter] = 0
    
    #get frequency of letters
    for word in remainder_list:
        if len(set(word)) == 5:
            for letter in list(word):
                alphabet_dict[letter] += 1
        
    # score words in tuples
    for word in remainder_list:
        if len(set(word)) == 5:
            word_score = 0
            for letter in list(word):
                word_score += alphabet_dict[letter]
            score_tuple = (word, word_score)
            score_list.append(score_tuple)
        # word_score = 0
    
    if score_list:
        print(score_list[-1])
    else:
        print("There are only words with repeating letters.")

# Play code
i = 1
full_word_dict = {}
test_word = ''
with open('wordlist.txt', 'r') as f:
    for word in f:
        full_word_dict[word.strip('\n')] = True

while i <= 6:

    if i == 1:
        while len(set(test_word)) != 5:
            test_word = random.choice(list(full_word_dict.keys()))
        print(f'You should try {test_word}.')
        # best_guess()
    else:
        best_guess()
    
    player_guess = input(f'Guess {i}: ').lower()
    wordle_response = input('Wordle response: (N)ot in word, (Y)ellow letter, (G)reen letter, e.g. NGYNN: ').upper()
    
    if 'G' in wordle_response:
        green_check(player_guess, wordle_response, full_word_dict)
        
    if 'Y' in wordle_response:
        yellow_check(player_guess, wordle_response, full_word_dict)

    if 'N' in wordle_response:
        grey_check(player_guess, wordle_response, full_word_dict)

    whats_left()

    i += 1

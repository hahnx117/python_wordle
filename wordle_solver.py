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

def green_check(player_guess, wordle_response):
    """Mark words FALSE where green characters not in the correct spot."""
    for j in range(len(player_guess)):
        if wordle_response[j].upper() == 'G':
            for key in full_word_dict:
                if key[j] != player_guess[j]:
                    full_word_dict[key] = False

def yellow_check(player_guess, wordle_response):
    """Mark words FALSE that are without yellow characters or with yellow characters in the incorrect spot."""
    for j in range(len(player_guess)):
        if wordle_response[j].upper() == 'Y':
            for key in full_word_dict:
                if player_guess[j] not in key:
                    full_word_dict[key] = False
                elif key[j] == player_guess[j]:
                    full_word_dict[key] = False

def grey_check(player_guess, wordle_response):
    """Mark words FALSE with letters that arent in the target word at all."""
    for j in range(len(player_guess)):
        if wordle_response[j].upper() == 'N':
            for key in full_word_dict:
                if player_guess[j] in key:
                    full_word_dict[key] = False


def whats_left():
    """Print values it could be if less than a certain amount."""
    possible_list = []

    for key in full_word_dict:
        if full_word_dict[key]:
            possible_list.append(key)
    
    print(f'There are {len(possible_list)} possibilities.')

    if len(possible_list) == 1:
        print(f'The answer is {possible_list[0]}. Nice!')
        sys.exit(0)
    elif len(possible_list) <= 100:
        print(possible_list)
    else:
        print('The list is too long to print.')
    

def best_guess():
    """Take the remaining words and return the word that yields the lowest remaining possibilities."""
    remainder_list = []

    for key in full_word_dict:
        if full_word_dict[key] == True:
            remainder_list.append(key)

# Play code
i = 1
full_word_dict = {}
with open('wordlist.txt') as f:
    for word in f:
        full_word_dict[word.strip('\n')] = True

while i <= 6:

    best_guess()

    player_guess = input(f'Guess {i}: ').lower()
    wordle_response = input('Wordle response: (N)ot in word, (Y)ellow letter, (G)reen letter, e.g. NGYNN: ').upper()
    
    if 'G' in wordle_response:
        green_check(player_guess, wordle_response)
    
    if 'Y' in wordle_response:
        yellow_check(player_guess, wordle_response)

    if 'N' in wordle_response:
        grey_check(player_guess, wordle_response)

    whats_left()

    i += 1
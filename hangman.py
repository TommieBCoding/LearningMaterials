import random
from words import words
import string

def get_valid_word(words):
    word = random.choice(words) #randomly chooses something from the list
    while "-" in word or " " in word: #eliminates words with spaces or hyphens
        word = random.choice(words)

    return word.upper()

def hangman():
    word = get_valid_word(words)
    word_letters = set(word) #save all of the letters in the string as a set
    alphabet = set(string.ascii_uppercase)
    used_letters = set() # what the user has guessed

    lives = 6

    #getting user input
    while len(word_letters) > 0 and lives > 0: #while the the string has more than 0 and you have lives, iterate
        #letters used
        # " ".join(["a","b","cd"]) --> "a b cd"
        print("You have used these letters: ", " ".join(used_letters))


        # what current word is (ie W - R D)
        word_list = [letter if letter in used_letters else "-" for letter in word]
        print("Current word: ", " ".join(word_list))

        user_letter = input("Guess a letter ").upper()
        if user_letter in alphabet - used_letters:
            used_letters.add(user_letter)
            if user_letter in word_letters:
                word_letters.remove(user_letter)
            else:
                lives -= 1 #takes one life away if you guess incorrectly
                print("A wrong guess, be careful! You lost a life!")
                print(f"You have {lives} lives remaining.")

        elif user_letter in used_letters:
            print("You have already used that character. Please try again.")

        else:
            print("Invalid character.")  
    if lives == 0:
        print("You died, sorry. The word was ", word)
    else:
        print(f"Wow you guessed it. The word was {word} Great Job!")      

hangman()
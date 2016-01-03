# -*- coding: utf-8 -*-
__author__ = 'Andrzej'

import random

the_number = 0
guess = 0
guess_count = 0

def play_game(guess):
    global  guess_count
    guess_count += 1

    if guess < the_number:
        return (False, " Dawaj wiencyj!")
    elif guess > the_number:
        return (False, " Za duzo, dawaj mniej!")
    return (True, "Trafiles za "+str(guess_count)+" razem! Gratki!")

def init_game():
    global the_number, guess, guess_count
    the_number = random.randint(1,100)
    guess = guess_count = 0

if __name__ == '__main__':
    game_result = False
    init_game()
    while not game_result:
        guess = input("Podaj liczbe: ")
        game_result, text = play_game(guess)
        print text


import pandas as pd
import re

words_file = open('wordle_words.txt', 'r')
big_words_file = open('words.txt','r')
letters_file = open('letters.txt', 'r')

big_words = big_words_file.readlines()
all_words = words_file.readlines()
all_letters = letters_file.readlines()

poss_letters = [i[0:1] for i in all_letters]
f_words = [i[0:5] for i in all_words]
f_big_words = [i[0:5] for i in big_words]

place_1 = []
place_2 = []
place_3 = []
place_4 = []
place_5 = []

yellow_letters = []
green_letters = []

place_1_poss = poss_letters.copy()
place_2_poss = poss_letters.copy()
place_3_poss = poss_letters.copy()
place_4_poss = poss_letters.copy()
place_5_poss = poss_letters.copy()

place_possibilities = [[1, place_1_poss],[2, place_2_poss],[3, place_3_poss],[4, place_4_poss], [5,place_5_poss]]

df = pd.DataFrame(place_possibilities, columns = ['Place', 'Poss_Letters'])

guesses = []
poss_words = f_words.copy()
guess_num = 0


def guesser(guess_no):
    print("This is guess number ", guess_no+1)
    greens = []
    yellows = []
    greys = [0,1,2,3,4]

    user_guess = (input("What was your guess? "))
    guesses.append(user_guess)

    n = int(input("How many greens were there?: "))
    for i in range(0, n):
        ele = int(input("One at a time, using numbers 0-4, where was the green?: "))
        greens.append(ele) 

    m = int(input("How many yellows?: ")) 
    
    for i in range(0, m):
        ele = int(input("One at a time, using numbers 0-4, where was the yellow?: "))
        yellows.append(ele) 
    for i in yellows:
        if i in greys:
            greys.remove(i)
    for i in greens:
        if i in greys:
            greys.remove(i)
    

    for i in greens:
        df.iloc[i,1] = user_guess[i]

    for i in yellows:
        try:
            df.iloc[i,1].remove(user_guess[i])
        except:
            pass
        yellow_letters.append(user_guess[i]) 

    for i in greys:
        for j in df["Poss_Letters"]:
            if user_guess[i] in yellow_letters:
                pass
            else:
                try:
                    j.remove(user_guess[i])
                except:
                    pass  
    letrange= [0,1,2,3,4]        
    for x in f_words:
        for po in yellow_letters:
            if po not in x:
                try:
                        poss_words.remove(x)
                except:
                    pass    
        for i in letrange:
            if x[i] not in df.iloc[i,1]:
                    try:
                        poss_words.remove(x)
                    except:
                        pass
    
    
    score_sheet = {}
    wordlist = f_big_words

    
    for q in wordlist:
            score_sheet[q] = 0

            for x in poss_words:
                for z in letrange:
                    if q[z] == x[z]:

                            if q[z] in green_letters:
                                    score_sheet[q] -= 1000
                                
                    elif q[z] not in list(x):
                            score_sheet[q] -= 100
                    elif q[z] != x[z]:
                        for i in range(0,4):    
                            if q[z] == x[i]:
                                if q[z] in yellow_letters:
                                    score_sheet[q] -= 100
                                elif q[z] in green_letters:
                                    score_sheet[q] -= 100
                                else:
                                    score_sheet[q] += 1000
                    if len(set(list(q))) < 5:
                        score_sheet[q] = 0
                
    sort_score_sheet = sorted(score_sheet.items(), key=lambda x: x[1], reverse=True)
    
    if len(poss_words) > 1:
        print(f"Here are the {len(poss_words)} remaining possible words:")
        for i in range(0,len(poss_words)):
            print(i+1, poss_words[i])
        if len(poss_words) == 2:
            print(f"There's only two left, so you're better off guessing here. \nPick between {poss_words[0]} and {poss_words[1]}")
        else:    
            print(f"\nThere are still {len(poss_words)} possibilities remaining,\nI reckon we should try this word next:")
            best = str(sort_score_sheet[0:1])
            f_best = re.sub("[^a-zA-Z]+", "", best)
            print(f_best)
    else:
        print("The word is:", poss_words[0])
    
guesser(guess_num)

while len(poss_words) > 1:
    if input("\nguess again? (y/n) ") == "y":
        guess_num +=1
        guesser(guess_num)
print(f"I got it in {guess_num+2}!")
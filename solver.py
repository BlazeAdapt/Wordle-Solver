import sys
import json
import numpy as np

targets1=[]
guessables=[]
colorings={}
automatic=True
combinations=[]
def makecombs(a):
    if len(a)==5:
        combinations.append(a)
        return
    makecombs(a+"g")
    makecombs(a+"r")
    makecombs(a+"y")
    return
with open("ans.txt", 'r') as f1:
    for i in f1.readlines():
        targets1.append(i[:-1])
with open("guessable.txt", 'r') as f1:
    for i in f1.readlines():
        guessables.append(i[:-1])
guess_index = {word: i for i, word in enumerate(guessables)}
answer_index = {word: i for i, word in enumerate(targets1)}

def solve(answer):
    guesses=[]
    history = []
    targets=targets1.copy()

    def makeguess():
        if not targets:
            raise ValueError("No possible answers remain")
        if len(targets) <= 2:
            return targets[0]
        target_ids = np.fromiter(
            (answer_index[word] for word in targets),
            dtype=np.intp,
            count=len(targets)
        )
        infos = np.empty(len(guessables), dtype=np.float64)
        for i in range(len(guessables)):
            patterns = feedback_matrix[i, target_ids]
            counts = np.bincount(patterns, minlength=243)

            counts = counts[counts > 0]
            probabilities = counts / len(targets)
            infos[i] = -np.sum(
                probabilities * np.log2(probabilities)
            )
        return guessables[int(np.argmax(infos))]

    def removal():
        nonlocal targets
        valid = []
        for word in targets:
            answer_id = answer_index[word]
            if all(
                    combinations[feedback_matrix[guess_index[previous_guess], answer_id]]
                    == feedback
                    for previous_guess, feedback in history
            ):
                valid.append(word)
        targets = valid
    # lets guess1 be salet
    guess="salet"
    feedacks=[]
    uses=0
    while targets:
        #print(guess)
        uses += 1
        guesses.append(guess)
        feedback = getcolsalt(guess, answer)
        feedacks.append(feedback)
        history.append((guess, feedback))

        if feedback == "ggggg":
            #print("hello")
            break
        removal()
        if uses >= 10:
            break
        guess=makeguess()
    print(guesses,uses)
    return uses,zip(guesses, feedacks)


def getcolsalt(guess, answer):
    result = ["r"] * 5
    remaining = {}
    for i in range(5):
        if guess[i] == answer[i]:
            result[i] = "g"
        else:
            remaining[answer[i]] = remaining.get(answer[i], 0) + 1
    for i in range(5):
        if result[i] == "g":
            continue
        letter = guess[i]
        if remaining.get(letter, 0) > 0:
            result[i] = "y"
            remaining[letter] -= 1
    return "".join(result)


def maketree(tree,l):
    branch=tree
    for guess,feed in l:
        if feed =="ggggg":
            branch["guess"]=guess
            break
        branch["guess"]=guess
        if feed not in branch:
            branch[feed]= {}

        branch=branch[feed]

def main():
    global feedback_matrix
    makecombs("")
    feedback_matrix = np.load("feedback_matrix.npy", mmap_mode="r")

    #to solve one specific word
    #solve("train")


    # to make a solution tree.json for html interface
    '''
    tree={}
    sum = 0
    max = 0
    loses=[]
    for i in targets1:
        n,l=solve(i)
        sum += n
        if n>6:
            loses.append(i)
        if n > max:
            max = n
        maketree(tree,l)
    with open("tree.json", 'w') as f1:
        f1.write(json.dumps(tree, indent=4))
    av = sum / len(targets1)
    print("average is: ", av)
    print("max is: ", max)
    '''


    #to only find average guesses per word
    '''
    for i in targets1:
        n,d=solve(i)
        sum+=n
        if n>max:
            max=n
        print(i)
    av=sum/len(targets1)
    print("average is: ",av)
    print("max is: ",max)'''


main()
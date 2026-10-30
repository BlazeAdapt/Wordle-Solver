import numpy as np
import sys
targets1=[]
guessables=[]
combinations=[]
def makecombs(a):
    if len(a)==5:
        combinations.append(a)
        return
    makecombs(a+"g")
    makecombs(a+"r")
    makecombs(a+"y")
    return
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
def wordcols(combination_id):
    rows=[]
    for a in range(len(guessables)):
        for b in range(len(targets1)):
            rows.append([a,b,combination_id[getcolsalt(guessables[a], targets1[b])]])
        sys.stdout.write(f"\r{a}")
        sys.stdout.flush()
    rows = np.array(rows, dtype=np.int16)
    return rows

with open("ans.txt", 'r') as f1:
    for i in f1.readlines():
        targets1.append(i[:-1])
with open("guessable.txt", 'r') as f1:
    for i in f1.readlines():
        guessables.append(i[:-1])
combination_id = {pattern: i for i, pattern in enumerate(combinations)}
rows=wordcols(combination_id)
np.save('my_rows.npy', rows)
rows = np.load("my_rows.npy")

feedback_matrix = np.empty(
    (len(guessables), len(targets1)),
    dtype=np.uint8
)

feedback_matrix[rows[:, 0], rows[:, 1]] = rows[:, 2]

np.save("feedback_matrix.npy", feedback_matrix)


# [Wordle Decipherer](https://wordle-decipher.vercel.app)

An interactive Wordle solver that uses precomputed decision trees to find the answer in as few guesses as possible.

Instead of simply suggesting possible words, Wordle Decipherer follows a decision tree: each guess determines the next guess based on the feedback received from Wordle.

## Features

- **Interactive Wordle grid:** Click individual tiles to cycle through gray, yellow, and green feedback. The next word is displayed automatically whenever feedback changes.
- **Two solving modes:**
  - **Quick:** Uses the original Wordle answer list of approximately 2,300 words.
  - **Realistic:** Uses a larger vocabulary of approximately 14,800 acceptable Wordle words, accounting for words outside the original answer list.
- **Precomputed decision trees:** Guesses are retrieved from generated trees rather than calculated from scratch during gameplay.

## How It Works

Wordle Decipherer uses a decision-tree-based approach.

1. The solver starts with the fixed opening guess `SALET`.
2. Enter that guess into Wordle.
3. Click the tiles in the interface to reproduce the feedback:
   - **Gray:** Letter is absent.
   - **Yellow:** Letter is present but in the wrong position.
   - **Green:** Letter is in the correct position.
4. The solver follows the corresponding feedback branch in its decision tree.
5. The next guess appears automatically.
6. Repeat until the answer is found.

Each node in the decision tree represents a guess, and its branches represent the possible feedback patterns.

## Solving Modes

| Mode | Answer vocabulary | Intended use |
|---|---|---|
| Quick | ~2,300 original answer words | Testing against the original Wordle answer list |
| Realistic | ~14,800 acceptable words | Playing against the broader Wordle vocabulary |

The two modes use separate decision-tree files:

- `tree.json` — Quick mode
- `treebig.json` — Realistic mode

Switching modes resets the current solving session.

## Running Locally

The project is a static website and does not require a backend server or database.

1. Clone the repository:

   ```bash
   git clone https://github.com/BlazeAdapt/Wordle-Solver.git
   cd Wordle-Solver
   ```

2. Make sure the HTML, CSS, JavaScript, and decision-tree JSON files are in the same directory.

3. Start a local HTTP server:

   ```bash
   python -m http.server 8000
   ```

4. Open the website:

   ```text
   http://localhost:8000
   ```

**Note:** Use a local HTTP server rather than opening `index.html` directly, because the solver loads its JSON files using `fetch()`.

## Project Structure

```text
Wordle-Solver/
│
├── Website/      # Website interface
|
├── tree.json        # Quick mode decision tree
├── treebig.json     # Realistic mode decision tree
│
├── ans.txt          # Possible answer words
├── guessable.txt    # Acceptable guess words
│
└── *.py             # Scripts for generating and evaluating
                   # the decision trees
```

## Limitations

- The solver depends on its precomputed word lists and decision trees.
- The opening guess must be `SALET`.
- The Realistic mode is designed to cover a broader vocabulary, but Wordle's accepted words and answer list can change over time.
- The Realistic mode currently fails on certain ~10 words on the 14,000 word list
---

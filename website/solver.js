let tree = null;
let currentNode = null;

let nodearr = [];
let guessarr = [];
let color_rotation = ["r", "y", "g"];
let word_colors = [];
let currentTreeFile = "tree.json";

// Load the decision tree.
async function loadTree(filename = currentTreeFile) {
    try {
        currentTreeFile = filename;

        const response = await fetch(filename);

        if (!response.ok) {
            throw new Error("Could not load " + filename);
        }

        tree = await response.json();
        currentNode = tree;

        nodearr = [currentNode];
        guessarr = [currentNode.guess];
        word_colors = ["rrrrr"];

        document.getElementById("message").textContent = "";

        renderGuesses();

        console.log("Loaded:", filename);
        console.log("First guess:", currentNode.guess);
    } catch (error) {
        console.error(error);
        document.getElementById("message").textContent =
            "Failed to load " + filename;
    }
}

function switchMode(filename) {
    if (filename === currentTreeFile) return;

    document.getElementById("normal-mode")
        .classList.toggle("active", filename === "tree.json");

    document.getElementById("big-mode")
        .classList.toggle("active", filename === "treebig.json");

    loadTree(filename);
}

// Check whether a node is a leaf (final answer).
function isLeaf(node) {
    return Object.keys(node).every(key => key === "guess");
}

// Render all guesses as clickable tiles.
function renderGuesses() {
    const container = document.getElementById("guesses");
    container.replaceChildren();

    guessarr.forEach((word, index) => {
        const row = document.createElement("div");
        row.className = "guess-row";

        const isFinal = index > 0 && isLeaf(nodearr[index]);

        for (let i = 0; i < 5; i++) {
            const tile = document.createElement("button");
            tile.className = "tile";
            tile.textContent = word[i].toUpperCase();

            const color = word_colors[index][i];

            tile.classList.add(
                color === "r" ? "gray" :
                color === "y" ? "yellow" : "green"
            );

            // The final answer cannot be clicked.
            tile.disabled = isFinal;

            tile.addEventListener("click", () => {
                colorchange(word, i);
            });

            row.appendChild(tile);
        }

        container.appendChild(row);
    });
}

// Change a tile's color and immediately calculate the next guess.
function colorchange(word, ind) {
    const index = guessarr.indexOf(word);

    if (index === -1) return;

    // Cycle the clicked tile: gray -> yellow -> green -> gray.
    const colors = word_colors[index].split("");
    const oldColor = color_rotation.indexOf(colors[ind]);

    colors[ind] = color_rotation[(oldColor + 1) % 3];
    word_colors[index] = colors.join("");

    // Discard guesses based on the old feedback.
    guessarr.splice(index + 1);
    nodearr.splice(index + 1);
    word_colors.splice(index + 1);

    // Return to the node for the guess that was clicked.
    currentNode = nodearr[index];

    document.getElementById("message").textContent = "";

    // Look up the branch for the new feedback.
    const feedback = word_colors[index];
    const nextNode = currentNode[feedback];

    if (!nextNode) {
        document.getElementById("message").textContent =
            "No matching branch for feedback: " + feedback.toUpperCase();

        renderGuesses();
        return;
    }

    // Add the next guess.
    currentNode = nextNode;

    guessarr.push(currentNode.guess);
    nodearr.push(currentNode);
    word_colors.push("rrrrr");

    // If this is a leaf, display it as the final answer.
    if (isLeaf(currentNode)) {
        word_colors[word_colors.length - 1] = "ggggg";

        document.getElementById("message").textContent =
            "Answer found: " + currentNode.guess.toUpperCase();
    }

    renderGuesses();
}

// Start the solver.
loadTree();
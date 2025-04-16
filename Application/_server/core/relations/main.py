import matplotlib.pyplot as plt
import numpy as np
import math
from scipy.linalg import svd

from .parseFile import countWords


def showTopWords(U, S, words, k, int=3, topN=5, printWords: bool = False) -> dict:
    topWordsPerConcept = {}

    for i in range(k):

        if printWords:

            print(f"Top words for Concept {i+1}:")

        concept_vector = U[:, i]

        top_indices = np.argsort(np.abs(concept_vector))[::-1][:topN]

        topWordsPerConcept[i + 1] = words[top_indices[0]]

        if printWords:

            for idx in top_indices:

                print(f"{words[idx]} -> {concept_vector[idx]:.4f}")

            print()

    return topWordsPerConcept


def getCosineSimilarity(v1: list, v2: list) -> float:
    dot_product = np.dot(v1, v2)

    norm_v1 = np.linalg.norm(v1)

    norm_v2 = np.linalg.norm(v2)

    if norm_v1 == 0 or norm_v2 == 0:

        return 0.0

    return dot_product / (norm_v1 * norm_v2)


def parseAllFiles(noteObj: dict) -> dict:
    allWordCounts = {}

    for note in noteObj["userNotes"]:

        content = note.get("note content")

        wordCount = countWords(content)

        allWordCounts[note["note name"]] = wordCount

    return allWordCounts


def makeMatrix(allWordCounts: dict) -> list:
    allWords = sorted(set().union(*allWordCounts.values()))

    matrix = []

    for filePath, wordCount in allWordCounts.items():

        row = [wordCount.get(word, 0) for word in allWords]

        matrix.append(row)

    return matrix, list(allWords)


def main(notesObj: dict):
    noteNameArray = []

    for note in notes["userNotes"]:
        noteNameArray.append(note["note name"])

    allWordCounts = parseAllFiles(notesObj)

    matrix, words = makeMatrix(allWordCounts)

    matrix = np.array(matrix).T

    U, S, Vt = svd(matrix, full_matrices=False)

    k = 3

    Sk = np.diag(S[:k])

    Vk = Vt[:k, :]

    Dk = np.dot(Sk, Vk).T

    # topConceptWords = showTopWords(U, S, words, k=3, topN=3)

    fig = plt.figure(figsize=(8, 6))

    ax = fig.add_subplot(111, projection="3d")

    DkNorm = Dk / np.linalg.norm(Dk, axis=1)[:, np.newaxis]

    scaleFactor = 0.1

    DkScaled = DkNorm * scaleFactor

    docsAndClosest = {}

    for idx, docVector in enumerate(DkScaled):
        vectorComponentsAdded = docVector[0] ** 2 + docVector[1] ** 2

        magOfVector = math.sqrt(vectorComponentsAdded)

        closestAngle = 1000

        closestDoc = "None"

        for otherIDX, otherDocVector in enumerate(DkScaled):
            if noteNameArray[idx] == noteNameArray[otherIDX]:
                pass

            else:

                otherVectorComponentsAdded = (
                    otherDocVector[0] ** 2 + otherDocVector[1] ** 2
                )

                otherMagOfVector = math.sqrt(otherVectorComponentsAdded)

                currAngle = math.acos(
                    (
                        (
                            docVector[0] * otherDocVector[0]
                            + docVector[1] * otherDocVector[1]
                        )
                        / (magOfVector * otherMagOfVector)
                    )
                )

                if currAngle < closestAngle:
                    closestAngle = currAngle

                    closestDoc = noteNameArray[otherIDX]

        print(f"Closest doc to {noteNameArray[idx]} is {closestDoc}")

        docsAndClosest[noteNameArray[idx]] = closestDoc

    return docsAndClosest


if __name__ == "__main__":
    # How to use

    notes = {
        "userNotes": [
            {
                "note name": "Test 2",
                "note content": "As technology advanced, so did our reach. The 20th century brought an explosion of innovation that transformed dreams of space travel into reality. The Moon landings, robotic probes, and space telescopes like Hubble revealed a universe far more complex and beautiful than we had ever imagined. Yet, for all we’ve achieved, our knowledge still feels like a drop in the cosmic ocean — and that humbling realization continues to fuel exploration.",
            },
            {
                "note name": "Test 1",
                "note content": "From the earliest days of civilization, humans have looked up at the night sky with wonder, mapping constellations and telling stories about the stars. This innate curiosity about what lies beyond our world has driven countless discoveries and shaped entire cultures. It’s a testament to our nature — a species constantly seeking to understand the unknown and push beyond visible horizon.",
            },
        ]
    }

    print(main(notes))

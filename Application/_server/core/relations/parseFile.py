import os, json


def loadFile(filePath: str, jsonType: bool = False) -> str:
    fullPath = os.path.join(os.getcwd(), filePath)

    with open(fullPath, "r") as file:

        if jsonType:
            content = json.load(file)
        else:
            content = file.read()

    return content


def countWords(content: str) -> dict:
    INGORELIST = loadFile("Application/_server/core/relations/IGNORELIST.json")
    
    words = content.split()

    wordCount = {}

    for word in words:

        word = word.lower()

        word = word.strip("-=_+<>.,!?()[]{};:\"'")

        if word not in INGORELIST:

            if word in wordCount:

                wordCount[word] += 1

            else:

                wordCount[word] = 1
        else:
            continue

    return wordCount


if __name__ == "__main__":
    filePath = "Full-Stack-Project/Application/src/relations/testDocuments/test1.txt"

    if os.path.exists(filePath):

        content = loadFile(filePath)

        wordCount = countWords(content)

        print(wordCount)

    else:

        print(f"File {filePath} does not exist.")

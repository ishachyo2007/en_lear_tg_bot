import json
def sq_add_user(us_id):
    try:
        with open(f"{str(us_id)}.json", "r", encoding="utf-8") as f:
            pass
    except:
        with open(f"{str(us_id)}.json", "w", encoding="utf-8") as f:
            pass

def sq_add_word(us_id, word, translate_word):
    with open(f"{str(us_id)}.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    word = word.lower()
    translate_word = translate_word.lower()
    if word in data:
        return "the word is already on the list."

    data[word] = {
        "translation": translate_word,
        "level": 1
    }
    with open(f"{str(us_id)}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return "the word was successfully added to the list."

def sq_del_word(us_id, word):
    with open(f"{str(us_id)}.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    word = word.lower()
    if word in data:
        del data[word]
        with open(f"{str(us_id)}.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return f"The word {word} has been successfully removed from the list."
    return f"The word {word} is not on the list."

def sq_word_list(us_id):
    with open(f"{str(us_id)}.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    all_words = []
    for i in data:
        all_words.append(i)
    return all_words

def quiz(us_id):
    with open(f"{str(us_id)}.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    all_quiz = []
    for i in data:
        if data[i]["level"] < 5:
            all_quiz.append(i)

    return all_quiz, len(all_quiz)

def true_answer(us_id):
    with open(f"{str(us_id)}.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def upgrade_level(us_id, word, count):
    with open(f"{str(us_id)}.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    word = word.lower()
    data[word]["level"] += count
    with open(f"{str(us_id)}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
"""data = {
    "word": "cat",
    "translate": "кот",
    "level": 1
}

with open("ishachyo.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(data, ensure_ascii=False, indent=4))

with open("ishachyo.json", "r", encoding="utf-8") as f:
    da = json.load(f)
    print(data)"""
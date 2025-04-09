import subprocess
import time
import re
from collections import Counter

models = ["llama3.1", "phi4"]
topics = ["Battlefield", "Minecraft" ,"Islam", "manga"]

# Functie om een prompt naar Ollama te sturen en de output te krijgen
def generate_words(prompt, model):
    command = ["ollama", "run", model, prompt]
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout.strip()

# Functie om woorden naar een bestand te schrijven (inclusief frequentie)
def save_words_to_file(word_freq, filename):
    with open(filename, "w", encoding="utf-8") as f:
        for word,count in word_freq.items():
            f.write(f"{count} {word}\n")

# Functie om 10.000 unieke woorden te verzamelen en hun frequentie bij te houden
def generate_unique_word_frequencies(target_count, topic, model):
    # Hier initialiseer ik wat lijsten
    word_freq = {}
    # Ik gebruik een set hier om een lijst met alleen de unieke woorden uit de woordenlijst op te slaan.
    #word_set = set()
    #freqlist = []
    
    prompt = f"Give me 200 words related to {topic} in some way. The output is a list with one term per line. HOWEVER, do NOT include explanations or comments, numbers or formatting symbols in the list. I ONLY want words in the output."

    while len(word_freq) < target_count:  # 10.000 unieke woorden
        # Run het model
        result = generate_words(prompt, model)
        words = result.split()

        # Verwijder woorden die beginnen met cijfers gevolgd door een punt, want dit was een probleem in eerdere runs
        words = [word for word in words if not re.match(r"^\d+\.$", word)]

        # Tel de frequentie op
        for word in words:
            if word not in word_freq:
                word_freq[word] = words.count(word)
            else:
                word_freq[word] += words.count(word)

        print(f"Generated {len(word_freq)} / {target_count} unique words so far.")
        time.sleep(5)  # Verminder belasting op Ollama

    return word_freq

# Genereer één grote lijst van 10.000 unieke woorden
for model in models:
    for topic in topics:
        word_frequencies = generate_unique_word_frequencies(10000, topic, model)

        # Bestand opslaan met de woordfrequenties
        filename = f"{topic}{model}10000.txt"
        save_words_to_file(word_frequencies, filename)
        print(f"Saved 10000 unique words with frequencies to {filename}")

print("All files generated successfully.")

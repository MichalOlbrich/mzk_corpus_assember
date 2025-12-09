import os
import regex as re
from collections import Counter

def collect_decade_stats(input_dir = "./results", output_file = "decades_stats_cz.tsv"):

    os.makedirs("./data_outputs", exist_ok=True)

    # Regex that keeps only letters and spaces (removes digits/punct)
    clean_pattern = re.compile(r"[^\p{L}\s]", re.UNICODE)

    stats = []

    for filename in sorted(os.listdir(input_dir)):


        decade = filename.replace("_decade_mzk_books.txt", "")

        filepath = os.path.join(input_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read().lower()
        # Remove non-letter, non-space chars
        text = clean_pattern.sub(" ", text)
        # Split into words
        words = text.split()
        word_cnt = len(words)
        uniq_word_cnt = len(set(words))
        stats.append((decade, word_cnt, uniq_word_cnt))

    # Write stats to TSV
    with open("./data_outputs/"+output_file, "w", encoding="utf-8") as f:
        f.write("decade\tword_cnt\tuniq_word_cnt\n")
        for decade, wc, uwc in stats:
            f.write(f"{decade}\t{wc}\t{uwc}\n")

    print(f"Decade statistics written to {output_file}")

def collect_decade_wordfreqs(startswith=""):
    input_dir = "./results"
    output_dir = "./data_outputs/decades_wordfreqs"
    os.makedirs(output_dir, exist_ok=True)

    # Unicode-aware: keep only letters
    word_pattern = re.compile(r"\p{L}+", re.UNICODE)

    for filename in sorted(os.listdir(input_dir)):
        if not filename.startswith(startswith):
            continue

        decade = filename.replace("_decade_mzk_books.txt", "")
        filepath = os.path.join(input_dir, filename)

        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read().lower()

        # Extract all words (letters only)
        words = word_pattern.findall(text)

        # Count frequencies
        counter = Counter(words)
        filtered_counter = Counter({w: c for w, c in counter.items() if c > 4})

        # Save TSV
        outpath = os.path.join(output_dir, f"decade_{decade}.tsv")
        with open(outpath, "w", encoding="utf-8") as out:
            out.write("word\tfrequency\n")
            for word, freq in filtered_counter.most_common():
                out.write(f"{word}\t{freq}\n")

    print(f"Word frequency TSVs written to {output_dir}")
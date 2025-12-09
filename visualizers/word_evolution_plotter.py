import os
import pandas as pd
import matplotlib.pyplot as plt


def plot_word_frequencies(words, year_begin=1850, year_end=1950, log_scale=False, normalized=True):
    """
    Plot frequencies of given words across decades.

    Args:
        words (list[str]): list of words to track
        year_begin (int): earliest decade to include
        year_end (int): latest decade to include
        log_scale (bool): if True, use log scale on y-axis
        normalized (bool): if True, plot relative frequency (per total words in decade)
    """
    freq_dir = "./data_outputs/decades_wordfreqs"
    stats_file = "./data_outputs/decades_stats_cz.tsv"

    # Normalize words to lowercase
    words = [w.lower() for w in words]

    # Load decade stats for normalization
    stats_df = pd.read_csv(stats_file, sep="\t")  # infer header
    stats_df["decade"] = stats_df["decade"].astype(int)
    stats_dict = dict(zip(stats_df["decade"], stats_df["word_cnt"]))

    # Collect data
    decades = []
    data = {w: [] for w in words}

    for fname in sorted(os.listdir(freq_dir)):
        if not fname.startswith("decade_") or not fname.endswith(".tsv"):
            continue

        decade = int(fname.replace("decade_", "").replace(".tsv", ""))
        if not (year_begin <= decade <= year_end):
            continue

        decades.append(decade)

        # Load frequency file
        df = pd.read_csv(os.path.join(freq_dir, fname), sep="\t")

        # Make lookup dict for fast access
        freq_map = dict(zip(df["word"], df["frequency"]))

        total_words = stats_dict.get(decade, 1)  # avoid div/0
        for w in words:
            count = freq_map.get(w, 0)
            if normalized:
                count = count / total_words
            data[w].append(count)

    # Plot
    plt.figure(figsize=(12, 6))

    for w in words:
        plt.plot(decades, data[w], marker="o", label=w)

    plt.xlabel("Decade")
    plt.ylabel("Relative Frequency" if normalized else "Frequency")
    plt.title(f"Word Frequencies Over Time ({year_begin}–{year_end})")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6)

    if log_scale:
        plt.yscale("log")

    plt.tight_layout()
    outpath = f"./data_outputs/word_freqs_{year_begin}_{year_end}{'_norm' if normalized else ''}.png"
    plt.savefig(outpath, dpi=300)
    plt.show()

    print(f"Word frequency plot saved to {outpath}")

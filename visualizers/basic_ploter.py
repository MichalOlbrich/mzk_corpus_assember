import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit

def plot_decade_stats(year_begin=1850, year_end=1940, log_scale=True,stats_file = "./data_outputs/decades_stats_cz.tsv"):


    # Load TSV
    df = pd.read_csv(stats_file, sep="\t")
    df["decade"] = df["decade"].astype(int)

    # Filter
    df = df[(df["decade"] >= year_begin) & (df["decade"] <= year_end)]
    df = df.sort_values("decade")

    if df.empty:
        print(f"No data available between {year_begin} and {year_end}")
        return

    decades = df["decade"].astype(str)
    word_cnt = df["word_cnt"]
    uniq_cnt = df["uniq_word_cnt"]

    x = np.arange(len(decades))
    width = 0.6  # main bar width

    plt.figure(figsize=(12, 6))

    # Total word bars
    plt.bar(x, word_cnt, width, label="Total words", color="skyblue")

    # Unique word bars in front
    plt.bar(x, uniq_cnt, width * 0.5, label="Unique words", color="steelblue")

    plt.xticks(x, decades, rotation=45)
    plt.xlabel("Decade")
    plt.ylabel("Count")
    plt.title(f"Word and Unique Word Counts ({year_begin}–{year_end})")
    plt.legend()
    plt.grid(axis="y", linestyle="--", alpha=0.6)

    if log_scale:
        plt.yscale("log")

    plt.tight_layout()
    outpath = f"./data_outputs/decades_word_cz_counts_{year_begin}_{year_end}.png"
    plt.savefig(outpath, dpi=300)
    plt.show()

    print(f"Bar plot saved to {outpath}")


def plot_decade_stats_comparison(
    year_begin=1850,
    year_end=1940,
    log_scale=True,
    stats_file="./data_outputs/decades_stats_cz.tsv",
    unfiltered_stats_file="./data_outputs/decades_stats_unfiltered.tsv",
):
    # Load TSVs
    df_filt = pd.read_csv(stats_file, sep="\t")
    df_unfilt = pd.read_csv(unfiltered_stats_file, sep="\t")

    for df in (df_filt, df_unfilt):
        df["decade"] = df["decade"].astype(int)
        df = df[(df["decade"] >= year_begin) & (df["decade"] <= year_end)]

    df_filt = df_filt.sort_values("decade")
    df_unfilt = df_unfilt.sort_values("decade")

    if df_filt.empty or df_unfilt.empty:
        print(f"No data available between {year_begin} and {year_end}")
        return

    decades = df_filt["decade"].astype(str)
    x = np.arange(len(decades))

    group_width = 0.35      # filtered vs unfiltered
    inner_width = 0.6       # total vs unique inside group

    plt.figure(figsize=(14, 6))

    # ---- Filtered ----
    plt.bar(
        x - group_width / 2,
        df_filt["word_cnt"],
        group_width,
        label="Filtered – Total",
    )
    plt.bar(
        x - group_width / 2,
        df_filt["uniq_word_cnt"],
        group_width * inner_width,
        label="Filtered – Unique",
    )

    # ---- Unfiltered ----
    plt.bar(
        x + group_width / 2,
        df_unfilt["word_cnt"],
        group_width,
        label="Diakon – Total",
    )
    plt.bar(
        x + group_width / 2,
        df_unfilt["uniq_word_cnt"],
        group_width * inner_width,
        label="Diakon – Unique",
    )

    plt.xticks(x, decades, rotation=45)
    plt.xlabel("Decade")
    plt.ylabel("Count")
    plt.title(f"Word and Unique Word Counts ({year_begin}–{year_end})")
    plt.legend(ncol=2)
    plt.grid(axis="y", linestyle="--", alpha=0.6)

    if log_scale:
        plt.yscale("log")

    plt.tight_layout()
    outpath = f"./data_outputs/decades_word_comparison_counts_diakon_{year_begin}_{year_end}.png"
    plt.savefig(outpath, dpi=300)
    plt.show()

    print(f"Bar plot saved to {outpath}")


def plot_decade_unique_stats(
    year_begin=1850,
    year_end=1940,
    log_scale=True,
    stats_file="./data_outputs/decades_stats_cz.tsv",
    unfiltered_stats_file="./data_outputs/decades_stats_unfiltered.tsv",
):
    # Load TSVs
    df_filt = pd.read_csv(stats_file, sep="\t")
    df_unfilt = pd.read_csv(unfiltered_stats_file, sep="\t")

    for df in (df_filt, df_unfilt):
        df["decade"] = df["decade"].astype(int)

    df_filt = df_filt[
        (df_filt["decade"] >= year_begin) & (df_filt["decade"] <= year_end)
    ].sort_values("decade")

    df_unfilt = df_unfilt[
        (df_unfilt["decade"] >= year_begin) & (df_unfilt["decade"] <= year_end)
    ].sort_values("decade")

    if df_filt.empty or df_unfilt.empty:
        print(f"No data available between {year_begin} and {year_end}")
        return

    decades = df_filt["decade"].astype(str)
    x = np.arange(len(decades))

    width = 0.35  # filtered vs unfiltered

    plt.figure(figsize=(14, 6))

    plt.bar(
        x - width / 2,
        df_filt["uniq_word_cnt"],
        width,
        label="Filtered",
    )

    plt.bar(
        x + width / 2,
        df_unfilt["uniq_word_cnt"],
        width,
        label="Unfiltered",
    )

    plt.xticks(x, decades, rotation=45)
    plt.xlabel("Decade")
    plt.ylabel("Unique word count")
    plt.title(f"Unique Word Counts ({year_begin}–{year_end})")
    plt.legend()
    plt.grid(axis="y", linestyle="--", alpha=0.6)

    if log_scale:
        plt.yscale("log")

    plt.tight_layout()
    outpath = f"./data_outputs/decades_unique_word_comparision_{year_begin}_{year_end}.png"
    plt.savefig(outpath, dpi=300)
    plt.show()

    print(f"Bar plot saved to {outpath}")


def heaps_law_fit(stats_file = "./data_outputs/decades_stats.tsv"):

    df = pd.read_csv(stats_file, sep="\t")

    N = df["word_cnt"].values
    V = df["uniq_word_cnt"].values

    # Define Heaps’ law function
    def heaps(N, K, beta):
        return K * (N ** beta)

    # Fit curve
    popt, _ = curve_fit(heaps, N, V, p0=[10, 0.5])  # initial guess: K=10, β=0.5
    K, beta = popt

    print(f"Fitted Heaps’ law parameters: K = {K:.4f}, β = {beta:.4f}")

    # Plot empirical data vs fitted curve
    plt.figure(figsize=(8, 6))
    plt.scatter(N, V, label="Observed (per decade)", color="blue")
    N_fit = np.linspace(min(N), max(N), 200)
    plt.plot(N_fit, heaps(N_fit, K, beta), color="red", label=f"Fit: V = {K:.2f} * N^{beta:.2f}")

    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Total words (N)")
    plt.ylabel("Unique words (V)")
    plt.title("Heaps’ Law Fit on Decade Corpora")
    plt.legend()
    plt.grid(True, which="both", linestyle="--", alpha=0.6)

    plt.tight_layout()
    plt.savefig("./data_outputs/heaps_fit_cz.png", dpi=300)
    plt.show()

    return K, beta

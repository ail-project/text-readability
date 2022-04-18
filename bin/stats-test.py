from readability import Readability
from guesslang import Guess
import cld3
import os
import sys
import magic
import json

dataset = "../../JTAN-dataset/pastebin-20210901/"
# This part is costly (models are loaded) - should be done at loading (and not
# for each item to analyse.
guess = Guess()


def cal_readability(text=None, id=None, filepath=None):
    if text is None:
        return False
    analysis = {}
    analysis["length"] = len(text)
    analysis["id"] = id
    analysis["filename"] = filename
    analysis["magic-type"] = magic.from_buffer(text)
    r = Readability(text)
    try:
        flesch = r.flesch_kincaid()
        analysis["flesch_kindcaid_score"] = flesch.score
    except:
        pass
    try:
        flesch = r.flesch()
        analysis["flesch_score"] = flesch.score
        analysis["flesch_ease"] = flesch.ease
    except:
        pass

    try:
        analysis["ari"] = r.ari().score
    except:
        pass
    try:
        analysis["smog"] = r.smog(ll_sentences=True).score
    except:
        pass
    try:
        analysis["dale_chall"] = r.dale_chall().score
    except:
        pass
    try:
        analysis["linsear_write"] = r.linsear_write().score
    except:
        pass
    lang_guess = guess.language_name(text)
    lang_guess_probabilities = guess.probabilities(text)
    # 0.95 is calculated on some random dataset from gist.github.com
    if lang_guess_probabilities[0][1] > 0.95:
        analysis["programming_language_guess"] = lang_guess
        analysis["programming_language_guess_probabilities"] = lang_guess_probabilities[
            0
        ][1]
    lang = cld3.get_language(text)
    if lang.probability > 0.95:
        analysis["natural_language"] = lang.language
    return analysis


all_analysis = []

with os.scandir(dataset) as dset:
    for entry in dset:
        if not entry.name.startswith(".") and entry.is_file():
            filename = os.path.join(dataset, entry.name)
            with open(filename, "r") as f:
                text = f.read()
                print(f"Processing {entry.name}", file=sys.stderr)
                all_analysis.append(
                    cal_readability(text=text, id=entry.name, filepath=filename)
                )

print(json.dumps(all_analysis))

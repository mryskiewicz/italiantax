import polars as pl
from conllu import parse
import io

# Odczyt pliku
with open("it_isdt-ud-train.conllu", "r", encoding="utf-8") as f:
    text = f.read()

# Parsowanie pliku CoNLL-U
sentences = parse(text)

# Przygotowanie danych do DataFrame
data = []
for sentence in sentences:
    for token in sentence:
        data.append({
            "ID": str(token["id"]),
            "FORM": str(token["form"]),
            "LEMMA": str(token["lemma"]),
            "UPOS": str(token["upos"]),
            "XPOS": str(token["xpos"]),
            "FEATS": str(token["feats"]),
            "HEAD": str(token["head"]),
            "DEPREL": str(token["deprel"]),
            "DEPS": str(token["deps"]),
            "MISC": str(token["misc"])
        })

# Tworzenie DataFrame
df = pl.DataFrame(data)

# Liczenie nominalności
nominal = df.filter(pl.col("UPOS").is_in(["NOUN", "PROPN", "PRON", "ADJ", "NUM"])).height
verbal = df.filter(pl.col("UPOS").is_in(["VERB", "AUX"])).height

nominality = nominal / verbal if verbal > 0 else 0
print(f"Nominalność: {nominality:.2f}")

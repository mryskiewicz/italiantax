import pdfplumber
import re

pdf_path = "code.pdf"
text = ""

with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        text += page.extract_text() + "\n"

with open("kodeks.txt", "w", encoding="utf-8") as f:
    f.write(text)

unwanted_phrases = ["Torna al sommario", "Decreto del Presidente della Repubblica del 26/10/1972 n. 633 -"]
remove_with_next_line = [r"^nota:"]
remove_only_this_line = [r"^modificato da:", r"^in vigore dal", r"^pagina"]

def clean_text(text, unwanted_phrases, remove_with_next_line, remove_only_this_line):
    for phrase in unwanted_phrases:
        text = text.replace(phrase, "")

    lines = text.split("\n")
    cleaned_lines = []
    skip_next = False

    for i, line in enumerate(lines):
        if skip_next:
            skip_next = False
            continue

        if any(re.match(pattern, line, re.IGNORECASE) for pattern in remove_with_next_line):
            skip_next = True  # Oznaczamy do pominięcia następnej linii
            continue  # Pomijamy aktualną linię

        if any(re.match(pattern, line, re.IGNORECASE) for pattern in remove_only_this_line):
            continue  # Pomijamy tylko aktualną linię

        cleaned_lines.append(line)

    return "\n".join(cleaned_lines)

# Wczytanie pliku tekstowego
with open("kodeks.txt", "r", encoding="utf-8") as f:
    raw_text = f.read()

# Czyszczenie tekstu
cleaned_text = clean_text(raw_text, unwanted_phrases, remove_with_next_line, remove_only_this_line)

# Zapisanie czystego tekstu do pliku
with open("kodeks_clean.txt", "w", encoding="utf-8") as f:
    f.write(cleaned_text)

print("Czyszczenie zakończone. Wynik zapisano do 'kodeks_clean.txt'.")

with open("kodeks_clean.txt", "r", encoding="utf-8") as f:
    text_cleaned = f.read()

def segment_articles(text):
    articles = re.split(r'(?=Articolo \d+)', text_cleaned)  # Podział na artykuły
    return [article.strip() for article in articles if article.strip()]

articles = segment_articles(text_cleaned)

for i, article in enumerate(articles[:5], 1):  # Podgląd pierwszych 5 artykułów
    print(f"=== ARTICOLO {i} ===\n{article[:500]}\n")

# Zapisanie do plików
with open("segmented_articles.txt", "w", encoding="utf-8") as f:
    f.write("\n\n".join(articles))


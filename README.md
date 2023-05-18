# NLTK project

Dit project bevat de code van het NLTK project dat is gemaakt voor PAV TTTV.

# Installatie

- `git clone https://github.com/koomen/pav-nltk & cd pav-nltk`
- `pip3 install -r requirements.txt`

# Gebruik

Omdat phrase structure rules te genereren maken we gebruik van de Standard
CoreNLP. In python gebruiken we een wrapper package die de API aanroept die je
lokaal hebt draaien, maar deze moet je dus installeren. Installeer CoreNLP v4
[hier](https://stanfordnlp.github.io/CoreNLP).

Om CoreNLP te draaien lokaal, heb je ook java nodig. Voor Mac gebruiker kan je
simpelweg het volgende commando draaien: `brew install openjdk`

Nadat je Java en CoreNLP hebt geïnstalleerd moet je in een terminal naar de
lokatie gaan waar je CoreNLP heb gedownload. Vervolgens kan je het onderstaande
commando draaien om een server te starten op port `9000`:

```
java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -annotators "tokenize,ssplit,parse" -port 9000 -timeout 30000
```


Vervolgens kan je het project lokaal uitvoeren middels:

```
./main.py ./foxinsocks.txt ./homophones.txt
```

Optioneel kan je nog een getal opgeven hoeveel zinnen het moet genereren. Om
50 zinnen te genereren, gebruik het volgende commando:

```
./main.py ./foxinsocks.txt ./homophones.txt 50
```

Voor meer uitleg over het gebruik van de `main.py`, de structuur is als volgt:

```
./main.py FILEPATH1 FILEPATH2 N
```

- `FILEPATH1` is een pad naar een corpus bestand dat gebuikt wordt voor de
  phrase structure rules. In dit project is dat `foxinsocks.txt`
- `FILEPATH2` is een pad naar een woordenlijst dat wordt gebruikt voor de
  lexical rules. In dit project is dat `homophones.txt`
- `N` een getal dat aangeeft hoeveel zinnen er gegenereerd moeten worden.

Voor dit project kan je dus simpelweg het volgend commando runnen:

# Authors

Gemaakt door Kim Koomen and Gijs Schouten als opdracht vanuit de Universiteit
van Amsterdam, 2023.

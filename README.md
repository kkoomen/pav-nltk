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

Nadat je CoreNLP hebt geïnstalleerd moet je in een terminal naar de lokatie gaan
waar je CoreNLP heb gedownload. Vervolgens kan je het onderstaande commando
draaien om een server te starten op port `9000`:

```
java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -annotators "tokenize,pos,parse" -port 9000 -timeout 30000
```


Vervolgens kan je het project lokaal uitvoeren middels:

```
./main.py ./foxinsocks.txt ./homophones.txt
```

Voor meer uitleg over het gebruik van de `main.py`, de structuur is als volgt:

```
./main.py FILEPATH1 FILEPATH2
```

- `FILEPATH1` is een pad naar een corpus bestand dat gebuikt wordt voor de
  phrase structure rules. In dit project is dat `foxinsocks.txt`
- `FILEPATH2` is ene pad naar een woordenlijst dat wordt gebruikt voor de
  lexical rules. In dit project is dat `homophones.txt`

Voor dit project kan je dus simpelweg het volgend commando runnen:

# Authors

Gemaakt door Kim Koomen and Gijs Schouten als opdracht vanuit de Universiteit
van Amsterdam, 2023.

# -*- coding: utf-8 -*-

import sys
import codecs
import nltk
from nltk import bigrams

#Raccolgo qui tutte le POS del corpus
def AnnotazioneLinguistica(frasi):
	tokensPOSTot = []
	tokensTOT = []
	for frase in frasi:
		tokens = nltk.word_tokenize(frase)
		tokensPOS = nltk.pos_tag(tokens)
		tokensPOSTot = tokensPOSTot + tokensPOS
	return tokensPOSTot


#Perndo in input il risultato della funzione AnnotazioneLinguistica ed estraggo il secondo elemento delle tupla, che contiene il POS Tag assegnatogli.
def EstraiSequenzaPOS(TestoAnalizzatoPOS):
	listaPOS = []
	for bigramma in TestoAnalizzatoPOS:
		listaPOS.append(bigramma[1])
	return listaPOS

#Raccolgo qui tutti i verbi, nomi, avverbi e aggettivi per calcolarmi la densità lessicale
def Densita1(SequenzaPOS):
	sos = 0
	ver = 0
	avv = 0
	agg = 0

	for element in SequenzaPOS:
		if element == ("NN" or "NNS" or "NP" or "NPS"):
			sos = sos + 1
		if element == ("VB" or "VBD" or "VBG" or "VBN" or "VBN" or "VBP" or "VBZ"):
			ver = ver + 1
		if element == ("RB" or "RBR" or "RBS"):
			avv = avv + 1
		if element == ("JJ" or "JJR" or "JJS"):
			agg = agg + 1

	den1 = sos + ver + avv + agg

	return den1

#Raccolgo qua i token che hanno un POS di tipo . o , per calcolarmi, in seguito, la densità lessicale
def Densita2(SequenzaPOS):
	tot = 0
	pun = 0
	vir = 0

	for element in SequenzaPOS:
		if element == ".":
			pun = pun + 1
		if element == ",":
			vir = vir + 1
		tot = tot + 1

	punvir = pun + vir
	den2 = float(tot)-float(punvir)

	return den2

#Dopo aver raccolto tutte le POS, adesso conto quanti sono nomi e quanti sono verbi: dividendo, ottengo il rapporto Sostantivi/verbi
def RappostoSosVer(SequenzaPOS):
	n = 0
	v = 0
	for element in SequenzaPOS:
		if element == ("NN" or "NNS" or "NP" or "NPS"):
			n = n + 1
		if element == ("VB" or "VBD" or "VBG" or "VBN" or "VBN" or "VBP" or "VBZ"):
			v = v + 1

	rap = float(n)/float(v)

	return rap


#Calcolo la TTR
def TypeTokenRatio(frasi):
	corpus = []
	for frase in frasi:
		tokens = nltk.word_tokenize(frase)
		corpus = corpus + tokens
	
	corpusMille = corpus[0:1000] #prendo in considerazione tutte le parole unità che vanno dall'indice 0 a 1000
	vocaboMille = set(corpusMille) #creo un vocabolario eliminando le copie delle parole unità

	ttr = float(len(vocaboMille))/float(len(corpusMille))

	return ttr

#Calcolo la cardinalità del vocabolario
def GrandezzaVocabolario(frasi):
	corpus = []
	for frase in frasi:
		tokens = nltk.word_tokenize(frase)
		corpus = corpus + tokens
	prepVoc = set(corpus) #usando set() posso eliminare i doppioni delle parole unità e ottenere così i types del corpus
	vocabolario = len(prepVoc) #calcolo quanti valori mi sono rimasti dopo aver eliminato i doppioni.
	return vocabolario

#Calcolo la lunghezza media delle frasi nel corpus
def CalcolaLunghezzaMediaFrasi(frasi):
	numeroFrasi = 0.0
	numeroTokenPerFrase = 0.0
	for frase in frasi:
		numeroFrasi = numeroFrasi + 1
		tokens = nltk.word_tokenize(frase)
		numeroTokenPerFrase = numeroTokenPerFrase + len(tokens)

	mediaAritmetica = numeroTokenPerFrase/numeroFrasi
	return mediaAritmetica

#Calcolo la lunghezza deli token nelle frasi, contando il numero di token nelle frasi
def CalcolaLunghezzaToken(frasi):
	lunghezzaTOT = 0.0
	for frase in frasi:
		tokens = nltk.word_tokenize(frase)
		lunghezzaTOT = lunghezzaTOT + len(tokens)
	return lunghezzaTOT


#Funzione principale
def main(file1, file2):

	fileInput1 = codecs.open(file1, "r", "utf-8")
	fileInput2 = codecs.open(file2, "r", "utf-8")

	raw1 = fileInput1.read()
	raw2 = fileInput2.read() 

	sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

	frasi1 = sent_tokenizer.tokenize(raw1)
	frasi2 = sent_tokenizer.tokenize(raw2)

	lunghezzaToken1 = CalcolaLunghezzaToken(frasi1)
	lunghezzaToken2 = CalcolaLunghezzaToken(frasi2)

	media1 = CalcolaLunghezzaMediaFrasi(frasi1)
	media2 = CalcolaLunghezzaMediaFrasi(frasi2)

	voc1 = GrandezzaVocabolario(frasi1)
	voc2 = GrandezzaVocabolario(frasi2)

	ttr1 = TypeTokenRatio(frasi1)
	ttr2 = TypeTokenRatio(frasi2)

	TestoAnalizzatoPOS1 = AnnotazioneLinguistica(frasi1)
	TestoAnalizzatoPOS2 = AnnotazioneLinguistica(frasi2)

	SequenzaPOS1 = EstraiSequenzaPOS(TestoAnalizzatoPOS1)
	SequenzaPOS2 = EstraiSequenzaPOS(TestoAnalizzatoPOS2)

	rap1 = RappostoSosVer(SequenzaPOS1)
	rap2 = RappostoSosVer(SequenzaPOS2)

	medioden1 = Densita1(SequenzaPOS1)
	medioden2 = Densita1(SequenzaPOS2)

	epiden1 = Densita2(SequenzaPOS1)
	epiden2 = Densita2(SequenzaPOS2)

	densitaTOT1 = float(medioden1)/float(epiden1)
	densitaTOT2 = float(medioden2)/float(epiden2)


	print ""

	print "-- Inizio del programma finale1.py --"

	print ""

	print "Il file", file1, "e' lungo", lunghezzaToken1, "tokens"
	print "Il file", file2, "e' lungo", lunghezzaToken2, "tokens"

	print ""

	if lunghezzaToken1>lunghezzaToken2:
		print "Il file", file1, "contiene un numero di token maggiore rispetto al file", file2
	elif lunghezzaToken1<lunghezzaToken2:
		print "Il file", file2, "contiene un numero di token maggiore rispetto al file", file1
	else:
		print "i due file hanno la stessa lunghezza in termini di token."

	print ""


	print "-------"

	print ""

	print "La lunghezza media delle frasi del file", file1, "e' pari a: ", media1
	print "La lunghezza media delle frasi del file", file2, "e' pari a: ", media2

	print ""

	if media1>media2:
		print "La lunghezza media delle frasi del", file1, "è maggiore rispetto a quelle contenute", file2
	elif media1<media2:
		print "La lunghezza media delle frasi del", file2, "è maggiore rispetto a quelle contenute", file1
	else:
		print "La lunghezza media delle frasi dei due file sono identici"

	print ""

	print "-------"

	print ""

	print "Il file", file1, "ha un vocabolario che conta", voc1, "type"
	print "Il file", file2, "ha un vocabolario che conta", voc2, "type"

	print ""

	if voc1>voc2:
		print "Il vocabolario del file", file1, "è più grande rispetto a quello del file", file2
	elif voc1<voc2:
		print "Il vocabolario del file", file2, "è più grande rispetto a quello del file", file1
	else:
		print "Entrambi i vocabolari hanno la stessa quantità di types."

	print ""

	print "-------"

	print ""

	print "Il corpus (primi 1000 token) del file", file1, "ha una ricchezza lessicale, misurata in TTR, pari a --->", ttr1
	print "Il corpus (primi 1000 token) del file", file2, "ha una ricchezza lessicale, misurata in TTR, pari a --->", ttr2

	print ""

	if ttr1>ttr2:
		print "Il coprus del file", file1, "ha una ricchezza lessicale maggiore rispetto a quella del file", file2
	elif ttr2>ttr1:
		print "Il coprus del file", file2, "ha una ricchezza lessicale maggiore rispetto a quella del file", file1
	else:
		print "Entrambi i corpus hanno la medesima ricchezza lessicale"


	print ""

	print "-------"

	print ""

	print "Il rapporto Sostantivi/Verbi del file", file1, "e' pari a --->", rap1
	print "Il rapporto Sostantivi/Verbi del file", file2, "e' pari a --->", rap2

	print ""

	if rap1>rap2:
		print "Il rapporto Sos/Ver del file", file1, "è maggiore rispetto al rapporto del file", file2
	elif rap1<rap2:
		print "Il rapporto Sos/Ver del file", file2, "è maggiore rispetto al rapporto del file", file1


	print ""

	print "-------"

	print ""

	print "La densità lessicale del file", file1, "corrisponde a --->", densitaTOT1
	print "La densità lessicale del file", file2, "corrisponde a --->", densitaTOT2

	print ""

	if densitaTOT1>densitaTOT2:
		print "La densità lessicale del file", file1, "è maggiore rispetto a quella del file", file2
	elif densitaTOT2>densitaTOT1:
		print "La densità lessicale del file", file2, "è maggiore rispetto a quella del file", file1

	print ""

	print "-- Fine del programma finale1.py --"

	print ""


main(sys.argv[1], sys.argv[2])

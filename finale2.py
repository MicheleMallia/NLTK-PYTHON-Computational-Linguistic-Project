# -*- coding: utf-8 -*-

import sys
import codecs
import nltk
import math
from nltk import bigrams

#Ordina gli elementi del dizionario
def Ordina(dict):
	return sorted(dict.items(), key=lambda x: x[1], reverse=True)


#Ottengo le prime 10 POS più frequenti, prendendo in input la distribuzione di frequenza delle POS
def DieciPOS(DistFreqPos):
	contatore = 0
	for elem in DistFreqPos:
		print "\t", elem, "-----frequenza:", DistFreqPos[elem]
		contatore = contatore + 1
		if contatore == 10:break
	

#Qui stampo i primi venti token, in base alla frequenza, ordinati in maniera decrescente
def StampaVenti(DistribuzioneDiFrequenza):

	contatore = 0
	for elem in DistribuzioneDiFrequenza:
		print "\t", elem, "-----frequenza:", DistribuzioneDiFrequenza[elem]
		contatore = contatore + 1
		if contatore == 20 : break


#Calcolo qui la Local Mutual Information, prendendo in input i bigrammi composti solamente da
#aggettivi e sostantivi e TokenTOT(corpus) per calcolarmi la frequenza

def LocalMutualInfo(bigrammaAggSos, tokensTOT):
	Dizionario= {}
	corpus = len(tokensTOT)
	TypeBigrammaAggSos = set(bigrammaAggSos)

	for bigramma in TypeBigrammaAggSos:
		u = bigramma[0][0]
		v = bigramma[1][0]
		frequenza=bigrammaAggSos.count(bigramma)		
		mutual =  ((float(frequenza))/((float(tokensTOT.count(u)))*(float(tokensTOT.count(v)))))*float(corpus)
		info = math.log(mutual, 2)
		localMutuInf = frequenza * info
		Dizionario[bigramma]=localMutuInf

	return Dizionario

#Calcolo qui la catena di markov per individuare la frase con maggiore probabilità
def CalcolaOrdineMarkov1(lunghezzaCorpus, DistribuzioneDiFrequenza, frase, bigrammi):
	index = 1
	probabilita=1.0
	parInit = frase[0]
	probabilitaToken=(DistribuzioneDiFrequenza[parInit]*1.0/lunghezzaCorpus*1.0)
	analizza=True
	for tok in frase:
		if DistribuzioneDiFrequenza[tok]<2:
			analizza=False
	if analizza==True:
		for tok in frase:
			par0 = frase[index-1]
			par1 = frase[index]
			if index < len(frase):
				probabilitaOrdineUno=(((bigrammi.count((par0, par1)))*1.0)/DistribuzioneDiFrequenza[par0]*1.0)
				probabilita=probabilita*probabilitaOrdineUno
			else:
				index=index+1
		probFinal= probabilitaToken*probabilita
	else:
		probFinal=0.0
	return probFinal

#L'analisi linguistica mi servirà per estrarre le informazioni dal testo
def AnalisiLinguistica(frasi):
	tokensTOT=[]
	NamedEntityList=[]
	tokensPOSTot=[]
	nodes=[]
	for frase in frasi:
		tokens=nltk.word_tokenize(frase)
		tokensPOS=nltk.pos_tag(tokens)
		analisi=nltk.ne_chunk(tokensPOS)
		for nodo in analisi:
			NE=''
			if hasattr(nodo, 'node'):
				if nodo.node in ["PERSON", "GPE", "ORGANIZATION"]:
					nodes.append(nodo.node)
					for partNE in nodo.leaves():
						NE=NE+' '+partNE[0]
					NamedEntityList.append(NE)
		tokensTOT = tokensTOT + tokens
		tokensPOSTot = tokensPOSTot + tokensPOS
	Persone = []
	Luoghi = []
	index = 0

	for elem in nodes:
		if elem == "PERSON":
			Persone.append(NamedEntityList[index])
		if elem == "GPE":
			Luoghi.append(NamedEntityList[index])
		index = index+1
	

	return Persone, Luoghi	


#Ordino qua le Named Entity estratte con la funzione qui sopra
def NamedEntityOrdinate(persFreq, luogFreq, fille):

	print ""
	
	print "Lista dei nomi propri di persona (PERSON) del file", fille,"ordinati per frequenza:"
	print ""
	for elep in persFreq:
		print "\t La parola:", elep,"ha frequenza --->", persFreq[elep]


	print ""


 	print "Lista dei nomi propri di luogo (GPE) del file", fille,"ordinati per frequenza:"
 	print ""
 	for elel in luogFreq:
 		print "\t La parola:", elel,"ha frequenza --->", luogFreq[elel]



def CalcolaFrequenzaBigramma(bigrammaAggSos):
	Dizionario={}
	TypeBigrammaAggSos = set(bigrammaAggSos)
	for bigramma in TypeBigrammaAggSos:
		frequenza=bigrammaAggSos.count(bigramma)
		Dizionario[bigramma]=frequenza
	return Dizionario


#Creo il vettore composto da aggettivi e sostantivi
def SoloAggSos(TestoAnalizzatoPOS, corpus):
	BigrammiEstratti=[]
	bigrammaTokPOS = bigrams(TestoAnalizzatoPOS)
	for bigramma in bigrammaTokPOS:
		if((bigramma[0][1] in ["JJ", "JJR", "JJS"]) and (bigramma[1][1] in ["NNP", "NNPS", "NN", "NNS", "NP", "NPS"]) and (corpus.count(bigramma[0][0])>2) and (corpus.count(bigramma[1][0])>2)):
			BigrammiEstratti.append(bigramma)
	return BigrammiEstratti


#Creo il vettore con tutte le sequenze di POS
def EstraiSequenzaPOS(TestoAnalizzatoPOS):
	listaPOS = []
	for bigramma in TestoAnalizzatoPOS:
		listaPOS.append(bigramma[1])
	return listaPOS

def AnnotazioneLinguistica(frasi):
	tokensPOSTot = []
	for frase in frasi:
		tokens = nltk.word_tokenize(frase)
		tokensPOS = nltk.pos_tag(tokens)
		tokensPOSTot = tokensPOSTot + tokensPOS
	return tokensPOSTot


def EstraiTestoTokenizzato(frasi):
	tokensTOT = []
	for frase in frasi:
		tokens = nltk.word_tokenize(frase)
		tokensTOT = tokensTOT + tokens
	return tokensTOT		
	
def main(file1, file2):

	fileInput1 = codecs.open(file1, "r", "utf-8")
	fileInput2 = codecs.open(file2, "r", "utf-8")
	raw1 = fileInput1.read()
	raw2 = fileInput2.read()
	sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

	frasi1 = sent_tokenizer.tokenize(raw1)
	frasi2 = sent_tokenizer.tokenize(raw2)

	TestoTokenizzato1 = EstraiTestoTokenizzato(frasi1)
	TestoTokenizzato2 = EstraiTestoTokenizzato(frasi2)
	bigrammi1 = bigrams(TestoTokenizzato1)
	bigrammi2 = bigrams(TestoTokenizzato2)

	DistribuzioneDiFrequenza1 = nltk.FreqDist(TestoTokenizzato1)
	DistribuzioneDiFrequenza2 = nltk.FreqDist(TestoTokenizzato2)

	TestoAnalizzatoPOS1 = AnnotazioneLinguistica(frasi1)
	TestoAnalizzatoPOS2 = AnnotazioneLinguistica(frasi2)

	SequenzaPOS1 = EstraiSequenzaPOS(TestoAnalizzatoPOS1)
	SequenzaPOS2 = EstraiSequenzaPOS(TestoAnalizzatoPOS2)

	DistFreqPos1 = nltk.FreqDist(SequenzaPOS1)
	DistFreqPos2 = nltk.FreqDist(SequenzaPOS2)

	soloAgg1 = SoloAggSos(TestoAnalizzatoPOS1, TestoTokenizzato1)
	soloAgg2 = SoloAggSos(TestoAnalizzatoPOS2, TestoTokenizzato2)

	DizionarioBig1 = CalcolaFrequenzaBigramma(soloAgg1)
	DizionarioBig2 = CalcolaFrequenzaBigramma(soloAgg2)

	DizionarioFreq1 = LocalMutualInfo(soloAgg1, TestoTokenizzato1)
	DizionarioFreq2 = LocalMutualInfo(soloAgg2, TestoTokenizzato2)

	ListaTuplaFreq1 = Ordina(DizionarioFreq1)
	ListaTuplaFreq2 = Ordina(DizionarioFreq2)

	ListaTupla1 = Ordina(DizionarioBig1)
	ListaTupla2 = Ordina(DizionarioBig2)

	DistFreqBig1 = nltk.FreqDist(soloAgg1)
	DistFreqBig2 = nltk.FreqDist(soloAgg2)

	lunghezzaCorpus1 = len(TestoTokenizzato1)
	lunghezzaCorpus2 = len(TestoTokenizzato2)

	print ""

	print "-- Inizio del programma finale2.py --"

	print ""

	print "Stampo i primi venti token del file", file1, "con relativa frequenza:"

	print ""

	StampaVenti(DistribuzioneDiFrequenza1)

	print ""

	print "Stampo i primi venti token del file", file2, "con relativa frequenza:"

	print ""

	StampaVenti(DistribuzioneDiFrequenza2)

	print ""

	print "-------"

	print "" 

	print "Stampo i primi dieci PoS (Part-of-Speech) del file", file1, "con relativa frequenza:"

	print

	DieciPOS(DistFreqPos1)

	print

	print "Stampo i primi dieci PoS (Part-of-Speech) del file", file2, "con relativa frequenza:"

	print 

	DieciPOS(DistFreqPos2)

	print ""

	print "-------"

	print ""
	
	print "Stampa i primi dieci bigrammi del file", file1, ",composti da Aggettivi e Sostantivi con frequenza maggiore di due e ordinati in base alla frequenza decrescente, con relativa frequenza:"

	print
    
    #la variabile contatore mi permette di avere tutto sotto controllo: la maggiorparte del lavoro è fatto dal for qua sotto; l'azione si ripete per quasi tutte le invocazioni di funzione
	contatore1= 0
	for tupla1 in ListaTupla1:
		print "\t bigramma -->", tupla1[0][0][0], tupla1[0][1][0],"-->",  tupla1[1]
		contatore1= contatore1+1
		if contatore1==10:break

	print

	print "Stampa i primi dieci bigrammi del file", file2, ",composti da Aggettivi e Sostantivi con frequenza maggiore di due e ordinati in base alla frequenza decrescente, con relativa frequenza:"

	print

	contatore2= 0
	for tupla2 in ListaTupla2:
		print "\t bigramma -->", tupla2[0][0][0], tupla2[0][1][0],"-->",  tupla2[1]
		contatore2= contatore2+1
		if contatore2==10:break

	print ""

	print "-------"

	print ""


	print "Stampa i primi dieci bigrammi del file", file1, ",composti da Aggettivi e Sostantivi con frequenza maggiore di due e ordinati in base alla forza associativa (calcolata in termini di Local Mutual Information), con relativa forza associativa:"

	print

	contatore3= 0
	for tupla3 in ListaTuplaFreq1:
		print "\t bigramma -->", tupla3[0][0][0], tupla3[0][1][0],"-->",  tupla3[1]
		contatore3= contatore3+1
		if contatore3==10:break

	print

	print "Stampa i primi dieci bigrammi del file", file2, ",composti da Aggettivi e Sostantivi con frequenza maggiore di due e ordinati in base alla forza associativa (calcolata in termini di Local Mutual Information), con relativa forza associativa:"

	print

	contatore4= 0
	for tupla4 in ListaTuplaFreq2:
		print "\t bigramma -->", tupla4[0][0][0], tupla4[0][1][0],"-->",  tupla4[1]
		contatore4= contatore4+1
		if contatore4==10:break

	print ""

	print "-------"

	print ""

	probMAX1 = 0.0
	for frase1 in frasi1:
	
		tokensFrase1 = nltk.word_tokenize(frase1) #vettore contenente tutti i token di ciascuna frase presente nel corpus
		if len(tokensFrase1)>8: #se la frase contiene piu' di otto token, puo' passare all'analisi delle probabilita'

			Probabilita1=CalcolaOrdineMarkov1(lunghezzaCorpus1, DistribuzioneDiFrequenza1, tokensFrase1, bigrammi1)
			
			if Probabilita1>probMAX1:
				probMAX1=Probabilita1
				fraseMAX1=frase1

	print "\t La frase --->", fraseMAX1, "<--- del file", file1,", ha la probabilita massima, che corrisponde a:", probMAX1

	print 

	probMAX2=0.0
	for frase2 in frasi2:
	
		tokensFrase2 = nltk.word_tokenize(frase2)

		if len(tokensFrase2)>8:

			Probabilita2=CalcolaOrdineMarkov1(lunghezzaCorpus2, DistribuzioneDiFrequenza2, tokensFrase2, bigrammi2)
			

			if Probabilita2 > probMAX2:
				probMAX2=Probabilita2
				fraseMAX2=frase2


	print "\t La frase --->", fraseMAX2, "<--- del file", file2,", ha la probabilita massima, che corrisponde a:", probMAX2

	print ""

	print "-------"

	print ""

	PersoLuog1=AnalisiLinguistica(frasi1)

	pers1 = PersoLuog1[0]
	luog1 = PersoLuog1[1]

	pers1Freq = nltk.FreqDist(pers1)
	luog1Freq = nltk.FreqDist(luog1)

	pers1Div = set(pers1)
	luog1Div = set(luog1)
	
	NamedEntityOrdinate(pers1Freq, luog1Freq, file1)

	print ""

	print "------------------------------------------------------"

	print ""

	PersoLuog2=AnalisiLinguistica(frasi2)

	pers2 = PersoLuog2[0]
	luog2 = PersoLuog2[1]

	pers2Freq = nltk.FreqDist(pers2)
	luog2Freq = nltk.FreqDist(luog2)

	pers2Div = set(pers2)
	luog2Div = set(luog2)

	NamedEntityOrdinate(pers2Freq, luog2Freq, file2)

	print ""

	print "-------"

	print "-- Fine del programma finale2.py --"

	print "" 

main(sys.argv[1], sys.argv[2])

# Simulazione Monte Carlo di uno Sciame Elettromagnetico  

## Descrizione del progetto

In questo progetto si sviluppa una simulazione Monte Carlo dello sviluppo di uno sciame elettromagnetico in un materiale, utilizzando un modello semplificato derivato da quello di Rossi.

L’obiettivo è riprodurre l’evoluzione longitudinale dello sciame e studiare l’energia depositata per ionizzazione.

---

## Parametri di ingresso

La simulazione consente di selezionare i seguenti parametri fisici:

- Energia iniziale della particella primaria  

- Energia critica del materiale  

- Perdita media di energia per ionizzazione in una lunghezza di radiazione  

- Passo di avanzamento della simulazione  
  s ∈ [0,1]  
  espresso come frazione della lunghezza di radiazione.

---

## Dinamica dello sciame

Ad ogni step di ampiezza s X₀, si applicano le seguenti regole:


- Un elettrone o positrone con energia  
  E > dE_X0 · s  
  perde per ionizzazione:  
  ΔE_ion = dE_X0 · s

- Un elettrone o positrone con  
  E > E_c  
  ha probabilità  
  P_brem = 1 − e^(−s)  
  di emettere un fotone di bremsstrahlung.
 
- Un fotone con  
  E > 2 m_e c²  
  ha probabilità  
  P_pair = 1 − e^(−7/9 s)  
  di interagire per produzione di coppia.

- Un elettrone o positrone con  
  E ≤ dE_X0 · s  
  deposita un’energia casuale nell’intervallo [0, E]  
  e viene escluso dal successivo sviluppo dello sciame.

- Un fotone con  
  E ≤ 2 m_e c²  
  deposita un’energia casuale nell’intervallo [0, E]  
  e viene escluso dal successivo sviluppo dello sciame.

La simulazione termina quando non sono più presenti particelle in grado di depositare energia o di interagire.

---

## Output della simulazione

Il programma fornisce:

- Energia totale persa per ionizzazione nel materiale;
- Numero di particelle presenti nello sciame ad ogni step;
- Energia persa per ionizzazione ad ogni step.

---

La simulazione viene utilizzata per studiare:

- Lo sviluppo longitudinale dello sciame;
- L’andamento dell’energia depositata per ionizzazione;

in funzione dell’energia iniziale E₀, per i seguenti materiali:

- Acqua liquida
- Ioduro di Cesio 

---

## Librerie
- matplotlib.pyplot 
- cmath
- pandas 
- numpy 
- time
- tqdm 


## Output

La funzione principale del programma restituisce 2 file PNG:

- "sviluppo_longitudinale.png"
   Contiene quattro pannelli con lo sviluppo longitudinale e l’energia ionizzata per step nei due materiali.

- "energia_totale_vs_E0.png"
   Contiene un pannello con l’energia ionizzata totale nei due materiali.

## Struttura del progetto

- simulazione.py
  Contiene la classe Simulazione che permette l'evoluzione dello sciame. Se chiamata direttamente nel terminale avvia un test della classe
  dove in input vengono richiesti tutti i parametri necessari all'evoluzione e in output viene restituito il dataframe passo passo dello 
  sciame insieme al tempo di esecuzione del programma.
	
- main.py
  Contiene lo studio dei materiali Acqua liquida e Ioduro di Cesio. Richiede in input lo step e il numero di iterazioni delle simulazioni 
  Montecarlo. In output restituisce i due grafici.


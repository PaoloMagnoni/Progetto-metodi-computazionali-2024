import matplotlib.pyplot as plt
import cmath
import pandas as pd
import numpy as np
import time
from tqdm import tqdm
from simulazione import Simulazione


#FUNZIONE RUNNARE SIMULAZIONI
def run_sim(e0,n_iter, step, materiale):
	"""
    Esegue un insieme statistico di simulazioni Monte Carlo dello sviluppo
    longitudinale di uno sciame elettromagnetico per diverse energie iniziali
    dell'elettrone incidente in un certo materiale.

    Parametri
    ----------
    e0 : array
        Insieme delle energie iniziali dell’elettrone incidente (in MeV).
    n_iter : int
        Numero di simulazioni indipendenti per ciascuna energia.
    step : float
        Passo della simulazione (frazione lunghezza di radiazione).
    materiale : list
        Parametri del materiale: energia critica, energia di ionizzazione e nome del materiale.

    Restituisce
    -------
    av_activep_tuple : lista di array
        Media del numero di particelle attive per ciascuna energia iniziale.
    stderr_activep_tuple : lista di array
        Errore standard del numero di particelle attive per step.
    enionxstep_tuple : lista di array
        Media dell’energia ionizzata per step.
    stderr_enionxstep_tuple : lista di array
        Errore standard dell’energia ionizzata per step.
    max_step_tuple : lista di int
        Numero massimo di step simulati per ciascuna energia iniziale.
	av_tot_enion_tuple : lista di float
        Media dell’energia ionizzata totale.
    stderr_tot_enion_tuple : lista di float
		Errore standard dell’energia ionizzata totale.
    """
	av_activep_tuple = []
	stderr_activep_tuple = []
	max_step_tuple = []
	enionxstep_tuple=[]
	stderr_enionxstep_tuple = []
	av_tot_enion_tuple=[]
	stderr_tot_enion_tuple=[]
	for i in e0:
		activeparticles=[]
		enionxstep=[]
		tot_enion=[]
		sim=Simulazione(i, materiale)
		for f in tqdm(range(n_iter), desc=f"Simulazioni {materiale[2]}: energia iniziale {i} MeV ", unit="iter"):
			df, tot_e=sim.stepxstep(step)
			activeparticles.append(df['Numero di particelle attive'])
			enionxstep.append(df['Energia ionizzata nello step'])
			tot_enion.append(tot_e)
		max_step = max(len(s) for s in activeparticles)
		filled_list_activep = [s.reindex(range(max_step), fill_value=0) for s in activeparticles]
		arr_activep=np.array([s.values for s in filled_list_activep])    #s.values prende i dati della serie come array 
		av_activep=np.mean(arr_activep,axis=0)
		std_per_step = np.std(arr_activep, axis=0, ddof=1)
		stderr_activep = std_per_step / np.sqrt(n_iter)
	
		filled_list_enion = [s.reindex(range(max_step), fill_value=0) for s in enionxstep]
		arr_enion=np.array([s.values for s in filled_list_enion])    #s.values prende i dati della serie come array 
		av_enion=np.mean(arr_enion,axis=0)
		std_enion = np.std(arr_enion, axis=0, ddof=1)
		stderr_enion = std_enion / np.sqrt(n_iter)
		
		av_tot_enion=np.mean(tot_enion)
		std_tot_enion = np.std(tot_enion, ddof=1)
		stderr_tot_enion = std_tot_enion / np.sqrt(n_iter)
		
		av_activep_tuple.append(av_activep)
		stderr_activep_tuple.append(stderr_activep)
		enionxstep_tuple.append(av_enion)
		stderr_enionxstep_tuple.append(stderr_enion)
		max_step_tuple.append(max_step)
		av_tot_enion_tuple.append(av_tot_enion)
		stderr_tot_enion_tuple.append(stderr_tot_enion)
	return av_activep_tuple, stderr_activep_tuple, enionxstep_tuple, stderr_enionxstep_tuple, max_step_tuple, av_tot_enion_tuple, stderr_tot_enion_tuple

if __name__ == "__main__":
	"""
	Il codice esegue uno studio Monte Carlo dello sviluppo longitudinale
	di uno sciame elettromagnetico generato da un elettrone incidente
	in due materiali differenti: acqua liquida e ioduro di cesio.

	Input utente
	-------
	-n_iter : numero di simulazioni Monte Carlo indipendenti
	-step   : frazione della lunghezza di radiazione 

	Produzione dei grafici
	-------
	-Sviluppo longitudinale medio del numero di particelle attive per diverse energie iniziali.

	-Energia ionizzata media per step.

	-Energia totale ionizzata in funzione dell’energia iniziale

	Vengono salvati due file:

	   - "sviluppo_longitudinale.png"
	     Contiene quattro pannelli con lo sviluppo longitudinale e l’energia ionizzata per step nei due materiali.

	   - "energia_totale_vs_E0.png"
	"""
	# Messaggio inizio

	print("\nStudio della propagazione di uno sciame elettromagnetico in Acqua liquida e Ioduro di Cesio \n\nL'utente deve inserire il numero di iterazioni delle simulazioni e lo step delle simulazioni. Il numero delle iterazioni va a definire l'insieme statistico delle simulazioni, un numero maggiore diminuirà l'errore nelle medie finali ma aumenterà il tempo di esecuzione del codice. \nLe simulazioni sono fatte per 5 differenti energie iniziali dell'elettrone entrante.")

	# Costanti

	acqua=[78.33, 1.981, 'acqua liquida']
	csi=[11.17,5.605, 'ioduro di cesio']
	energie = np.linspace(10000, 100000, 5)
	colors = ['r', 'g', 'b', 'orange', 'purple']

	# Input utente

	n_iter=int(input("Inserisci il numero di iterazioni delle simulazioni: "))
	step=float(input("Inserisci il passo della simulazione: "))
	
	#RUN
	csi_av_activep_tuple, csi_stderr_activep_tuple, csi_enionxstep_tuple, csi_stderr_enionxstep_tuple, csi_max_step_tuple, csi_av_tot_enion_tuple, csi_stderr_tot_enion_tuple = run_sim(energie, n_iter, step, csi)
	wat_av_activep_tuple, wat_stderr_activep_tuple, wat_enionxstep_tuple, wat_stderr_enionxstep_tuple, wat_max_step_tuple, wat_av_tot_enion_tuple, wat_stderr_tot_enion_tuple = run_sim(energie, n_iter, step, acqua)
	
	fig, axs = plt.subplots(2, 2, figsize=(14,10))
	csi_labels = [f'CsI E_0: {energie[i]} MeV' for i in range(5)]
	wat_labels = [f'Acqua E_0: {energie[i]} MeV' for i in range(5)]

	for i in range(5):

		axs[0,0].errorbar(x=np.arange(csi_max_step_tuple[i]), y=csi_av_activep_tuple[i], yerr=csi_stderr_activep_tuple[i], fmt='-o', color=colors[i],  ecolor=colors[i],markersize=4, elinewidth=1, capsize=3, label=csi_labels[i])
		axs[1,0].errorbar(x=np.arange(csi_max_step_tuple[i]), y=csi_enionxstep_tuple[i], yerr=csi_stderr_enionxstep_tuple[i], fmt='-o',color=colors[i], ecolor=colors[i],markersize=4, elinewidth=1, capsize=3, label=csi_labels[i])
		axs[0,1].errorbar(x=np.arange(wat_max_step_tuple[i]), y=wat_av_activep_tuple[i], yerr=wat_stderr_activep_tuple[i], fmt='-o',color=colors[i], ecolor=colors[i],markersize=4, elinewidth=1, capsize=3, label=wat_labels[i])
		axs[1,1].errorbar(x=np.arange(wat_max_step_tuple[i]), y=wat_enionxstep_tuple[i], yerr=wat_stderr_enionxstep_tuple[i], fmt='-o',color=colors[i], ecolor=colors[i],markersize=4, elinewidth=1, capsize=3, label=wat_labels[i])
	axs[0,0].set_title('Sviluppo longitudinale CsI')
	axs[1,0].set_title('Energia ionizzata vs step CsI')
	axs[0,1].set_title('Sviluppo longitudinale Acqua')
	axs[1,1].set_title('Energia ionizzata vs step Acqua')

	for ax in axs.flat:
		ax.set_xlabel('step (frazione di X₀)')
		ax.grid(alpha=0.3)
		ax.legend()

	axs[0,0].set_ylabel('Numero particelle attive')
	axs[0,1].set_ylabel('Numero particelle attive')
	axs[1,0].set_ylabel('Energia ionizzata')
	axs[1,1].set_ylabel('Energia ionizzata')

	plt.tight_layout()
	plt.savefig("sviluppo_longitudinale.png", dpi=150)
	plt.show()
	
	
	plt.figure(figsize=(8,6))
	plt.errorbar(energie, csi_av_tot_enion_tuple, yerr=csi_stderr_tot_enion_tuple, fmt='-o', color='r', label='CsI')
	plt.errorbar(energie, wat_av_tot_enion_tuple, yerr=wat_stderr_tot_enion_tuple, fmt='-o',color='b', label='Acqua')

	plt.xlabel('Energia iniziale E₀ (MeV)')
	plt.ylabel('Energia totale ionizzata (MeV)')
	plt.title('Energia ionizzata totale vs energia iniziale')
	plt.grid(alpha=0.3)
	plt.legend()

	plt.tight_layout()
	plt.savefig("energia_totale_vs_E0.png", dpi=150)
	plt.show()

	# Messaggio fine
	print('Fatto! I grafici sono stati salvati nella cartella.')

import matplotlib.pyplot as plt
import cmath
import pandas as pd
import numpy as np
import time


class Simulazione:
	"""
	
	Simulazione Monte Carlo di uno sciame elettromagnetico.
	
	Parametri
    ----------
    en_i : float
        Energia (MeV) iniziale della particella primaria.
    materiale : lista float contenente:
            E_c : energia critica del materiale
            E_i : energia di ionizzazione per unità di step
        Se None, i valori vengono richiesti da input.


    Attributi
    ----------
    ec : float
        Energia critica del materiale.
    ei : float
        Energia di ionizzazione.
    elettroni : array numpy
        Array contenente le energie degli elettroni/positroni attivi.
    fotoni : array numpy
        Array contenente le energie dei fotoni attivi.
    tot_ion : float
        Energia totale depositata per ionizzazione.
	"""
	
	def __init__(self, en_i, materiale=None):
		#CONDIZIONI INIZIALI
		self.in_elettroni = np.array([en_i])
		self.in_fotoni = np.array([])
		self.in_tot_ion = 0
		#INIZIALIZZAZIONE VARIABILI
		self.elettroni = np.array([])
		self.fotoni = np.array([])
		self.step = 0
		self.tot_ion = 0
		if materiale is None:
			self.ec = float(input("Inserisci l'energia critica "))
			self.ei= float(input("Inserisci l'energia di ionizzazione: "))
		else:
			self.ec = materiale[0]
			self.ei= materiale[1]

	def pbrem(self,step):
		"""
		
		Resituisce un booleano True/False in base alla probabilità che un elettrone faccia Bremsstrahlung ad un certo step di simulazione.
		"""
		return np.random.random() < 1 - np.exp(-step)
		   
	def pfoton(self,step):
		"""
		
		Resituisce un booleano True/False in base alla probabilità che un fotone produca una coppia ad un certo step di simulazione.
		"""
		
		return np.random.random() < 1 - np.exp(-step*(7/9))
		
	def	n_energic_partc(self):
		"""
		
		Restituisce il numero di elettroni e fotoni attivi ad un certo step.
		"""
		
		return self.elettroni.size+self.fotoni.size
		
	def stepxstep(self,step):
		"""
		
		Esegue l'evoluzione completa dello sciame per passi discreti.
		
		Schematizza i processi di perdita per ionizzazione, bremsstrahlung, produzione di coppia e collasso delle particelle sottosoglia.
		
		Parametri
		----------
		step : float
        Frazione della lunghezza di radiazione.
        
        Restituisce
        ----------
		Dataframe pandas contenente:
            - Numero di passo
            - Energia ionizzata totale
            - Energia ionizzata nello step
            - Numero di particelle attive
		
        Energia totale depositata per ionizzazione: float
		"""
		
		# Inizializzazione
		self.elettroni = self.in_elettroni.copy()
		self.fotoni = self.in_fotoni.copy()
		self.tot_ion = self.in_tot_ion 
		df_simulazione = pd.DataFrame([{'N * passo': 0, 'Energia ionizzata totale': self.tot_ion, 'Energia ionizzata nello step': 0, 'Numero di particelle attive': 1}])
		nstep=0
		
		while self.n_energic_partc()>0:
			
			# Energia ionizzata per step
			step_ion=0
			
			# Blocco elettro-positroni
			mask_attivi = self.elettroni > self.ei * step
			mask_inattivi = ~mask_attivi
			self.tot_ion+=self.ei*self.elettroni[mask_attivi].size*step 
			self.elettroni[mask_attivi]-= self.ei * step
			step_ion=self.ei*self.elettroni[mask_attivi].size*step
			fotoni_nuovi=np.array([])
			probability=np.array([self.pbrem(step) for _ in self.elettroni])
			mask_brem= np.logical_and(self.elettroni > self.ec, probability)
			if np.any(mask_brem):
				self.elettroni[mask_brem]=self.elettroni[mask_brem]/2
				fotoni_nuovi=self.elettroni[mask_brem]
			
			# Rimozione elettro-positroni
			if np.any(mask_inattivi):
				ecollapse=np.sum(np.random.uniform(0, self.elettroni[mask_inattivi]))
				self.tot_ion+=ecollapse
				step_ion+=ecollapse
			self.elettroni=self.elettroni[mask_attivi]
			
			#Blocco fotoni
			elettroni_nuovi=np.array([])
			if self.fotoni.size>0:
				probability=np.array([self.pfoton(step) for _ in self.fotoni])
				maskf_produzione = np.logical_and(self.fotoni> 1.022, probability)
				maskf_inattivi = self.fotoni<= 1.022 # 2 m_e c^2 in MeV
				maskf_rimanenti= ~maskf_inattivi & ~maskf_produzione
				self.fotoni[maskf_produzione]=self.fotoni[maskf_produzione]/2
				elettroni_nuovi =self.fotoni[maskf_produzione]
				if np.any(maskf_inattivi):
					fcollapse=np.sum(np.random.uniform(0, self.fotoni[maskf_inattivi]))
					self.tot_ion+=fcollapse
					step_ion+=fcollapse
			
			# Rimozione fotoni
			if self.fotoni.size>0:
				self.fotoni=self.fotoni[maskf_rimanenti]
			
			# Aggiunta particelle nuove
			if(elettroni_nuovi.size>0):
				#self.totp+=2*elettroni_nuovi.size
				self.elettroni=np.concatenate([self.elettroni, elettroni_nuovi, elettroni_nuovi])
			if(fotoni_nuovi.size>0):
				#self.totp+=fotoni_nuovi.size
				self.fotoni=np.concatenate([self.fotoni, fotoni_nuovi])
			nstep+=1
			nuova_riga = pd.DataFrame([{'N * passo': nstep,'Energia ionizzata totale': self.tot_ion, 'Energia ionizzata nello step': step_ion, 'Numero di particelle attive': self.n_energic_partc()}])
			df_simulazione = pd.concat([df_simulazione, nuova_riga], ignore_index=True)
			
		return df_simulazione, self.tot_ion
	
		
		
if __name__ == "__main__":	
	"""
	
	Test di funzionamento simulazione. 
	Stampa dataframe step per step e il tempo di esecuzione della simulazione.
	""" 
	
	en_i=float(input("Inserisci l'energia iniziale dell'elettrone:  "))
	step_i=float(input("Inserisci il passo della simulazione: "))
	sim = Simulazione(en_i)
	start = time.time()  
	df, _= sim.stepxstep(step_i)
	end = time.time() 
	print(df.to_string(index=False))
	print(f"Tempo di esecuzione: {end - start:.5f} secondi") 


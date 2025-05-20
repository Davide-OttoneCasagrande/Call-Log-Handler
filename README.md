# Call-Log-Handler

### CONSEGNA:
Progettare, realizzare e dimostrare un semplice applicativo "demo" realizzato utilizzando il linguaggio python che realizzi le seguenti funzionalità:  
- ricevere in ingresso/configurazione le coordinate di un folder del filesysem contenente file in formato csv che rappresentano dati di log di chiamate telefoniche (call-log)  
- identificare i file, aprirli ed estrarre i dati di call-log  
- strutturare i dati in dizionari json  
- rendere persistenti tali dati in un datastore esterno.  
    Non è necessario realizzare l'implementazione del datastore esterno, che verrà gestito da una libreria il cui sviluppo verrà affidato ad una terza parte (società esterna). La società esterna potrà realizzare il datastore utilizzando più tecnologie eterogenee, e.g. un semplice file su filesystem oppure un database NO-SQL (e.g. MongoDb) etc. Nella definizione tenere conto che in installati differenti si potrebbero volere usare tecinolige differenti (e.g in un caso l'implementazione su file, in un altro l'implementazione su DB NO-SQL).  
    Valutare quindi quale astrazione realizzare della libreria per ipotizzare un percorso, anche evolutivo, in cui si realizzeranno ed utilizzeranno differenti implementazioni su differenti tecnologie del datastore esterno. Valutare quali richieste/specifiche fare/fornire alla società esterna che realizzera la/le librerie di gestione del datastore
    persistente.

### DETTAGLIO
- Obiettivo:
    - Realizzare un'applicazione che:
        - Legga i file CSV da una directory.
        - Converta i dati in dizionari JSON-like.
        - Li salvi in un data store usando una libreria esterna fornita da terze parti
            che esponga un servzio di gestione della persistenza:
    - Rispettare i seguenti Requisiti di Design:
        - Separare chiaramente:
            - Parsing dei file CSV.
            - Modellazione delle chiamate (CallLog come entità OOP).
            - Interfaccia di accesso al DataStore.
            - Flusso di controllo generale dell’applicazione.
        - Progettare classi con responsabilità singole e coesive.
        - Utilizzare dizionari per la serializzazione JSON dei dati.

### VINCOLI
- svolgere una attività di progettazione prima di realizzare l'applicativo. Scegliere in libertà le modalità di descrizione della progettazione, da rivedere assieme ai tutor prima di iniziare le attività di sviluppo.
- utilizzare una modalità di progettazione Object oriented; in particolare sforzarsi di indirizzare un design modulare che si basi sul paradigma del "separation of concerns" (separazione di responsabilità)
- Una semplice progettazione potrebbe essere basata su
    - definizione di una tabella che identifichi ogni classe che compone l'applicativo ed una descrizione testuale delle responsabilità di tale classe
    - una descrizione, anche testuale, delle macro-interazioni previste fra le classi
- tentare di realizzare anche una strutturazione dei sorgenti coerente con la modularità del design
- è consentito l'uso di chatGPT solamente per
    - supporto puntuale relativo alla sintassi del linguaggio,
    - utilizzo di libreria python per lettura file csv e per gestione dizionari json
    - formazione su tematiche generali OO (e.g. modularità/separation of concerns)
    - uso di un ambiente di sviluppo (IDE) python
- **NON é consentito** l'uso di ChatGPT per la definizione della struttura generale dell'applicativo

### RAZIONALE DELL'ESERCIZIO
-sperimentare tecniche di progettazione OO
-sperimentare il setup di un ambiente di sviluppo e la definizione della struttura del software
-sperimentare semplici tecniche di acquisizione e parsing dei dati
-sperimentare semplici tecniche di modellizzazione del dato e di trasformazione in dizionari serializzabili JSON
-sperimentare le modalità di definizione di interazione con componenti sviluppati da terze parti

### DATI ACCESSORI
<details>
    <summary>Esempio di contenuto CSV:</summary> 
        timestamp,caller,receiver,duration,status,uniqueCallReference<br>
        2025-05-14T10:23:00,1234567890,0123456789,120,successfully_completed,AABBCCDD<br> 
        2025-05-14T10:24:00,2345678901,3456789012,0,called_busy,EEFFGGHH
</details>

### SPUNTI INIZIALI
Tentare di identificare le 4 entità principali che costituiscono l'applicazione e indirizzare il principio di "separation of conerns" astraendo utilizzando un design object oriented queste 4 entità principali
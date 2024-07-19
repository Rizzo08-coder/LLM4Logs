### settare ambiente

```bash
git clone https://github.com/Rizzo08-coder
docker compose up
```
verranno create due container:
- llm4logs -> contiene l'interprete python con tutte le sue dipendenze per eseguire le inferenze
- ollama -> contiene l'immagine di ollama e i 3 modelli LLM finetunati (llama3-beth, llama3-unsw, llama3-ecmlpkdd)


Gli script python per le inferenze degli LLM non finetunati sono suddivisi per dataset, quindi va modificato l'entry-point nel file
docker-compose.yml in base al dataset che si vuole usare.
Ognuno di questi script contiene diversi iperparametri da settare:
- model_name  (nome del modello che si vuole utilizzare per fare inferenze) -> ci si riferisce ai modelli presenti su Ollama
- number_of_shots (numero di n-shot del modello con n>=0)
- useJson (booleano che setta come risposta del LLM un json se è a True, altrimenti un numero) -> esso va impostato a True per i modelli code-oriented


Mentre vi è uno script separato per gli LLM finetunati, anche qua andrà impostato esso come entry-point. In base al modello utilizzato
verrà già impostato il dataset corretto.
Questo script contiene un solo iperparametro:
- model_name (nome del modello finetunato [llama3-beth, llama3-unsw, llama3-ecmlpkdd]


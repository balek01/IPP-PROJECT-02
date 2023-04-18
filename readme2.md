Implementační dokumentace k 2. úloze do IPP 2022/2023
Jméno a příjmení: Miroslav Bálek
Login: xbalek02

Skript interpret.py

### Statická analýza kódu

Statická analýza se provádí v PHP souboru assert.php, kde se na základě operačního kódu a pomocí regulárních výrazů ověřuje zda čtený vstup je v souladu s pravidly jazyka IPPcode23.

### Prerun

Jelikož Interpret provádí kód instrukci po instrucki nebyl by schopný určit existenci návěští. Proto je před spuštěním Interpretu nutno předat všechny návěští a instrukce. Z načtených instrukcí se vytváří instance třídy Instruction a jsou následně předány přes konstruktor Interpretu.

### Třída Interpret

Dynamickou analýzu provádí třída Interpret. Pomocí metody parse_argument se u instrukcí ověří správnost typů argumentů, zejména pak pokud je argumentem proměná. U proměných se ověřuje i jejich existence v aktuálních rámcích. Následně je vykonána požadovaná instrukce. Interpret obsahuje atributy jako: rámece, zásobník lokálních rámců, slovník instruckí a jejich operačních kódů, cestu k souboru se vstup a zásobník instrukcí pro návrat po volání instrukce call.

### Třída Instruction

Třída instuction obsahuje operační kód instrukce, její pořadí, seznam argumentů jenž obsahuje instance třídy Argument a instanci další Instrukce.

### Třída Argument

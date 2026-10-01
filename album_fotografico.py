
import csv
def carica_da_file(file_path):
    from csv import reader
    diz_per_anno={} #creo il dizionario
    try :
        file_csv = open(file_path, "r")
        lettura_csv = reader(file_csv)
        next(lettura_csv)  #salto la prima riga , che non serve
        for row in lettura_csv:#prendo ogni pezzo della riga e lo divido
            codice=row[0]
            fotografia = row[1]
            fotografo = row[2]
            mese = row[3]
            anno = row[4]
            if anno not in diz_per_anno:#creo la chiave che corrisponde all'anno
                diz_per_anno[anno] = []  # creo lista vuota la prima volta

            diz_per_anno[anno].append((codice,fotografia, fotografo, mese))#in base all'anno ci aggiungo le informazioni
    except FileNotFoundError:
            return None
    return diz_per_anno
    """Carica le foto dal file, creando un nuovo anno ogni volta che compare per la prima volta"""


def aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path):
    from csv import writer
    if not 1 <= mese <= 12:
        return None

    for lista in album.values():#se il codice è gia associato ad una foto non va bene
        for c, t, a, m in lista:
            if c == codice:
                return None

    if anno not in album:#se non ho una chiave con quell'anno la creo
        album[anno] = []

    foto = (codice, titolo, autore, mese)
    album[anno].append(foto)#carico la foto nel dizionario al corrispondete anno

    try:
        file_csv = open(file_path, "a", newline="")#scrivo la nuova riga nel file , "a" serve per aggiungere sennò lo spiana
        scrittura_csv = writer(file_csv)
        scrittura_csv.writerow([codice, titolo, autore, mese, anno])
        file_csv.close()
    except FileNotFoundError:
        # se da errore rimuovo la riga
        album[anno].remove(foto)
        return None

    return foto

    """Aggiunge una foto all'album, creando l'anno al volo se non è ancora presente"""


def cerca_foto(album, codice):
    for anno, lista in album.items():
        for c, t, a, m in lista:
            if c == codice:
                return f"{c},{t}, {a}, {m}, {anno}"
    return None

    """Cerca una foto nell'album dato il codice"""
    # TODO


def elenco_foto_anno_per_titolo(album, anno):
    if anno not in album:#se l'anno non c'e non va bene
        return None
    lista_titoli = []
    for c, t, a, m in album[anno]:
        lista_titoli.append(t)#inserisco i titoli nella lista
    return sorted(lista_titoli)#sordino la lista

    """Ordina i titoli delle foto di un dato anno in ordine alfabetico"""


def main():
    album = {}
    file_path = "album_fotografico.csv"

    while True:
        print("\n--- MENU ALBUM FOTOGRAFICO ---")
        print("1. Carica album da file")
        print("2. Aggiungi una nuova foto")
        print("3. Cerca una foto per codice")
        print("4. Elenco foto di un anno (ordinato per titolo)")
        print("5. Esci")

        scelta = input("Scegli un'opzione >> ").strip()

        if scelta == "1":
            while True:
                file_path = input("Inserisci il path del file da caricare: ").strip()
                album = carica_da_file(file_path)
                if album is not None:
                    break

        elif scelta == "2":
            if not album:
                print("Prima carica l'album da file.")
                continue

            codice = input("Codice della foto: ").strip()
            titolo = input("Titolo: ").strip()
            autore = input("Autore: ").strip()
            try:
                mese = int(input("Mese (1-12): ").strip())
                anno = int(input("Anno: ").strip())
            except ValueError:
                print("Errore: inserire valori numerici validi per mese e anno.")
                continue

            foto = aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path)
            if foto:
                print("la struttura dati aggiornata è:")
                print(album)
                for chiave_anno in album:
                    print(chiave_anno, ":")
                    for codice, titolo, autore, mese in album[chiave_anno]:
                        print(codice, titolo, autore, mese)

                print(f"Foto aggiunta con successo!")
            else:
                print("Non è stato possibile aggiungere la foto.")

        elif scelta == "3":
            if not album:
                print("L'album è vuoto.")
                continue

            codice = input("Inserisci il codice della foto da cercare: ").strip()
            risultato = cerca_foto(album, codice)
            if risultato:
                print(f"Foto trovata: {risultato}")
            else:
                print("Foto non trovata.")

        elif scelta == "4":
            if not album:
                print("L'album è vuoto.")
                continue

            try:
                anno = input("Inserisci l'anno da consultare: ").strip()
            except ValueError:
                print("Errore: inserire un valore numerico valido.")
                continue

            titoli = elenco_foto_anno_per_titolo(album, anno)
            if titoli is not None:
                print(f'\nFoto del {anno}:')
                print("\n".join([f"- {titolo}" for titolo in titoli]))
            else:
                print(f"Nessuna foto trovata per l'anno {anno}.")

        elif scelta == "5":
            print("Uscita dal programma...")
            break
        else:
            print("Opzione non valida. Riprova.")


if __name__ == "__main__":
    main()

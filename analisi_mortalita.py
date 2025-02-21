import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt



file_path= 'cause_morte.json_'
df = pd.read_json(file_path)

st.title("CAUSE DI MORTE IN SICILIA")
st.write('DataFrame delle cause di morte in Sicilia', df)

df['MASCHI'] = pd.to_numeric(df['MASCHI'], errors='coerce')
df['FEMMINE'] = pd.to_numeric(df['FEMMINE'], errors='coerce')
df = df.drop_duplicates()


sum_patologia=df.groupby('PATOLOGIA')[['MASCHI', 'FEMMINE']].sum()

# Aggiungi una nuova colonna 'TOTALE' che è la somma di 'MASCHI' e 'FEMMINE'
sum_patologia['TOTALE'] = sum_patologia['MASCHI'] + sum_patologia['FEMMINE']

# Visualizza la tabella con le somme per patologia e il totale
st.write("### Somma per Patologia (Maschi, Femmine e Totale):", sum_patologia)

# usa il selectbox per far scegliere l'utente tra maschi, femmine e totale
scelta = st.selectbox(
    "Seleziona il gruppo di cui vedere una classifica delle patologie più mortali:",
    ['MASCHI', 'FEMMINE', 'TOTALE'])

# usa lo slider per far scegliere all'utente il numero di patologie da visualizzare
num_classifica = st.slider("Selezione il numero di patologie per visualizzare la distribuzione per il gruppo selezionato", min_value=1, max_value=10, value=10)


# Filtra le patologie in base al numero selezionato dall'utente
top_n = sum_patologia.nlargest(num_classifica, scelta)


# Crea il grafico a torta
fig, ax = plt.subplots(figsize=(10, 8))
ax.pie(top_n[scelta], labels=top_n.index, autopct='%1.1f%%', startangle=90)
ax.set_title(f"Distribuzione delle prime {num_classifica} patologie più mortali per {scelta}")
ax.axis('equal')  # Per fare in modo che il grafico sia un cerchio

# Visualizza il grafico
st.pyplot(fig)


sum_patologia=df.groupby('PATOLOGIA')[['MASCHI', 'FEMMINE']].sum()
# Filtra le righe dove sia 'MASCHI' che 'FEMMINE' sono diversi da 0
sum_patologia = sum_patologia[(sum_patologia['MASCHI'] != 0) & (sum_patologia['FEMMINE'] != 0)]

# Aggiungi una nuova colonna 'TOTALE' che è la somma di 'MASCHI' e 'FEMMINE'
sum_patologia['TOTALE'] = sum_patologia['MASCHI'] + sum_patologia['FEMMINE']

top_50 = sum_patologia.nlargest(50,'TOTALE')
st.write("ECCO LE PRIME 50 PATOLOGIE PER MORTALITA'", top_50)
top_50 = top_50.sort_values('PATOLOGIA')

malattie_selezionate = st.multiselect(
    "Seleziona le malattie per visualizzare i dati comparati tra Maschi e Femmine:(massimo 6)",
    options = top_50.index.tolist(),  # Elenco di tutte le patologie
    default = top_50.index.tolist()[:3]) #Di default mi da le prime 5


#limita un massimo di 6 malattie
if len(malattie_selezionate) > 6:
    st.warning("Puoi selezionare un massimo di 6 malattie.")
    malattie_selezionate = malattie_selezionate[:6]

# Filtra il DataFrame in base alle malattie selezionate
if malattie_selezionate:
    # Se l'utente ha selezionato delle malattie, mostra i dati per quelle malattie
    df_selezionato = top_50.loc[malattie_selezionate]

# Visualizza i dati selezionati
    st.write("Dati comparati tra Maschi e Femmine per le malattie selezionate:", df_selezionato)

# Crea il grafico comparativo per maschi e femmine
    fig, ax = plt.subplots(figsize=(10, 10))

# Disegna il grafico a barre per ogni malattia
    df_selezionato[['MASCHI', 'FEMMINE']].plot(kind='bar', ax=ax)
    ax.set_title('Comparazione tra Maschi e Femmine per le malattie selezionate')
    ax.set_ylabel('Numero di decessi')
    ax.set_xlabel('Malattia')
    ax.grid(True)


 # Visualizza il grafico
    st.pyplot(fig)
else:
    st.write("Seleziona almeno una malattia per visualizzare i dati comparati.")
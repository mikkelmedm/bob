import streamlit as st
import pandas as pd
import numpy as np
import pickle

from faker import Faker
fake = Faker('dk_DK')

def random_genders(size):
    """Generate n-length ndarray of genders."""
    gender = ("M", "F")
    return np.random.choice(gender, size=size)

def random_times(start, end, size):
    """
    Generate random dates within range between start and end.    
    Adapted from: https://stackoverflow.com/a/50668285
    """
    # Unix timestamp is in nanoseconds by default, so divide it by
    # 24*60*60*10**9 to convert to days.
    divide_by = 10**9
    
    start_u = start.value // divide_by
    end_u = end.value // divide_by
    return pd.to_datetime(np.random.randint(start_u, end_u, size), unit="s")

def random_postnr(start, end, size):
    return np.random.choice(np.arange(start, end, 50), size=size)

def f(x):
    if (x > 6) and (x <= 11):
        return 'Morgen'
    elif (x > 11) and (x <= 16):
        return'Middag'
    elif (x > 16) and (x <= 21):
        return'Aften'
    elif (x <= 6) or (x > 21):
        return'Nat'

# Load from file
with open('forest.pkl', 'rb') as file:
    forest = pickle.load(file)

with open('le.pkl', 'rb') as file:
    le = pickle.load(file)

with open('le1.pkl', 'rb') as file:
    le1 = pickle.load(file)

with open('norm.pkl', 'rb') as file:
    norm = pickle.load(file)

dfphonere = pd.read_csv('dfphonere.csv')

# Generer dataframe med 1000 kunder
size = 1000
dagenskunder = pd.DataFrame(columns=['Navn','TelefonNr', 'Køn', 'PostNr'])

dagenskunder['Køn'] = random_genders(size)
dagenskunder['PostNr'] = random_postnr(1000, 3500, size)

for i in dagenskunder.index:
    dagenskunder.at[i, 'Navn'] = fake.name()
    dagenskunder.at[i, 'TelefonNr'] = fake.phone_number()


# from datetime import datetime
# now = datetime.now().time().hour

def poc(phonerID,tidspunkt):
    
    '''
    Proof of concept!!!!
    
    PhonerID : Hvad ID har Phoneren som skal finde sin opkaldsliste med bedste match
    tidspunkt : Hvad tid på dagen foregår dette. Default er sat til nu.
    '''
    
    #tid = f( int( tidspunkt )) 
    X_test = dagenskunder[['Køn', 'PostNr']].copy()
    
    for i in X_test.index:
        _, ppostnr, pkøn = dfphonere.loc[phonerID-1,:]
        X_test.at[i, 'Phoner_PostNr'] = ppostnr
        X_test.at[i, 'Phoner_Køn'] = pkøn
        X_test.at[i, 'Time'] = tidspunkt

    X_test['PostNr_dist'] = abs(X_test['PostNr'] - X_test['Phoner_PostNr'])

    X_test['Køn'] = le.transform(X_test['Køn'])
    X_test['Phoner_Køn'] = le.transform(X_test['Phoner_Køn'])

    X_test['Time'] = le1.transform(X_test['Time'])
    
    xxx = X_test[['Køn',"PostNr_dist","Time","Phoner_Køn"]].copy()
    
    xxx = norm.transform(xxx)
    
    dfp = dagenskunder.copy()

    dfp['Salgschance']=[x[1] for x in forest.predict_proba(xxx)]
    dfp['Salgschance']=round(dfp['Salgschance']*100,2)
    
    print(f'For Phoner{phonerID}/{pkøn} med postnr:{ppostnr} og opkaldstidspunkt sat til {tidspunkt} er følgende kunder bedste match:')
    return dfp.sort_values('Salgschance',ascending = False)
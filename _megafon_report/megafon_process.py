
from glob import glob
import numpy as np
import pandas as pd
from datetime import datetime as dt
from matplotlib import pyplot as plt
import seaborn as sns

sns.set()

# VARIABLES
start_date = '2020-01'
stop_date = '2020-02'

# some functions
def operator_find(rawline):
    operators = ['МТС', 'Теле2', 'Билайн', 'Мегафон']
    for operator in operators:
        if operator in rawline:
            return operator

def type_find(rawline):
    cases = {
    'Исх. ': 'call_out',
    'Вх. ': 'call_in',
    'Входящее сообщение': 'sms_in',
    'Исх. сообщение': 'sms_out',
    'Мобильный интернет': 'internet'
    }
    for i in cases.keys():
        if i in rawline:
            return cases[i]


# takes only first one
f = glob('*.xlsx')[0]
df = pd.read_excel(f, skipfooter=4)

### cleaning the data
df.dropna(subset=[df.columns[-1]], inplace=True) # leaving only filled rows according the price presence
df['datetime'] = df['Дата'] + ' ' + df['Время']
df['datetime'] = pd.to_datetime(df['datetime'], format='%d.%m.%Y %H:%M:%S')
df.set_index('datetime', inplace=True)
df.drop(axis=1, labels=df.columns[0: 3], inplace=True)
df.columns = ['type', 'number', 'location', 'amount', 'unit', 'sum']

# feature engineering
df['unit'] = df['unit'].map({'Килобайт': 'mb', 'Секунда': 'minutes', 'Штука': 'piece'})
df['operator'] = df['type'].apply(operator_find)
df['type'] = df['type'].apply(type_find) # ---------- REDEFINE THE TYPE COLUMN
df.loc[(df['type'] == 'call_out') | (df['type'] == 'call_in'), 'amount'] /= 60 # turn speaktime to minutes
df.loc[df['type'] == 'internet', 'amount'] /= 1024 # turn kb to mb
df['rate'] = df['sum'] / df['amount']
df['hour'] = df.index.hour
df['dayofweek'] = df.index.dayofweek

df = df.loc[start_date:stop_date]

print(df.info())


## List of locations
print('\n--- LOCATIONS ---\n', df['location'].value_counts())

# print('\n--- TYPES ---\n', df['unit'].value_counts())
# print(df.groupby('call_out').sum())
# print(df['unit'].value_counts())

## Paid outgoing calls
print('\nOutgoing Paid phonecalls:\n', df[(df['type'] == 'call_out') & (df['rate'] > 0)][['number', 'location', 'amount', 'rate', 'sum']])

## Paid incoming calls
print('\nPaid incoming calls:\n', df[(df['type'] == 'call_in') & (df['rate'] > 0)][['number', 'location', 'amount', 'rate', 'sum']])

## Mean talk time and count per number
df2 = df[(df['type'] == 'call_out') | (df['type'] == 'call_in')].groupby('number').agg({'amount': ['mean', 'sum', 'count']})
df2.columns = df2.columns.droplevel()
# print(df2)
print('\nMean talk time and count per number (count sorted)\n', df2.sort_values(by='count', ascending=False).head(5))
print('\nMean talk time and count per number (sum sorted)\n', df2.sort_values(by='sum', ascending=False).head(5))

## Top 5 outgoing calls
df2 = df[df['type'] == 'call_out']['number'].value_counts()[:5]
# print('\nTop 5 outgoing calls\n', df2)
sns.barplot(x=df2.values, y=df2.index, orient='h', order=df2.index)

plt.xlabel('Number of calls')
plt.ylabel('Phome Number')
plt.title('Top-5 Outgoing Phonecalls')
plt.tight_layout()
plt.show()


# --- top 5 income calls ---
df2 = df[df['type'] == 'call_in']['number'].value_counts()[:5]
print(df2)
sns.barplot(x=df2.values, y=df2.index, orient='h', order=df2.index)
plt.xlabel('Number of calls')
plt.ylabel('Phome Number')
plt.title('Top-5 Incoming Phonecalls')
plt.tight_layout()
plt.show()


# --- daily phonecalls PLOT ---
df2 = df[(df['type'] == 'call_out') | (df['type'] == 'call_in')].groupby('hour').count()
plt.figure(figsize=(8, 5))
sns.barplot(x=df2['amount'].index,
    y=df2['amount'].values)

plt.xlabel('Hour of day')
plt.ylabel('Number of phonecalls')
plt.title('Phonecalls (in & out) during the day')
plt.tight_layout()
plt.show()


# --- weekly phonecalls PLOT ---
df2 = df[(df['type'] == 'call_out') | (df['type'] == 'call_in')].groupby('dayofweek').count()
weekdays = {0:'Пн', 1:'Вт', 2:'Ср', 3:'Чт', 4:'Пт', 5:'Сб', 6:'Вс'}
df2.index = df2.index.map(weekdays)
plt.figure(figsize=(8, 5))
sns.barplot(x=df2['amount'].index,
    y=df2['amount'].values)

plt.xlabel('Day of week')
plt.ylabel('Number of phonecalls')
plt.title('Phonecalls (in & out) during week')
plt.tight_layout()
plt.show()


# --- phone calls during weekdays/days heatmap PLOT ---
df2 = df[(df['type'] == 'call_out') | (df['type'] == 'call_in')].groupby(by=['dayofweek', 'hour']).count()['amount'].unstack()
# dayhour = df.groupby(by=['dayofweek', 'hour']).count()['amount'].unstack()
weekdays = {0:'Пн', 1:'Вт', 2:'Ср', 3:'Чт', 4:'Пт', 5:'Сб', 6:'Вс'}
df2.sort_index(inplace=True)
df2.index = df2.index.map(weekdays)
sns.heatmap(df2, 
    cmap='YlOrRd',
    linewidths=2,
    linecolor='white')
plt.title('Phonecalls per hour in day of week')
plt.xlabel('Hour')
plt.ylabel('Day of week')
plt.tight_layout()
plt.show()

# --- mean speaktime ---
df2 = df[(df['type'] == 'call_out') | (df['type'] == 'call_in')]['amount'].values.mean()
print(df2)

# --- speaktime daily during week ---
df2 = df[(df['type'] == 'call_out') | (df['type'] == 'call_in')].groupby('dayofweek').sum()['amount']
weekdays = {0:'Пн', 1:'Вт', 2:'Ср', 3:'Чт', 4:'Пт', 5:'Сб', 6:'Вс'}
df2.sort_index(inplace=True)
df2.index = df2.index.map(weekdays)
plt.figure(figsize=(8, 5))
sns.barplot(x=df2.index,
    y=df2.values)
plt.xlabel('Day of week')
plt.ylabel('Lenght of phonecalls')
plt.title('Phonecall lenght in day of week (summary)')
plt.tight_layout()
plt.show()

### INTERNET CONSUMPTION

## Internet traffic weekdays/day heatmap
df2 = df[df['type'] == 'internet'].groupby(by=['dayofweek', 'hour']).count()['amount'].unstack()
weekdays = {0:'Пн', 1:'Вт', 2:'Ср', 3:'Чт', 4:'Пт', 5:'Сб', 6:'Вс'}
df2.sort_index(inplace=True)
df2.index = df2.index.map(weekdays)
sns.heatmap(df2, 
    cmap='YlOrRd',
    linewidths=2,
    linecolor='white',
    cbar_kws={'label': 'Mb'})
plt.title('Internet traffic per hour in day of week')
plt.xlabel('Hour')
plt.ylabel('Day of week')
plt.tight_layout()
plt.show()

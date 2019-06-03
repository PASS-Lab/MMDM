"""
Author: Christian Lozoya, 2017
"""
import os
import random as random
import re

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.externals import joblib

random.seed(0)
np.random.seed(0)

ID = 'STRUCTURE_NUMBER_008'
LATITUDE = 'LAT_016'
LONGITUDE = 'LONG_017'
ENCODING = 'latin1'
NA_VALUES = ['N']


def read_folder(directory, ext):
    """
    Collect all file paths with given extension (ext) inside directory
    """
    paths = []
    for file in os.listdir(directory):
        if file.split('.')[-1].lower() == ext.lower():
            paths.append(file)
    return sorted(paths)


def process_data(item, directory, ext, clean=False):
    """
    item is the item of interest (str)
    dir is the directory where the files of data are found (str)
    paths is all the paths of data in the directory (list of str)
    clean determines whether or not incomplete data is removed
    returns a list of pandas dataFrames and a list of numerics to name the files
    """
    data = []
    yrs = []
    paths = read_folder(directory, ext)
    for i, file in enumerate(paths):
        data.append(pd.read_csv(directory + '/' + file, usecols=[ID] + [item], na_values=NA_VALUES,
                                dtype={**{ID: str}, **{item: str}}, encoding=ENCODING))
        yrs.append(re.findall(r"[0-9]{4}(?=.txt)", file)[0])
        data[i].set_index(ID, inplace=True)
        data[i] = data[i][~data[i].index.duplicated()]
    data = concat_data(dataFrame=data, columns=yrs, index=item)
    if clean:
        data = clean_data(dataFrame=data, columns=yrs)
    return data, yrs


def concat_data(dataFrame, columns, index=None):
    """
    Concatenate list of pandas Series into a DataFrame
    dataFrame is a pandas DataFrame and columns are the columns in data
    index is used for concatenating only specific columns
    """
    if index:
        cnc = pd.concat([d[index] for d in dataFrame], axis=1)
    else:
        cnc = pd.concat([d for d in dataFrame], axis=1)
    cnc.columns = columns
    return cnc


def count_matrix(data, matrix, columns=None, hst=False, offset=None):
    """
    Count data and store the count in matrix (pre-labeled DataFrame objects)
    columns is a list of column labels
    """
    data = data.astype('int8')
    if not hst:
        matrix.fillna(0, inplace=True)
    length = len(data.columns)
    for i, row in enumerate(data.iterrows()):
        for j, column in enumerate(data.loc[row[0], :]):
            if hst:
                matrix[data.iloc[i, j]].append(int(columns[j]) - (offset - 1))
            elif columns:  # If columns are specified: row=the value in (i,j), column=column j
                matrix.loc[data.iloc[i, j], columns[j]] += 1
            else:  # If nothing is specified: transition matrix is assumed
                if (j < length - 1):
                    try:
                        if (int(data.iloc[i, j + 1]) <= int(data.iloc[i, j])):
                            matrix.loc[data.iloc[i, j], data.iloc[i, j + 1]] += 1
                    except Exception as e:
                        print(e)
    return matrix


def normalize_rows(dataFrame):
    """
    Normalize dataFrame by row
    """
    try:
        nrm = dataFrame.div(dataFrame.sum(axis=1), axis=0)
        nrm.fillna(0, inplace=True)
        return nrm
    except Exception as e:
        print(e)


def frq(focus, matrix):
    """
    Count state transitions in data and store the count in matrix (pre-labeled DataFrame objects)
    """
    matrix = matrix
    if focus == "year":
        frq = matrix.T
        frq = frq[frq.columns[::-1]]
        return normalize_rows(frq).as_matrix()
    elif focus == "state":
        return normalize_rows(matrix.T).T.as_matrix()
    else:
        print("Select focus")


def hst(data, matrix, columns):  # TODO bad method + needs generalizing (only works for freq vs state)
    print(data)
    print(matrix)
    hst = count_matrix(data=data, matrix=matrix, columns=columns, hst=True)
    hst = pd.DataFrame([hst[m] for m in hst], index=[m for m in hst])
    print(hst)
    hst.fillna(0, inplace=True)
    hst.sort_index(ascending=False, inplace=True)
    return hst.as_matrix().astype(np.float64)


def clean_data(dataFrame, columns):
    """
    Clears incomplete data resulting in regular matrix
    data is a pandas DataFrame and columns are the columns in data
    """
    cln = dataFrame
    for column in columns:
        cln = (cln[np.isfinite(cln[column].astype(float))])
    cln.columns = columns
    return cln


def get_transition_matrix(data, vS, offset=None):
    return normalize_rows(count_matrix(data, pd.DataFrame(index=vS, columns=vS), offset=offset))


def sample(simulation, vS, pV, iteration):
    """
    simulation: list
    vS: list of valid state names
    pV: probability vector
    iteration: current iteration, int
    returns a state vector
    """
    r = random.uniform(0, 1)
    if r > 2:
        state = np.argmax(pV)
        simulation[iteration].append(state)
        return simulation, np.transpose((pd.Series([1 if s == state else 0 for s in vS], index=vS)))
    else:
        sum = 0
        randomNumber = random.uniform(0, 1)
        # Assign state if randomNumber is within its range
        for state, prob in zip(vS, pV):
            sum += prob
            if (sum >= randomNumber):
                if state > simulation[-1][-1]:
                    simulation[iteration].append(simulation[-1][-1])
                    return simulation, np.transpose((pd.Series([1 if s == simulation[-1][-1] else 0 for s in vS], index=vS)))
                else:
                    simulation[iteration].append(state)
                    return simulation, np.transpose((pd.Series([1 if s == state else 0 for s in vS], index=vS)))


def markov_chain_monte_carlo(time, matrix, vS, iS, iterations):
    simulation = []
    for i in range(iterations):
        simulation.append([])
        cS = iS
        for t in range(time):
            if t != 0:
                # Multiply current state and transition matrix, resulting in a probability vector
                pV = cS.dot(np.linalg.matrix_power(matrix, t))
                simulation, cS = sample(simulation, vS, pV, i)
            else:
                for state, prob in zip(vS, cS):
                    if prob == 1:
                        simulation[i].append(state)
        simulation[i] = pd.Series(simulation[i])
    return simulation


def model_monte_carlo(time, model, vS, iS, iterations):
    simulation = []
    age = np.array([time])
    kind = np.array([0 if i != 1 else 1 for i in range(9)])
    type = np.array([0 if i != 19 else 1 for i in range(22)])

    for i in range(iterations):
        simulation.append([])
        cS = iS
        for t in range(time):
            #print(np.argmax(cS))
            if t != 0:
                cS = np.hstack([age, np.argmax(cS), kind, type])
                pV = model.predict_proba([cS])[0]
                simulation, cS = sample(simulation, vS, pV, i)
            else:
                for state, prob in zip(vS, cS):
                    if prob == 1:
                        simulation[i].append(state)
        simulation[i] = pd.Series(simulation[i])
    return simulation


plt.ylim(0, 9)
dataDir = 'training'
item = 'DECK_COND_058'
iterations = 10000
clean = True
nStates = 10
offset = 1992

data, yrs = process_data(item=item, directory=dataDir, ext='txt', clean=clean)
o = data.T.astype('int8')
o.index = o.index.astype(int) - offset
#plt.plot(o.mode(axis=1), linestyle=':')
plt.plot(o.mean(axis=1), linestyle='--')
vS = tuple(range(10))
time = len(data.columns)
#Q = get_transition_matrix(data, vS, offset=offset)
model = joblib.load("model.joblib.dat")
plt.xlabel('Time')
plt.ylabel('Condition')
plt.title('{} Gradient Boost Simulations'.format(iterations))
for initialState in range(9, nStates):
    iS = np.array([0 if i != initialState else 1 for i in range(nStates)])
    #simulationA = markov_chain_monte_carlo(100, Q, vS, iS, iterations=iterations)
    #c = pd.concat(simulationA, axis=1)
    #plt.plot(c.mode(axis=1), linestyle=':')
    #plt.plot(c, linewidth=0.5)
    #plt.plot(c.mean(axis=1), linewidth=2.0)


    simulationB = model_monte_carlo(100, model, vS, iS, iterations=iterations)
    c = pd.concat(simulationB, axis=1)
    #plt.plot(c.mode(axis=1))
    plt.plot(c,  linestyle=':', linewidth=0.5)
    plt.plot(c.mean(axis=1), linewidth=2.0, label='Simulations Mean')
plt.legend(loc='best')

plt.show()

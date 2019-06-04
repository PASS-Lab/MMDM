"""
Author: Christian Lozoya, 2017
"""

import numpy as np
import os
import pandas as pd
from Utilities import DataHandler as dh
from Utilities import MathHandler as mh


def get_probability_vectors(states, transitionProbabilityMatrix):
    probabilityVectors = []
    for state in states:
        probabilityVectors.append(pd.Series([1 if s == state else 0 for s in states], index=states))
    probabilityVectorsDict = {state: pd.Series(probabilityVector.dot(transitionProbabilityMatrix))
                              for state, probabilityVector in zip(states, probabilityVectors)}
    return probabilityVectorsDict


def get_state_vectors(states):
    stateVectorsDict = {state: np.transpose((pd.Series([1 if s == state else 0 for s in states],
                                                       index=states)))
                        for state in states}
    return stateVectorsDict


def monte_carlo_curve_fit(initialStateVector, transitionProbabilityMatrix,
                          iterations, timeSteps, metropolisHastings=False):
    monteCarlo = []
    index = initialStateVector.index
    probabilityVectors = get_probability_vectors(index, transitionProbabilityMatrix)
    stateVectorsDict = get_state_vectors(index)
    for i in range(iterations):
        currentStateVector = initialStateVector
        state = [state for state, prob in zip(index, currentStateVector) if prob == 1][0]
        simulation = [state]
        for t in range(1, timeSteps):
            probabilityVector = probabilityVectors[state]
            if probabilityVector.sum() != 0:
                randomNumber, proposedState, proposedStateVector = sample(index,
                                                                          probabilityVector,
                                                                          stateVectorsDict)
            if metropolisHastings:
                state, currentStateVector = metropolis_hastings(proposedState=proposedState,
                                                                proposedStateVector=proposedStateVector,
                                                                priorState=state,
                                                                priorStateVector=currentStateVector,
                                                                randomNumber=randomNumber, p=0)
            else:
                state, currentStateVector = proposedState, proposedStateVector
            simulation.append(state)
        monteCarlo.append(pd.Series(simulation))
    monteCarloMatrix = dh.concat_data(monteCarlo, columns=list(range(iterations)))
    return monteCarloMatrix, pd.DataFrame()


def experimental_monte_carlo(distribution, transitionProbabilityMatrix, iterations):
    try:
        simulation = []
        likelihood = []
        for i in range(iterations):
            sum = 0
            randomNumber = np.random.uniform(0, 1)
            for state in distribution.index:
                sum += distribution.loc[state]
                if sum >= randomNumber:
                    simulation.append(state)
                    if len(simulation) > 1:
                        likelihood.append(get_likelihood(simulation[-1],
                                                         simulation[-2],
                                                         transitionProbabilityMatrix))
                    break
        monteCarlo = pd.DataFrame(simulation)
        likelihood = pd.DataFrame(likelihood)
        return monteCarlo, likelihood
    except Exception as e:
        print(e)


def monte_carlo(initialStateVector, transitionProbabilityMatrix,
                iterations, metropolisHastings=False):
    """
    initialStateVector: pandas Series
    transitionProbabilityMatrix: pandas DataFrame
    iterations: int
    metropolisHastings: boolean
    return: tuple of (pandas Dataframe, pandas DataFrame)
    """
    index = initialStateVector.index
    probabilityVectors = get_probability_vectors(index, transitionProbabilityMatrix)
    stateVectorsDict = get_state_vectors(index)
    currentStateVector = initialStateVector
    state = [state for state, prob in zip(index, currentStateVector) if prob == 1][0]
    simulation = [state]
    likelihoodList = []
    for i in range(iterations):
        probabilityVector = probabilityVectors[state]
        if probabilityVector.sum() != 0:
            randomNumber, proposedState, proposedStateVector = sample(index,
                                                                      probabilityVector,
                                                                      stateVectorsDict)
        p = get_likelihood(proposedState=proposedState,
                           priorState=state,
                           transitionProbabilityMatrix=transitionProbabilityMatrix)
        if metropolisHastings:
            state, currentStateVector = metropolis_hastings(proposedState=proposedState,
                                                            proposedStateVector=proposedStateVector,
                                                            priorState=state,
                                                            priorStateVector=currentStateVector,
                                                            randomNumber=randomNumber,
                                                            p=p)
        else:
            state, currentStateVector = proposedState, proposedStateVector
        simulation.append(state)
        likelihoodList.append(p)
    monteCarloMatrix = pd.DataFrame(simulation)
    likelihood = pd.DataFrame(likelihoodList)
    return monteCarloMatrix, likelihood


def sample(states, probabilityVector, stateVectorsDict):
    """
    states: list
    probabilityVector is a probability vector: list
    returns state value, state vector: float, list
    """
    # random.seed(1)
    sum = 0
    randomNumber = np.random.uniform(0, 1)
    for state, prob in zip(states, probabilityVector):
        sum += prob
        if (sum >= randomNumber):
            return randomNumber, state, stateVectorsDict[state]


def get_likelihood(proposedState, priorState, transitionProbabilityMatrix):
    pX0 = transitionProbabilityMatrix.loc[priorState, proposedState]
    pX1 = transitionProbabilityMatrix.loc[proposedState, priorState]
    if pX1 != 0:
        return pX0 / pX1
    else:
        return 0


def metropolis_hastings(proposedState, proposedStateVector,
                        priorState, priorStateVector,
                        randomNumber, p):
    if randomNumber <= p:
        print('proposed')
        return proposedState, proposedStateVector
    else:
        print('prior')
        return priorState, priorStateVector


def monte_carlo_frequency(monteCarloMatrix, keys):
    temp = mh.frequency(monteCarloMatrix)
    frq = pd.Series(index=keys).fillna(0)
    for i in temp.index:
        frq[i] = temp[i]
    return frq

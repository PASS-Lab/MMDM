"""
Author: Christian Lozoya, 2017
"""
import difflib
import operator
import os
import re
import unicodedata

import pandas as pd

OPERATORS = {'>=': operator.ge,
             '<=': operator.le,
             '>': operator.gt,
             '<': operator.lt,
             '==': operator.eq}

INVERTED_OPERATORS = {operator.ge: '>=',
                      operator.le: '<=',
                      operator.gt: '>',
                      operator.lt: '<',
                      operator.eq: '=='}

OPERATORS_WORDS = {'greaterthanorequalto': '>=',
                   'lessthanorequalto': '<=',
                   'greaterthan': '>',
                   'lessthan': '<',
                   'equal': '=='}

# DATABASE
ENCODING = None
ID = None  # 'STRUCTURE_NUMBER_008'
NA_VALUES = ['N']
SEPARATOR = ','

"""
The directory containing the data to be read and the directory
where the query results are to be stored are specified by the
dataDir and resultsDir variables respectively.
"""
dataDir = 'data'
resultsDir = 'results'

querySettings = {
    'dataDir': dataDir,
    'columns': False,  # Set to true to limit the results to only show the columns specified in 'entries'
    'entries': {
        'ROUTE_PREFIX_005B': [
            '3',
            '4'
        ],
        'HIGHWAY_DISTRICT_002': [
            '02',
        ]
    },
    'tol': 0.1,
    'resultsDir': resultsDir,
}


def is_number(str):
    """
    Determine if a string is a number.
    """
    try:
        float(str)
        return True
    except ValueError as e:
        print(e)
    try:
        unicodedata.numeric(str)
        return True
    except (TypeError, ValueError) as e:
        print(e)
    return False


def filter_data(dataFrame, column, entry):
    operator, number = inequality(entry)
    if operator != None:
        if is_number(number):
            if float(number) == int(float(number)):
                number = int(float(number))
            filtered = pd.DataFrame(data=dataFrame[operator(dataFrame.astype(float)[column], number)])
        else:
            filtered = pd.DataFrame(data=dataFrame[operator(dataFrame.astype(str)[column], number)])
        return filtered
    operators, numbers = interval(entry)
    if operators != (None, None):
        leftOperator = operators[0]
        rightOperator = operators[1]
        leftNumber = numbers[0]
        rightNumber = numbers[1]
        filtered = pd.DataFrame(data=dataFrame[
            leftOperator(dataFrame[column], leftNumber) &
            rightOperator(dataFrame[column], rightNumber)])
        return filtered
    return None


def inequality(str):
    """
    Process inequalities in an entry string.
    Supports <, >, <=, >=, or english equivalent.
    If a number is detected, an inequality operator will be searched for.
    If an inequality operator is not found, an english equivalent will be searched for.
    str: string
    return: tuple
    """
    string = str.lower()
    numberRegex = re.findall(r'(\d*[.]?\d*$)', string.strip())
    if numberRegex == ['']:
        numberRegex = re.findall(r'[A-Za-z]+$', string.strip())
    if numberRegex:
        number = numberRegex[0]
    else:
        number = None
    if number:
        leftover = re.sub(number, '', string).strip().replace(" ", "")
        if leftover in OPERATORS:
            op = OPERATORS[leftover]
            return op, number
        return None, number
    return None, None


def interval(entry):
    """
    Process intervals in an entry string. Supports - (exclusive), -- (inclusive)
    str: string
    return: tuple
    """
    string = entry.lower()
    number1 = ''
    number2 = ''
    second = False
    for c in entry:
        if c.isdigit() or c == '.':
            if second == False:
                number1 += c
            else:
                number2 += c
        elif not c.isdigit() and len(number1) > 0:
            second = True
    if number1 and number2:
        leftover = re.sub(number1, '', string).strip().replace(" ", "")
        leftover = re.sub(number2, '', leftover).strip().replace(" ", "")
        numbers = (number1, number2)
        if leftover:
            op = leftover
        else:
            op = None

        if op:
            if op == '--':
                ops = (OPERATORS['>='], OPERATORS['<='])
            else:
                ops = (OPERATORS['>'], OPERATORS['<'])
            return ops, numbers
    return (None, None), (None, None)


def reduce_expression(expressionList):
    greater = {}
    less = {}

    def inserter(dict, key, op, op1, op2):
        if key not in dict.keys():
            dict[key] = op
        elif dict[key] == op1 and op == op2:
            dict[key] = op

    for expression in expressionList:
        op, number = inequality(expression)
        if op:
            if is_number(number): number = float(number)
            if op == operator.gt or op == operator.ge:
                inserter(greater, number, op, operator.gt, operator.ge)
            else:
                inserter(less, number, op, operator.lt, operator.le)
        else:
            ops, numbers = interval(expression)
            if ops != (None, None):
                for op, number in zip(ops, numbers):
                    nums = []
                    if is_number(numbers[0]): nums.append(float(numbers[0]))
                    if is_number(numbers[1]): nums.append(float(numbers[1]))
                    if op == operator.gt or op == operator.ge:
                        inserter(greater, number, op, operator.gt, operator.ge)
                    else:
                        inserter(less, number, op, operator.lt, operator.le)
    if len(greater) > 0:
        significantGreat = (greater[min(greater)], min(greater))
    else:
        significantGreat = (None, None)
    if len(less) > 0:
        significantLeast = (less[max(less)], max(less))
    else:
        significantLeast = (None, None)
    if significantGreat != (None, None) and significantLeast != (None, None):
        if INVERTED_OPERATORS[significantGreat[0]] == '>' or not is_number(significantGreat[1]):
            lowerBound = significantGreat[1]
        else:
            lowerBound = str(int(significantGreat[1]) - 1)
        if INVERTED_OPERATORS[significantLeast[0]] == '<' or not is_number(significantLeast[1]):
            upperBound = significantLeast[1]
        else:
            upperBound = str(int(significantLeast[1]) + 1)
        reduced = str(lowerBound) + '-' + str(upperBound)
        return reduced.split(',')
    elif significantGreat != (None, None):
        reduced = INVERTED_OPERATORS[significantGreat[0]] + str(significantGreat[1])
        return reduced.split(',')
    elif significantLeast != (None, None):
        reduced = INVERTED_OPERATORS[significantLeast[0]] + str(significantLeast[1])
        return reduced.split(',')
    else:
        return expressionList


def remove_data(dataFrame, column, entry):
    dF = pd.DataFrame(dataFrame)
    matches = pd.DataFrame(dF[dF[column].str.lower().isin(entry)])
    return matches


def remove_nonmatches(dataFrame, entries, columns, tol):
    dF = pd.DataFrame(dataFrame)
    for column in columns:
        dataList = []
        entry = entries[column]
        entry = reduce_expression(entry)
        for e in entry:
            e = e.strip().lower()
            filtered = filter_data(dF, column, e)
            if type(filtered) != pd.DataFrame:
                matches = difflib.get_close_matches(str(e), dF[column].dropna().str.lower().values, cutoff=tol)
                cleared = remove_data(dF, column, matches)
                dataList.append(cleared)
            else:
                dataList.append(filtered)
        dF = pd.DataFrame(pd.concat(dataList, join='inner', axis=0))
    return dF


def read_data(path, dtype='str', columns=None):
    try:
        cols = pd.read_csv(path, nrows=0)
        usecols = [c for c in columns if c in cols.columns]
        return pd.read_csv(path, index_col=ID, usecols=usecols, dtype=dtype, encoding=ENCODING,
                           na_values=NA_VALUES,
                           sep=SEPARATOR)
    except Exception as e:
        print(e)
    try:
        return pd.read_csv(path, dtype=dtype)
    except Exception as e:
        print(e)
    try:
        return pd.read_excel(path)
    except Exception as e:
        print(e)


def query(dataDir, entries, columns=False, tol=1, resultsDir=None):
    resultsList = {}
    filesList = []
    cols = [entry for entry in entries if entries[entry] is not '']
    c = cols if columns else None
    for subdir, dirs, files in os.walk(dataDir):
        for i, file in enumerate(files, start=1):
            try:
                data = read_data(os.path.join(dataDir, file), columns=c)
                results = remove_nonmatches(data, entries, columns=cols, tol=tol)
                if not results.empty:
                    resultsList[file] = (results)
                    results.to_csv('{}{}{}'.format(resultsDir, os.sep, file))
                    filesList.append(file)
            except Exception as e:
                msg = "Error: Couldn't read {0}.\n{1}".format(str(file), str(e))
                print(msg)
    return resultsList, filesList


query(**querySettings)

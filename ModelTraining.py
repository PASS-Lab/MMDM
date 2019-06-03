'''
# memory footprint support libraries/code
!ln -sf /opt/bin/nvidia-smi /usr/bin/nvidia-smi
!pip install gputil
!pip install psutil
!pip install humanize
import psutil
import humanize
import os
import GPUtil as GPU
GPUs = GPU.getGPUs()
# XXX: only one GPU on Colab and isn’t guaranteed
gpu = GPUs[0]
def printm():
 process = psutil.Process(os.getpid())
 print("Gen RAM Free: " + humanize.naturalsize( psutil.virtual_memory().available ), " | Proc size: " + humanize.naturalsize( process.memory_info().rss))
 print("GPU RAM Free: {0:.0f}MB | Used: {1:.0f}MB | Util {2:3.0f}% | Total {3:.0f}MB".format(gpu.memoryFree, gpu.memoryUsed, gpu.memoryUtil*100, gpu.memoryTotal))
printm()
'''

import os

import numpy as np
import tensorflow as tf

tf.set_random_seed(1)
np.random.seed(3)
import numpy as np
import pandas as pd
from sklearn.utils import class_weight
from keras.layers import Dense, Dropout
from keras.optimizers import SGD
from keras import regularizers
from keras import Sequential
from sklearn.svm import SVC
from xgboost import XGBClassifier as XGB
from sklearn.externals import joblib

# AI LIBRARY - sklearn or keras
aiLib = 'xgboost'

# DIRECTORY SETTINGS
testingDir = 'testing'  # 'drive/My Drive/kaggle/PASS Lab/testing'
trainingDir = 'training'  # 'drive/My Drive/kaggle/PASS Lab/training'
modelsDir = {'keras': 'keras_models', 'sklearn': 'sklearn_models', }
modelExt = {'keras': 'h5', 'sklearn': 'joblib', }

lat = 'LAT_016'
long = 'LONG_017'
deck = 'DECK_COND_058'
superstructure = 'SUPERSTRUCTURE_COND_059'
substructure = 'SUBSTRUCTURE_COND_060'
channel = 'CHANNEL_COND_061'
culvert = 'CULVERT_COND_062'
structNum = 'STRUCTURE_NUMBER_008'

# AI SETTINGS
epochs = 100
batchSize = 32  # * 21  # 672
encodeOutput = True if aiLib == 'keras' else True
print('== GLOBAL SETTINGS ==\n'
      ' o aiLib: {}\n'
      ' o epochs: {}\n'
      ' o batchSize: {}\n'
      '====================='.format(aiLib, epochs, batchSize, ))

el = {
    'STRUCTURE_KIND_043A': 10,
    'STRUCTURE_TYPE_043B': 23,
    'DECK_COND_058': 10,
    'DESIGN_LOAD_031': 10,
    'SERVICE_LEVEL_005C': 9,
    'SURFACE_TYPE_108A': 10,
    'DECK_STRUCTURE_TYPE_107': 9,
    'MEMBRANE_TYPE_108B': 10,
    'DECK_PROTECTION_108C': 10
}

categoricalCols = [
    'STRUCTURE_KIND_043A',  # 10 element vector
    'STRUCTURE_TYPE_043B',  # 23 element vector
    # 'STRUCTURE_FLARED_035',
    # 'DECK_STRUCTURE_TYPE_107',
    # 'SURFACE_TYPE_108A',
    # 'MEMBRANE_TYPE_108B',  # Stupid NBI
    # 'SERVICE_LEVEL_005C',
    # 'DECK_PROTECTION_108C',  # Stupid NBI
    # 'PIER_PROTECTION_111',
    # 'DESIGN_LOAD_031',
]
numericalCols = [
    # 'ADT_029',
    # 'YEAR_ADT_030',
    # 'DECK_WIDTH_MT_052',
    # 'MAX_SPAN_LEN_MT_048',
    # 'PERCENT_ADT_TRUCK_109',
    'YEAR_BUILT_027',
    # 'YEAR_RECONSTRUCTED_106',
    # 'LAT_016',
    # 'LONG_017',
    # 'DEGREES_SKEW_034',
    # 'MIN_VERT_CLR_010',
]
con = {
    'DECK_COND_058': 'Deck',
    'SUPERSTRUCTURE_COND_059': 'Superstructure',
    'SUBSTRUCTURE_COND_060': 'Substructure',
    'STRUCTURE_KIND_043A': 'Kind',
    'STRUCTURE_TYPE_043B': 'Type',
    'CHANNEL_COND_061': 'Channel',
    'CULVERT_COND_062': 'Culvert',
    'ADT_029': 'ADT',
    # 'YEAR_ADT_030': '',
    'PERCENT_ADT_TRUCK_109': '% ADT Trucks',
    'YEAR_BUILT_027': 'Year Built',
    'YEAR_RECONSTRUCTED_106': 'Year Reconstructed',
    'LAT_016': 'Latitude',
    'LONG_017': 'Longitude',
    'DECK_WIDTH_MT_052': 'Deck Width (m)',
    'MAX_SPAN_LEN_MT_048': 'Max Span Length (m)',
    'DEGREES_SKEW_034': 'Skew (degrees)',
    'MIN_VERT_CLR_010': 'Min Vertical Clearance (m)',
    'DESIGN_LOAD_031': 'Design Load',
    'SERVICE_LEVEL_005C': 'Service Level',
    'SURFACE_TYPE_108A': 'Surface Type',
    'DECK_STRUCTURE_TYPE_107': 'Deck Type',
    'MEMBRANE_TYPE_108B': 'Membrane Type',
    'DECK_PROTECTION_108C': 'Deck Protection',
}
invcon = {}
for key in con:
    invcon[con[key]] = key
conditionCols = ['DECK_COND_058', 'SUPERSTRUCTURE_COND_059', 'SUBSTRUCTURE_COND_060']

pCols = [structNum, deck] + numericalCols + categoricalCols
cCols = [structNum, deck]


def get_files(path: str, fullPath=True):
    return sorted([os.path.join(path, f) if fullPath else f for f in next(os.walk(path))[2]])


def path_end(path):
    return os.path.basename(os.path.normpath(path))


def strip_ext(filename):
    return filename.split('.')[0]


def encode(item, value):
    s = np.zeros(el[item])
    s[int(value)] = 1
    return s.reshape(1, -1)


def munge(df, year=False):
    encoded = df[~df.index.duplicated(keep='first')]
    for col in encoded.columns:
        if 'Deck' not in col:
            invcol = invcon[col]
            if invcol in el.keys():
                try:
                    encoded[col] = encoded[col].astype(np.int8)
                except:
                    pass
                encoded[col] = pd.Categorical(encoded[col])
                dummies = pd.get_dummies(encoded[col], prefix=col)
                encoded = pd.concat([encoded, dummies], axis=1).drop([col], axis=1)
    if year:
        ecol = encoded.columns
        if 'Year Built' in ecol:
            encoded['Year Built'] = year - encoded['Year Built']
            encoded = encoded.rename(columns={'Year Built': 'Age'})
        if 'Year Reconstructed' in ecol:
            encoded['Year Reconstructed'] = year - encoded['Year Reconstructed']
            encoded = encoded.rename(columns={'Year Reconstructed': 'Last Repair'})
    # result['ADT'] = result['ADT'] / (result['Deck Width (m)'] * result['Max Span Length (m)'])
    # result = result.drop(['Deck Width (m)', 'Max Span Length (m)'], axis=1)
    # 'ADT': 'Capacity',
    # })
    return encoded


def get_model(inputSize, classWeight):
    if aiLib == 'keras':
        model = Sequential()
        model.add(Dense(units=1000,
                        activation='tanh',
                        input_shape=(inputSize,),
                        kernel_initializer='lecun_normal',
                        kernel_regularizer=regularizers.l2(0.01),
                        ))
        model.add(Dropout(rate=0.5))
        model.add(Dense(units=1000,
                        activation='tanh',
                        bias_initializer='lecun_normal',
                        bias_regularizer=regularizers.l2(0.01)
                        ))
        model.add(Dropout(rate=0.5))
        model.add(Dense(units=10, activation='softmax'))
        sgd = SGD(lr=1, clipvalue=0.5, decay=1, momentum=0.5, nesterov=True)
        model.compile(optimizer='adam',
                      loss='categorical_crossentropy')
    elif aiLib == 'sklearn':
        model = SVC(probability=True, class_weight=classWeight)
    elif aiLib == 'xgboost':
        model = XGB(probability=True, class_weight=classWeight,
                    eta=1e-3, objective='multi:softprob', num_class=10,
                    max_depth=20)
    return model


n = []


def read(i, xL, yL, files):
    f = files[i - 1]
    year = int(strip_ext(path_end(f))[-4:])
    _x = pd.read_csv(files[i - 1], usecols=pCols, na_values=['N'] + n).set_index('STRUCTURE_NUMBER_008')
    _x = _x.dropna(axis=0).rename(columns=con).add_suffix('_{}_pre'.format(year))
    _x = _x[~_x.index.duplicated(keep='first')]
    _x.index += '_{}'.format(year)

    _y = pd.read_csv(files[i], usecols=cCols, na_values=['N'] + n).set_index('STRUCTURE_NUMBER_008')
    _y = _y.dropna(axis=0).rename(columns=con).add_suffix('_{}_cur'.format(year))
    _y = _y[~_y.index.duplicated(keep='first')]
    _y.index += '_{}'.format(year)
    master = pd.concat([_y, _x], axis=1, join='inner')
    previous = master[_x.columns].rename(columns=lambda z: str(z)[:-9])
    del _x
    current = master[_y.columns].rename(columns=lambda z: str(z)[:-9])
    del _y
    xL.append(previous)
    yL.append(current)
    return xL, yL


def enter_the_matrix():
    for col in pCols:
        print(col)
    trainFiles = get_files(trainingDir)
    testFiles = get_files(testingDir)
    fullSet = trainFiles + testFiles
    xL, yL = [], []
    for i, _ in enumerate(fullSet):
        if i > 0:
            xL, yL = read(i, xL, yL, fullSet)
    P = munge(pd.concat(xL))
    print(list(P.columns))
    P.drop(['Kind_0', 'Type_0'], axis=1)
    print(list(P.columns))
    C = pd.concat(yL).astype('int8')
    print(len(P.index))
    print(len(C.index))
    '''for row in P.index:
      if C.loc[row, 'Deck'] > P.loc[row, 'Deck']:
        P.drop(row)
        C.drop(row)'''
    P2 = P[P['Deck'] < C['Deck']]
    C2 = C[P['Deck'] < C['Deck']]

    print(len(P2.index))
    print(len(C2.index))
    classWeight = class_weight.compute_sample_weight('balanced', C)
    '''classWeight = class_weight.compute_class_weight('balanced', 
                                                   np.unique(C[C.columns[0]]),
                                                   C)'''
    C = munge(C) if encodeOutput else C

    trainP = P[~P.index.str.contains("_201")]
    trainC = C[~C.index.str.contains("_201")]

    testP = P[~P.index.str.contains("_19")]
    testC = C[~C.index.str.contains("_19")]
    testP = testP[~testP.index.str.contains("_200")]
    testC = testC[~testC.index.str.contains("_200")]
    inputSize = len(trainP.columns)
    trainP, trainC = trainP.to_numpy(), trainC.to_numpy()
    testP, testC = testP.to_numpy(), testC.to_numpy()
    print(inputSize)
    print(len(trainC))
    print(len(testC))
    model = get_model(inputSize=inputSize, classWeight=classWeight)
    model.fit(trainP, trainC)  # , batch_size=32, class_weight=classWeigt, epochs=10)
    joblib.dump(model, "model.joblib.dat")
    print(validate(trainP, trainC, model))
    print(validate(testP, testC, model))


def validate(P, C, model):
    gucci, bacci = [], []
    _p = model.predict_proba(P)
    p = np.vstack([encode(deck, i) for i in np.argmax(_p, axis=1)])
    print(np.unique(p, axis=0))
    c = np.vstack([encode(deck, i[0]) for i in C])
    for a, b in zip(c, p):
        gucci.append(0) if np.array_equal(a, b) else bacci.append(0)
    acc = len(gucci) / (len(gucci) + len(bacci))
    print(len(gucci), len(bacci))
    return acc


enter_the_matrix()

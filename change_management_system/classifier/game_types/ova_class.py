import random as rand
import time
from datetime import datetime
import os
import joblib

import jellyfish as dist
import numpy as np
import pandas as pd
from similarity.jaccard import Jaccard
from similarity.sorensen_dice import SorensenDice
from similarity.weighted_levenshtein import WeightedLevenshtein
from sklearn import svm
from sklearn.multiclass import OneVsRestClassifier

from change_management_system.common.myutil import CharacterSubstitution, calcSimpleScore, distance, printResult, loadOCSVMbySupportVectors, writeSupportVectors

def retryIt(string, f):
        multiSVM = loadOCSVMbySupportVectors('ovaGame' + string + f.__name__)

        test = pd.read_csv('../data/chessboard_games/dataset_set.csv')
        testSamples = test[['Input', 'Output']]
        testSamples = testSamples.apply(lambda x : distance(x, string, f))
        testClasses = test[['Game']]
        
        results = multiSVM.predict(testSamples)

        return calcSimpleScore(testClasses, results, 'Game')


def tryIt(string, randFunction):
        f_name = randFunction[0]
        f = randFunction[1]
        df = pd.read_csv('../data/chessboard_games/dataset.csv')
        X = df[['Input', 'Output']]
        X = X.apply(lambda x: distance(x, string, f))
        y = df['Game']
        _svc = svm.SVC(gamma='auto', probability=True) #SVC()
        clf = OneVsRestClassifier(_svc)
        clf.fit(X, y)

        exists = 0

        if not os.path.exists('models/game_types/ovaclass/'+f_name):
                os.makedirs('models/game_types/ovaclass/'+f_name)
        else:
                exists = exists + 1

        if not os.path.exists('models/game_types/ovaclass/dump/'+f_name):
                os.makedirs('models/game_types/ovaclass/dump/'+f_name)
        else:
                exists = exists + 1
        
        if exists < 1 :      
                joblib.dump(clf, 'models/game_types/ovaclass/dump/'+f_name+'/OVO_SVM_' + string + '.joblib')
                i = 0

                for estimator in clf.estimators_:
                        writeSupportVectors('models/game_types/ovaclass/' + f_name + '/' + str(i) + '_OVO_SVM_' + string + f_name, estimator)
                        i = i + 1



        test = pd.read_csv('../data/chessboard_games/dataset_set.csv')
        testSamples = test[['Input', 'Output']]
        testSamples = testSamples.apply(lambda x : distance(x, string, f))
        testClasses = test[['Game']]
        results = clf.predict(testSamples)

        # writeToFile('multiGame' + string + f.__name__, clf)

        return calcSimpleScore(testClasses, results, 'Game')

# alphabet = 'abcdefghijklmnopqrstuvwxyz' + '0123456789'
# distanceFunctions = [dist.jaro_winkler, dist.levenshtein_distance, Jaccard(4).distance, SorensenDice().distance, dist.damerau_levenshtein_distance, WeightedLevenshtein(CharacterSubstitution()).distance]
# results = []
# for i in range(0,1):
#        line = []
#        randString = ''.join(rand.sample(alphabet,rand.randint(4,20)))
#        for i in range(0, len(distanceFunctions)):
#                randFunction = distanceFunctions[i]
#                distances = []
#                distances.append(randString)
#                distances.append(randFunction)
#                distances.append("{:.4f}".format(tryIt(randString, randFunction)))
#                distances.append("{:.4f}".format(retryIt(randString, randFunction)))
#                line.append(distances)
#        results.append(line)
# print(results)

import subprocess
import os
import json
import csv
import shutil


def runOneExperiment(fileName, arg):
    res = []
    for i in range(10):
        data = str(subprocess.check_output(arg, universal_newlines=True, stderr=subprocess.STDOUT))
        res.append(json.loads(data))

    # headers = ['EvolutionDelay', 'NumberOfEvals', 'Emigrations',
    # 'EvaluatorsCount', 'ReproducersCount', 'IslandsCount', 'BestSol']
    headers = ['EvolutionDelay', 'NumberOfEvals', 'EvaluatorsCount', 'ReproducersCount', 'BestSol']
    fname = fileName + '.csv'
    with open(fname, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(headers)
        for a in res:
            # Convert from ns to ms
            a['EvolutionDelay'] /= 10 ** 6
            row = [a[key] for key in headers]
            spamwriter.writerow(row)


def runParExperiment(arg):
    print('runParExperiment')
    inputConfig = 'configMaxSAT.json'
    for ce in range(1, 31):
        for cr in range(1, 11):
            if ce >= cr:
                print("Calculating with < " + str(ce) + " > evaluators, and < " + str(cr) + " > reproducers")
                conf = json.loads("".join(open(inputConfig).readlines()))
                conf['EvaluatorsCount'] = ce
                conf['ReproducersCount'] = cr
                w = open(inputConfig, 'w+')
                w.write(json.dumps(conf))
                w.close()
                runOneExperiment(
                    './results/parResults_' + str(conf['EvaluatorsCount']) + '_' + str(
                        conf['EvaluatorsCapacity']) + '_' + str(
                        conf['ReproducersCount']) + '_' + str(conf['ReproducersCapacity']), arg)


def runSeqExperiment(arg):
    print('runSeqExperiment')
    fileName = './results/seqResults'
    res = []
    for i in range(10):
        data = str(subprocess.check_output(arg, universal_newlines=True, stderr=subprocess.STDOUT))
        res.append(json.loads(data))

    headers = ['EvolutionDelay', 'BestSol']
    fname = fileName + '.csv'
    with open(fname, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(headers)
        for a in res:
            # Convert from ns to ms
            a['EvolutionDelay'] /= 10 ** 6
            row = [a[key] for key in headers]
            spamwriter.writerow(row)


def goExperiment():
    os.chdir("D:/Mis Documentos/PhD/src/goEA/src/mainEA")
    if os.path.exists('results'):
        shutil.rmtree('results')
    os.mkdir('results')
    runSeqExperiment(["mainEA.exe", 'sfq'])
    runParExperiment(["mainEA.exe", 'pfq'])


def javaExperiment():
    os.chdir("D:/Mis Documentos/PhD/src/jEA/out/artifacts/jEA_jar")
    if os.path.exists('results'):
        shutil.rmtree('results')
    os.mkdir('results')
    runSeqExperiment(["java", '-jar', 'jEA.jar', 'sfq'])
    runParExperiment(["java", '-jar', 'jEA.jar', 'pfq'])


def cljExperiment():
    os.chdir("D:/Mis Documentos/PhD/src/cljEA/pools-based-ea/target/uberjar")
    if os.path.exists('results'):
        shutil.rmtree('results')
    os.mkdir('results')
    runSeqExperiment(["java", '-jar', 'pools-based-ea-0.1.0-SNAPSHOT-standalone.jar', 'sfq'])
    runParExperiment(["java", '-jar', 'pools-based-ea-0.1.0-SNAPSHOT-standalone.jar', 'pfq'])


def sclExperiment():
    os.chdir("D:/Mis Documentos/PhD/src/sclEA/out/artifacts/PoolsBasedEA_jar")
    if os.path.exists('results'):
        shutil.rmtree('results')
    os.mkdir('results')
    runSeqExperiment(["java", '-jar', 'PoolsBasedEA.jar', 'sfq'])
    runParExperiment(["java", '-jar', 'PoolsBasedEA.jar', 'pfq'])


#goExperiment()
#sclExperiment()
#cljExperiment()
javaExperiment()
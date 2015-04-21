import subprocess
import os
import json
import shutil
import csv

reproducers = [1, 2]
evaluators = [2, 4, 8, 16, 32]


def runParExperiments(home, cmds):
    os.chdir(home)
    conf = json.loads("".join(open("baseConfig.json").readlines()))
    for rc in reproducers:
        for ec in evaluators:
            conf["evaluatorsCount"] = ec
            conf["reproducersCount"] = rc
            conf["parallelOutputFilename"] = './results/parResults' + '_' + str(conf["evaluatorsCount"]) + "_" + str(
                conf["evaluatorsCapacity"]) + "_" + str(conf["reproducersCount"]) + "_" + str(
                conf["reproducersCapacity"]) + ".csv"
            open('maxSATConfig.json', 'w').write(json.dumps(conf))
            subprocess.call(cmds)


def runSeqExperiments(home, cmds):
    os.chdir(home)
    conf = json.loads("".join(open("baseConfig.json").readlines()))
    conf["seqOutputFilename"] = './results/seqResults.csv'
    open('maxSATConfig.json', 'w').write(json.dumps(conf))
    subprocess.call(cmds)


def runScala():
    runSeqExperiments('D:/MisDocumentos/PhD/src/sclEA/out/artifacts/Pool_Island_jar',
                      ["java", '-jar', 'Pool-Island.jar', 'seq'])
    runParExperiments('D:/MisDocumentos/PhD/src/sclEA/out/artifacts/Pool_Island_jar',
                      ["java", '-jar', 'Pool-Island.jar', 'par'])


def runClojure():
    runSeqExperiments('D:/MisDocumentos/PhD/src/cljEA/out/artifacts/Pool_Island_jar',
                      ["java", '-jar', 'Pool-Island.jar', 'seq'])
    runParExperiments('D:/MisDocumentos/PhD/src/cljEA/out/artifacts/Pool_Island_jar',
                      ["java", '-jar', 'Pool-Island.jar', 'par'])


def runSeqExperimentCombiningFromPython(arg):
    print('runSeqExperiment')
    fileName = './results/seqResults'
    res = []
    for i in range(30):
        data = str(subprocess.check_output(arg, universal_newlines=True, stderr=subprocess.STDOUT))
        res.append(json.loads(data))

    headers = ['EvolutionDelay', 'BestSol', 'Evaluations']
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


def runOneExperimentCombiningFromPython(fileName, arg):
    res = []
    for i in range(30):
        data = str(subprocess.check_output(arg, universal_newlines=True, stderr=subprocess.STDOUT))
        res.append(json.loads(data))

    headers = ['EvolutionDelay', 'Evaluations', 'Emigrations', 'EvaluatorsCount', 'ReproducersCount', 'IslandsCount',
               'BestSol']
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


def runParExperimentCombiningFromPython(arg):
    print('runParExperiment')
    inputConfig = 'configMaxSAT.json'
    for ce in evaluators:
        for cr in reproducers:
            print("Calculating with < " + str(ce) + " > evaluators, and < " + str(cr) + " > reproducers")
            conf = json.loads("".join(open(inputConfig).readlines()))
            conf['EvaluatorsCount'] = ce
            conf['ReproducersCount'] = cr
            w = open(inputConfig, 'w+')
            w.write(json.dumps(conf))
            w.close()
            runOneExperimentCombiningFromPython(
                './results/parResults_' + str(conf['EvaluatorsCount']) + '_' + str(
                    conf['EvaluatorsCapacity']) + '_' + str(
                    conf['ReproducersCount']) + '_' + str(conf['ReproducersCapacity']), arg)


def runGo():
    os.chdir("D:/MisDocumentos/PhD/src/goEA/src/mainEA")
    if os.path.exists('results'):
        shutil.rmtree('results')
    os.mkdir('results')
    runSeqExperimentCombiningFromPython(["mainEA.exe", 'seq'])
    runParExperimentCombiningFromPython(["mainEA.exe", 'par'])

runScala()
# runClojure()
# runGo()
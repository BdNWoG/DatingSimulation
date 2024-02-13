import random
import numpy as np
import pandas as pd
import os  

os.makedirs('/Users/billygao/Documents/GitHub/DatingSimulation', exist_ok=True)  

data = {"New?": [1], "Actual Self": [1], "Perceived Self": [1], "character": [1], "Actual Other": [1], "Perceived Other": [1], 
        "Ideal Other": [1], "Max Accept Range": [1], "Min Accept Range": [1], "Other Character": [1], "Other Self Eval": [1], 
        "Other Accept Min": [1], "Other Accept Max": [1], "Other Eval Self": [1], "Outcome from Self": [1], "Outcome from Other": [1], 
        "Overall Outcome": [1], "Perceived Reward": [1], "Actual Reward": [1]} 
#yes or not new person, actual self rating, perceived self, actual other, perceived other, idealother, acceptMax, 
#acceptMin, selfOutcome, otherOutcome, change

df = pd.DataFrame(data)

def charac():
    return np.random.normal(0.1, 0.02)

def actualSelf():
    return random.randint(0, 100)

def selfEval(actualSelf):
    return np.random.normal(actualSelf, 7)

def otherEval(actualOther):
    return np.random.normal(actualOther, 11)

def maxAccept(idealOther):
    return idealOther

def minAccept(selfEval, idealOther, charac):
    return selfEval - (idealOther - selfEval)*charac

def changeSelfEval(selfEval, otherEval, charac):
    return selfEval - (otherEval - selfEval)*charac

def changeIdealOther(idealOther, seflEval, charac):
    return idealOther - (idealOther - seflEval)*charac

def changeMinAccept(minAccept, otherEval, selfEval, charac):
    return minAccept - (otherEval - selfEval)*charac

def changeMaxAccept(maxAccept, otherEval, selfEval, charac):
    return maxAccept - (otherEval - selfEval)*charac

rowlist = []

for i in range(0, 1):
    
    print(i)
    idealOther = 100
    matched = False
    new = True
    character = charac()
    selfActual = actualSelf()
    evalSelf = selfEval(selfActual)
    acceptMax = maxAccept(idealOther)
    acceptMin = minAccept(evalSelf, idealOther, character)

    while (not matched):
        
        otherActual = actualSelf()
        evalOther = otherEval(otherActual)
        otherCharacter = charac()
        otherAcceptMax = maxAccept(idealOther)
        otherAcceptMin = minAccept(evalOther, idealOther, otherCharacter)
        otherSelfEval = selfEval(otherActual)
        otherEvalSelf = otherEval(selfActual)

        if (acceptMin <= evalOther and evalOther <= acceptMax):
            selfOutcome = True

            if (otherAcceptMin <= otherEvalSelf and otherEvalSelf <= otherAcceptMax):
                otherOutcome = True
                matched = True
                perceivedReward = evalOther - evalSelf
                actualReward = otherActual - selfActual

            else:
                otherOutcome = False
                perceivedReward = - character * (evalOther - evalSelf)
                actualReward = - character * (otherActual - selfActual)

        else:
            selfOutcome = False
            if (acceptMin > evalOther):
                otherOutcome = True
                perceivedReward = character * (evalSelf - evalOther)
                actualReward = character * (selfActual - otherActual)

            else:
                otherOutcome = False #separate
                perceivedReward = - character * character * (evalOther - evalSelf)
                actualReward = - character * character * (otherActual - selfActual)
        
        rowlist.append([[new, selfActual, evalSelf, character, otherActual, evalOther, idealOther, acceptMax, acceptMin, 
                                    otherCharacter, otherSelfEval, otherAcceptMin, otherAcceptMax, otherEvalSelf, selfOutcome, 
                                    otherOutcome, (selfOutcome==True and otherOutcome==True), perceivedReward, actualReward]], columns=df.columns)

        if (selfOutcome==True and otherOutcome==False):
            evalSelf = changeSelfEval(evalSelf, evalOther, character)
            idealOther = changeIdealOther(idealOther, evalSelf, character)
            acceptMin = changeMinAccept(acceptMin, evalOther, evalSelf, character)
            acceptMax = idealOther

        if (selfOutcome==False and otherOutcome==True):
            evalSelf = changeSelfEval(evalSelf, evalOther, character)
            acceptMin = changeMinAccept(acceptMin, evalOther, evalSelf, character)

        if (selfOutcome==False and otherOutcome==False):
            evalSelf = changeSelfEval(evalSelf, evalOther, character)
            acceptMax = changeMaxAccept(acceptMax, evalOther, evalSelf, character)

        new = False

df = pd.DataFrame(rowlist)
df.to_csv('/Users/billygao/Documents/GitHub/DatingSimulation/Datingv5.csv', index=False)
os.chdir('/Users/billygao/Documents/GitHub/DatingSimulation')
df_saved_file = pd.read_csv('Datingv5.csv')
print(df_saved_file)

import random
import numpy as np
import pandas as pd
import os
import math

unmar = 0
n = 100000
m = 30

# Create the directory if it doesn't exist
directory_path = '/Users/billygao/Documents/GitHub/DatingSimulation'
os.makedirs(directory_path, exist_ok=True)

# Define the functions
def charac():
    return np.random.normal(0.1, 0.015)

def actualSelf():
    return random.randint(0, 100)

def selfEval(actualSelf):
    return np.random.normal(actualSelf, 6)

def otherEval(actualOther):
    return np.random.normal(actualOther, 9)

def maxAccept(idealOther):
    return idealOther

def minAccept(selfEval, idealOther, charac):
    return selfEval - (idealOther - selfEval) * charac

def changeSelfEval(selfEval, otherEval, charac, att):
    if otherEval > selfEval:
        return selfEval - pow((otherEval - selfEval), 1/(1+charac)) * charac * (50 - abs(50-selfEval))/50 * pow(1+charac, att)
    else:
        return selfEval + pow((selfEval - otherEval), 1/(1+charac)) * charac * (50 - abs(50-selfEval))/50 * pow(1+charac, att)
    #decrease should be modeled better (2 case) [sqrt]

def changeIdealOther(idealOther, selfEval, charac):
    return idealOther - (idealOther - selfEval) * charac

def changeMinAccept(minAccept, otherEval, selfEval, charac, att):
    if otherEval > selfEval:
        return minAccept - (otherEval - selfEval) * charac * pow(1+charac, att)
    else:
        if (minAccept - (otherEval - selfEval) * charac * pow(1-charac, att)) > selfEval:
            return selfEval
        else: 
            return minAccept - (otherEval - selfEval) * charac * pow(1-charac, att)

def changeMaxAccept(maxAccept, otherEval, selfEval, charac, att):
    if otherEval > selfEval:
        if (maxAccept - (otherEval - selfEval) * charac * pow(1+charac, att)) < selfEval:
            return selfEval
        else: 
            return maxAccept - (otherEval - selfEval) * charac * pow(1+charac, att)
    else:
        return maxAccept - (otherEval - selfEval) * charac * pow(1-charac, att)
    
# Initialize a list to hold data rows
data_rows = []

# Adjust the range as needed for multiple iterations
for i in range(n):  # Example: running the simulation once for testing
    matched = False
    new = True
    character = charac()
    selfActual = actualSelf()
    evalSelf = selfEval(selfActual)
    idealOther = 100
    acceptMax = maxAccept(idealOther)
    acceptMin = minAccept(evalSelf, idealOther, character)
    attempt = 0
    # Prevent infinite loop

    while not matched and attempt < m:
        attempt += 1
        otherActual = actualSelf()
        evalOther = otherEval(otherActual)
        otherCharacter = charac()
        otherAcceptMax = maxAccept(100)
        otherAcceptMin = minAccept(evalOther, 100, otherCharacter)
        otherSelfEval = selfEval(otherActual)
        otherEvalSelf = otherEval(selfActual)

        # Determine if there is a match
        selfOutcome = acceptMin <= evalOther <= acceptMax
        otherOutcome = otherAcceptMin <= otherEvalSelf <= otherAcceptMax
        matched = selfOutcome and otherOutcome

        perceivedReward = evalOther - evalSelf if matched else -character * (evalOther - evalSelf)
        actualReward = otherActual - selfActual if matched else -character * (otherActual - selfActual)

        data_rows.append({
            "New?": new, "Actual Self": round(selfActual, 0), "Perceived Self": round(evalSelf, 0), "Character": round(character, 2),
            "Actual Other": round(otherActual, 0), "Perceived Other": round(evalOther, 0), "Ideal Other": round(idealOther, 0),
            "Max Accept Range": round(acceptMax, 0), "Min Accept Range": round(acceptMin, 0), "Other Character": round(otherCharacter, 2),
            "Other Self Eval": round(otherSelfEval, 0), "Other Accept Min": round(otherAcceptMin, 0), "Other Accept Max": round(otherAcceptMax, 0),
            "Other Eval Self": round(otherEvalSelf, 0), "Outcome from Self": selfOutcome, "Outcome from Other": otherOutcome,
            "Overall Outcome": matched, "Perceived Reward": round(perceivedReward, 0), "Actual Reward": round(actualReward, 0), "Attempt": attempt
        })

        # Update for next attempt if not matched
        if not matched:
            evalSelf = changeSelfEval(evalSelf, evalOther, character, attempt)
            idealOther = changeIdealOther(idealOther, evalSelf, character)
            acceptMin = changeMinAccept(acceptMin, evalOther, evalSelf, character, attempt)
            acceptMax = changeMaxAccept(acceptMax, evalOther, evalSelf, character, attempt)
            new = False
            if attempt == m:
                unmar += 1

# Create DataFrame from the collected rows
df = pd.DataFrame(data_rows)

# Save the DataFrame to CSV
csv_file_path = os.path.join(directory_path, 'DatingSimulationResultsNew2.csv')
df.to_csv(csv_file_path, index=False)

# Optional: Load and print the DataFrame to verify
df_saved_file = pd.read_csv(csv_file_path)
print(df_saved_file)
print("Unmarried = ", round(unmar/n, 2))

import random
import os
import time
from colorama import Fore, Style
import math
from jsonData import BaseAlreadyExistsError, DateAlreadyExistsError, DigitGroupAlreadyExistsError, add_base, save_data, load_data, add_date, add_digits
import datetime

def clear_console():
    os.system('clear')


def start():
    while(1):

        mode = input(
            "Modes: \n\n"
            "1 - addition \n"
            "2 - subtraction \n"
            "3 - addition and subtraction \n"
            "4 - multiplication \n"
            "5 - division \n"
            "6 - multiplication and division \n"
            "7 - all inculded \n"
            "\nChoose mode: "
            )

        try:
            mode = int(mode)
            if(mode >= 1 and mode <=9):
                break
        except ValueError:
            pass

        clear_console()
        print("\n Invalid input, try again \n")

    return mode


def float_dec_to_base(num, base, percision):

    base = int(base)
    convertedNum = ''

    hexadecimalDict = {
        10:'a',
        11:'b',
        12:'c',
        13:'d',
        14:'e',
        15:'f'
    }

    # get amount of digits after floating point
    digits = math.floor(-math.log(num, base))
    wrongNum = 0

    for i in range(digits, percision+1):

        # get digit
        digit = int(num*base**i) % base

        if base > 10 and base < 17:
            if digit in hexadecimalDict:
                digit = hexadecimalDict[digit]
        elif base > 16:
            digit = ' ' + str(digit)

        if i == 1:
            convertedNum += '.'

        convertedNum = convertedNum + str(digit)

        # print("Digit: ")
        # print(digit)
        # print("Digit context: ")
        # print(int(num*base**i) % base * 10**(-i))
        # print("Converted Num: ")
        # print(convertedNum)
        # print("Old calculation: ")
        # wrongNum = wrongNum + int(num*base**i) % base * 10**(-i)
        # print(wrongNum)
        # print("\n")
    print(convertedNum)


    """FORMATTING RESULT"""

    # FOR LARGER BASES remove trailing space after .
    if base > 16:
        floatingPointIndex = convertedNum.find(".")
        convertedNum = convertedNum[:floatingPointIndex+1] + convertedNum[floatingPointIndex+2:]

    #check if number starts with 0
    while (convertedNum[0] == '0' and convertedNum[1] != '.') or convertedNum[0] == ' ':
        convertedNum = convertedNum[1:]

    # remove trailing 0s
    while convertedNum[-1] == '0' or convertedNum[-1] == '':
        convertedNum = convertedNum[:-1]

    # check if number doesnt need a floating point
    if convertedNum[-1] == '.':
        convertedNum = convertedNum[:-1]


    return convertedNum


def int_dec_to_base(decInt, base):

    base = int(base)

    if(decInt == 0):
        return '0'

    hexadecimalDict = {
        10:'a',
        11:'b',
        12:'c',
        13:'d',
        14:'e',
        15:'f'
    }

    convertedNum = ""

    while(decInt > 0):
        remainder = decInt % base
        decInt = int(decInt / base)
        if(base <= 16):

            if(remainder in hexadecimalDict):
                remainder = hexadecimalDict[remainder]

            convertedNum = str(remainder) + convertedNum
        else:
            convertedNum = str(remainder) + " " + convertedNum

    # remove trailing spaces for bases > 16
    convertedNum = convertedNum.rstrip()

    return convertedNum


def int_input(min, max, msg):

    while(1):
        var = input(msg)
        try:
            var = int(var)
            if(var >= min and var <= max):
                break

        except ValueError:
            pass

    return var


# Choose base
base = int_input(2, math.inf, "Base: ")

# get min, max Rng
maxRng = int_input(1, math.inf, "Max RNG: ")
minRng = int_input(1, math.inf, "Min RNG: ")

if maxRng < minRng:
    minRng, maxRng = maxRng, minRng

# fetch stats
fileName = "stats.json"
date = datetime.datetime.now().strftime('%Y-%m-%d')

stats = load_data(fileName)

base = str(base)

# create date entry if doesnt exist
try:
    stats = add_date(base, stats)
    save_data(fileName, stats)

except DateAlreadyExistsError:
    pass

# get todays stats
roundsPlayed = stats["bases"][base][date]["all"]["rounds_played"]
averageTime = stats["bases"][base][date]["all"]["average_time"]
successRate = stats["bases"][base][date]["all"]["success_rate"]
playTime = stats["bases"][base][date]["all"]["total_time"]

correctAnswers = roundsPlayed * successRate
bestTime = None


# Choose operations and start
mode = start()
clear_console()

#loop
while(1):

    # determine operand
    if(mode == 1):
        operand = '+'
    elif(mode == 2):
        operand = '-'
    elif(mode == 3):
        if(random.randint(0, 1)):
            operand = '+'
        else:
            operand = '-'
    elif(mode == 4):
        operand = '*'
    elif(mode == 5):
        operand = '/'
    elif(mode == 6):
        if(random.randint(0, 1)):
            operand = '*'
        else:
            operand = '/'
    elif(mode == 7):
        num = random.randint(0, 3)
        if(num == 0):
            operand = '+'
        elif(num == 1):
            operand = '-'
        elif(num == 2):
            operand = '*'
        else:
            operand = '/'

    # generate nums
    num1 = random.randint(minRng, maxRng)
    num2 = random.randint(minRng, maxRng)

    # avoid negative answers
    if(operand == '-' and num1 < num2):
        num3 = num1
        num1 = num2
        num2 = num3

    # convert nums to base
    convertedNum1 = int_dec_to_base(num1, base)
    convertedNum2 = int_dec_to_base(num2, base)

    # start recording time
    start = time.time()

    # ask question
    userAnswer = input(
        "Round : " + str(roundsPlayed + 1) + "\n" +
        "Best t: " + str(bestTime) + "\n" +
        "AVRG t: " + str(averageTime) + "\n" +
        "W Rate: " + str(successRate * 100) + "%"
        "\n\n" +
        convertedNum1 + " " + operand + " " + convertedNum2 + " = "
    )

    # get answer in decimal
    if(operand == '+'):
        answer = num1 + num2
    elif(operand == '-'):
        answer = num1 - num2
    elif(operand == '*'):
        answer = num1 * num2
    elif(operand == '/'):
        answer = num1 / num2

    # convert answer to base
    if(operand == '/'):
        answer = float_dec_to_base(answer, base, 4)
    else:
        answer = int_dec_to_base(answer, base)

    # calculate stats
    isCorrect = False

    roundsPlayed += 1
    timeTaken = time.time() - start

    # answer is correct
    if(userAnswer == answer):

        isCorrect = True

        if(bestTime is None):
            bestTime = timeTaken
        elif(bestTime > timeTaken):
            bestTime = timeTaken

        playTime += timeTaken
        correctAnswers += 1
        averageTime = playTime/correctAnswers
        print(Fore.GREEN + "Correct answer!")
    else:
    # answer is wrong
        print(Fore.RED + "Wrong! Answer was " + answer)

    successRate = correctAnswers/roundsPlayed

    # colour green if answer time is less than avrg time and red if >
    if(timeTaken > averageTime and averageTime > 0):
        colour = Fore.RED
    else:
        colour = Fore.GREEN
    print(colour + str(timeTaken))
    print(Style.RESET_ALL)

    # log stats
    action = "all"

    # update date for all actions
    stats["bases"][base][date][action]["rounds_played"] = roundsPlayed
    stats["bases"][base][date][action]["average_time"] = averageTime
    stats["bases"][base][date][action]["success_rate"] = successRate
    stats["bases"][base][date][action]["total_time"] = playTime

    # update alltime for all actions
    stats["bases"][base]["alltime"][action]["rounds_played"] += 1
    stats["bases"][base]["alltime"][action]["total_time"] += timeTaken
    stats["bases"][base]["alltime"][action]["average_time"] = stats["bases"][base][date][action]["total_time"] / stats["bases"][base][date][action]["rounds_played"]
    stats["bases"][base]["alltime"][action]["success_rate"] = (( (stats["bases"][base]["alltime"][action]["rounds_played"]-1) * stats["bases"][base]["alltime"][action]["success_rate"]) + isCorrect) / stats["bases"][base]["alltime"][action]["rounds_played"]



    if(operand == '+'):
        action = "addition"
    elif(operand == '-'):
        action = "subtraction"
    elif(operand == '*'):
        action = "multiplication"
    else:
        action = "division"

    # update date for specific action
    stats["bases"][base][date][action]["rounds_played"] += 1
    stats["bases"][base][date][action]["total_time"] += timeTaken
    stats["bases"][base][date][action]["average_time"] = stats["bases"][base][date][action]["total_time"] / stats["bases"][base][date][action]["rounds_played"]
    stats["bases"][base][date][action]["success_rate"] = (( (stats["bases"][base][date][action]["rounds_played"]-1) * stats["bases"][base][date][action]["success_rate"]) + isCorrect) / stats["bases"][base][date][action]["rounds_played"]


    # update global for specific action
    stats["bases"][base]["alltime"][action]["rounds_played"] += 1
    stats["bases"][base]["alltime"][action]["total_time"] += timeTaken
    stats["bases"][base]["alltime"][action]["average_time"] =  stats["bases"][base]["alltime"][action]["total_time"] / stats["bases"][base]["alltime"][action]["rounds_played"]
    stats["bases"][base]["alltime"][action]["success_rate"] = (( (stats["bases"][base]["alltime"][action]["rounds_played"]-1) * stats["bases"][base]["alltime"][action]["success_rate"]) + isCorrect) / stats["bases"][base]["alltime"][action]["rounds_played"]


    # update digit info

    if len(str(num1)) == len(str(num2)):
        # nums have to be the same length else it feels inaccurate, example 100+1
        # TODO alternatively store the digits of num 1 and 2 to be more percise, 25+100 would be 2-3, 100+100: 3-3. Have to reverse mirror cases, but it matters when dividing?
        
        keyName = "1"
        for i in range(1, len(str(num1))):
            keyName += "0"  
        keyName = keyName + "-" + keyName + "0"

        if keyName not in stats["bases"][base][date]["all"]:
            stats = add_digits(base, stats, len(str(num1)))


        #update date for global actions
        savePrevAction = action
        action = "all"
 
        stats["bases"][base][date]["all"][keyName]["rounds_played"] += 1
        stats["bases"][base][date][action][keyName]["total_time"] += timeTaken
        stats["bases"][base][date][action][keyName]["average_time"] =  stats["bases"][base][date][action][keyName]["total_time"] / stats["bases"][base][date][action][keyName]["rounds_played"]
        stats["bases"][base][date][action][keyName]["success_rate"] = (( (stats["bases"][base][date][action][keyName]["rounds_played"]-1) * stats["bases"][base][date][action][keyName]["success_rate"]) + isCorrect) / stats["bases"][base][date][action][keyName]["rounds_played"]

        if stats["bases"][base][date][action][keyName]["best_time"] is None or stats["bases"][base][date][action][keyName]["best_time"] > timeTaken:
            stats["bases"][base][date][action][keyName]["best_time"] = timeTaken

        # update alltime for global actions
        stats["bases"][base]["alltime"][action][keyName]["rounds_played"] += 1
        stats["bases"][base]["alltime"][action][keyName]["total_time"] += timeTaken
        stats["bases"][base]["alltime"][action][keyName]["average_time"] =  stats["bases"][base]["alltime"][action][keyName]["total_time"] / stats["bases"][base]["alltime"][action][keyName]["rounds_played"]
        stats["bases"][base]["alltime"][action][keyName]["success_rate"] = (( (stats["bases"][base]["alltime"][action][keyName]["rounds_played"]-1) * stats["bases"][base]["alltime"][action][keyName]["success_rate"]) + isCorrect) / stats["bases"][base]["alltime"][action][keyName]["rounds_played"]


        if stats["bases"][base]["alltime"][action][keyName]["best_time"] is None or stats["bases"][base]["alltime"][action][keyName]["best_time"] > timeTaken:
            stats["bases"][base]["alltime"][action][keyName]["best_time"] = timeTaken

        # update date for specific action
        action = savePrevAction

        stats["bases"][base][date][action][keyName]["rounds_played"] += 1
        stats["bases"][base][date][action][keyName]["total_time"] += timeTaken
        stats["bases"][base][date][action][keyName]["average_time"] =  stats["bases"][base][date][action][keyName]["total_time"] / stats["bases"][base][date][action][keyName]["rounds_played"]
        stats["bases"][base][date][action][keyName]["success_rate"] = (( (stats["bases"][base][date][action][keyName]["rounds_played"]-1) * stats["bases"][base][date][action][keyName]["success_rate"]) + isCorrect) / stats["bases"][base][date][action][keyName]["rounds_played"]


        if stats["bases"][base][date][action][keyName]["best_time"] is None or stats["bases"][base][date][action][keyName]["best_time"] > timeTaken:
            stats["bases"][base][date][action][keyName]["best_time"] = timeTaken

        # update alltime for specific action

        stats["bases"][base]["alltime"][action][keyName]["rounds_played"] += 1
        stats["bases"][base]["alltime"][action][keyName]["total_time"] += timeTaken
        stats["bases"][base]["alltime"][action][keyName]["average_time"] =  stats["bases"][base]["alltime"][action][keyName]["total_time"] / stats["bases"][base]["alltime"][action][keyName]["rounds_played"]
        stats["bases"][base]["alltime"][action][keyName]["success_rate"] = (( (stats["bases"][base]["alltime"][action][keyName]["rounds_played"]-1) * stats["bases"][base]["alltime"][action][keyName]["success_rate"]) + isCorrect) / stats["bases"][base]["alltime"][action][keyName]["rounds_played"]


        if stats["bases"][base]["alltime"][action][keyName]["best_time"] is None or stats["bases"][base]["alltime"][action][keyName]["best_time"] > timeTaken:
            stats["bases"][base]["alltime"][action][keyName]["best_time"] = timeTaken

    # save data and repeat

    save_data(fileName, stats)

    time.sleep(1)

    clear_console()

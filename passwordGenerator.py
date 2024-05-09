# returns a password with a random prime number length between 0 and 100. Conducts divisibility tests on random numbers
# until prime is found. Password checks if there are two of the same characters next to it and generates a new pwd if so.
# also checks if any two consecutive characters are consecutive in ASCII using the ord command.  As a result, no password can have ex abc
# 4/8/24

import time, math, logging, subprocess, os, json, secrets, random, subprocess
import numpy as np
import sys

from PyJavaRunner import javaProgram

sys.path.append("..")  # Add the parent directory to the Python path

# creates blank line of space
def newprintLn():
    print("\n----------------------\n")


# copies text to clipboard for ease of use
def copyToClipboard(txt):
    cmd = "echo " + txt.strip() + "|clip"
    return subprocess.check_call(cmd, shell=True)


# finds random prime number for len
def primeNumGen():
    check = True
    while True:
        num = random.randint(10, 100)
        # print(f'\n\033[34mTrying Number: {num}\033[0m')
        for j in range(2, num // 2 + 1):
            if num % j == 0:
                # print(f"\033[31mNumber fails divisibility test of {j}\033[0m")
                check = False
                break
        if check:
            print(f"\033[32mPrime Number Found: {num}\033[33m")
            print(f"Generating Password of length {num}...\033[0m")
            newprintLn()
            return num
        else:
            check = True


# creates password using sets of characters and pwd length found by primeNumGen
def pwdCreation(num):
    # global variables
    letters = "abcdefghijklmnopqrstuvwxyz"
    numbers = "1234567890"
    statusDict = {True: "\033[32mAPPROVED\033[0m", False: "\033[31mFAILED\033[0m"}
    while True:
        pwd = []
        prev_type = None
        consecutive_count = 0
        for i in range(num):
            while True:
                case = secrets.randbelow(3)
                if case == 0 and (
                    prev_type != 0 or consecutive_count < 3
                ):  # Check if the previous character was not a number or consecutive count is less than 3
                    pwd.append(numbers[random.randint(0, 9)])
                    prev_type = 0
                    consecutive_count = 0 if prev_type != 0 else consecutive_count + 1
                    break
                elif case == 1 and (
                    prev_type != 1 or consecutive_count < 3
                ):  # Check if the previous character was not a lowercase letter or consecutive count is less than 3
                    pwd.append(letters[random.randint(0, 25)])
                    prev_type = 1
                    consecutive_count = 0 if prev_type != 1 else consecutive_count + 1
                    break
                elif case == 2 and (
                    prev_type != 2 or consecutive_count < 3
                ):  # Check if the previous character was not an uppercase letter or consecutive count is less than 3
                    pwd.append(letters[random.randint(0, 25)].upper())
                    prev_type = 2
                    consecutive_count = 0 if prev_type != 2 else consecutive_count + 1
                    break

        if pwdCheckCons(pwd, num, statusDict):
            break

    pwdf = "".join(pwd)
    ans = input(
        f'\nComputer has created a secure password. Would you like to use: "{pwdf}" as the password? (Y or N) '
    ).upper()
    if ans == "Y":
        # passwordlist.append(pwdf)
        # print(f'\n-------------\nFinal Password Generated:')
        # print(f"\033[32m{pwdf}\033[0m")
        return pwdf
    elif ans == "N":
        pwdCreation(num)

    else:
        print("\n Invalid Response.\n \033[033m Generating new password... \033[0m")
        pwdCreation(num)

    return pwdf


# asigns password to program
def pwdAppend1(pwdf):
    prog = input("\nWhat program would you like to assign the password to? ")
    uname = input("\nWhat is the username? ")
    passwordManager[prog.upper()] = [uname, pwdf]
    print(
        f"\033[32mPassword ({pwdf}) added to password manager under program ({prog.upper()})\033[0m"
    )


# allows user to add full login info
def pwdAppend2():
    prog = input("\nWhat program would you like to assign the password to? ")
    uname = input("\nWhat is the username? ")
    pwd = input("\nType in the password to be added: ")
    # pwdE = encryptPassword(pwd)
    passwordManager[prog.upper()] = [uname, pwd]
    print(
        f"\033[32mPassword ({pwd}) added to password manager under program ({prog.upper()})\033[0m"
    )
    return prog


def f(x):
    try:
        return round(abs(np.sqrt(x + 0.3 * np.log(x + 0.01)) - 0.308), 2)
    except RuntimeWarning:
        pass


def s(x):
    if x == 150:
        return 10
    return round((f(x) - 2.96) * (125 / 113), 5)


def commonWordsScore(pwd):
    if not checkCommonWords2(pwd) or not pwd == "" or not pwd == " ":
        s = 10
    else:
        s = 0
    return s

def charDistScore(pwd, printing):
    if not checkCommonWords2(pwd) or pwd == "":
        print("\033[31mWARNING: COMMON PASSWORD\033[0m")
        return 0, 0
    
    #redundancy in case of code error
    score, diC, upC, lcC  = 0, 0, 0, 0
    
    #calculates password
    threshold = int(len(pwd) / 3)

    # runs java file function and gets results
    diC,upC,lcC = javaProgram(pwd)
   

    # calculates password score based upon the frequency of each type of character
    differences = (abs(threshold - diC), abs(threshold - upC), abs(threshold - lcC))
    totalQuant = round(float(sum(differences) / len(pwd)), 4) * 100
    score = max(0, 100 - totalQuant)

    if printing == 1:
        print(f"\nintC: {diC/len(pwd)*100}%")
        print(f"upC: {upC/len(pwd)*100}%")
        print(f"lwC: {lcC/len(pwd)*100}%")
        # print(f"Differences: {differences}")
        (a, time) = calculatePasswordEntropy(pwd)
        print(f"Password Entropy: {a} in time {time} seconds")
        
    return round(score, 3), time 

def findPWDInfo(pwd):
    lenVal = s(len(pwd))
    commonWS = commonWordsScore(pwd)
    charDS,time = charDistScore(pwd,1)
    cDS = round(charDS/10)
    print(f"LENV = {lenVal}\ncommonWS = {commonWS}\ncharDS = {cDS}")
    return max(lenVal*3.3 + commonWS*3.4 + cDS*3.4,0), time, 



# check password strength
def checkStrength(pwd, printing):
    strength,time = findPWDInfo(pwd)
    print(f"2 Score Total: {strength}")
    return round(strength,3),time
    
    
    


# prints the password strength using a bar
def printStrengthGraphically(score):
    scoreFixed = int(round(score / 10))
    graphicP1 = "█" * scoreFixed
    graphicP2 = "░" * (max(10 - scoreFixed, 0))
    return graphicP1 + graphicP2


# calculates and returns password entropy
def calculatePasswordEntropy(pwd):
    charamt = 0
    charPrices = [26, 26, 9]
    charCheck = [False, False, False]
    for i in pwd:
        if i.islower():
            charCheck[0] = True
        elif i.isupper():
            charCheck[1] = True
        elif i.isdigit():
            charCheck[2] = True
    for a in range(3):
        if charCheck[a]:
            charamt += charPrices[a]
    entropy = math.log2(charamt) * len(pwd)
    return entropy, round(math.pow(2, entropy), 5)


# checks for errors in password
def pwdCheckCons(pwd, num, statusDict):

    pwdJoined = "".join(pwd)
    print(f"\nChecking Password for Errors: {pwdJoined}")
    for i in range(0, num - 1):
        if pwd[i] == pwd[i + 1]:
            print(
                f"\033[31mDuplicate Char Found: {pwd[i]}\n\033[0mPassword Status: {statusDict[False]}\033[33m\nGenerating New Password...\033[0m"
            )
            return False
        if abs(ord(pwd[i]) - ord(pwd[i + 1])) == 1:
            print(
                f"\033[31mConsecutive Characters in ASCII Found: {pwd[i]} and {pwd[i+1]}\n\033[0mPassword Status:{statusDict[False]}\033[33m\nGenerating New Password...\033[0m"
            )
            return False

    if pwdCheckKeyboard(pwd, num, statusDict) == False:
        return False
    if checkCommonWords1(pwd, statusDict) == False:
        for i in range(100):
            print(f"PWD = {pwd}")
    print(f"Password Status: {statusDict[True]}")
    return True


# checks if consecutive characters in the password are next to eachother on the keyboard
def pwdCheckKeyboard(pwd, num, statusDict):
    pwdString = "".join(pwd)
    keyboardLayoutRow = {"r1": "qwertyuiop", "r2": "asdfghjkl", "r3": "zxcvbnm"}
    keyboardLayoutColLeft = {
        "1": "1qaz",
        "2": "2wsx",
        "3": "3edc",
        "4": "4rfv",
        "5": "5tgb",
        "6": "6yhn",
        "7": "7ujm",
        "8": "8ik",
        "9": "9ol",
        "0": "0p",
    }
    keyboardLayoutColRight = {
        "1": "pl",
        "2": "0okm",
        "3": "9ijn",
        "4": "8uhb",
        "5": "7ygv",
        "6": "6tfc",
        "7": "5rdx",
        "8": "4esz",
        "9": "3wa",
        "0": "2q",
    }

    for i in range(0, num - 1):
        charFst = pwdString[i]
        charNxt = pwdString[i + 1]
        for row in keyboardLayoutRow.values():
            if charFst in row and charNxt in row:
                if abs(row.index(charFst) - row.index(charNxt)) == 1:
                    print(
                        f"\033[31mClose Characters on Keyboard Found (row wise): {charFst} and {charNxt}\n\033[0mPassword Status: {statusDict[False]}\033[33m\nGenerating New Password...\033[0m"
                    )
                    return False
        for row in keyboardLayoutColLeft.values():
            if charFst in row and charNxt in row:
                if abs(row.index(charFst) - row.index(charNxt)) == 1:
                    print(
                        f"\033[31mClose Characters on Keyboard Found (right column wise): {charFst} and {charNxt}\n\033[0mPassword Status: {statusDict[False]}\033[33m\nGenerating New Password...\033[0m"
                    )
                    return False
        for row in keyboardLayoutColRight.values():
            if charFst in row and charNxt in row:
                if abs(row.index(charFst) - row.index(charNxt)) == 1:
                    print(
                        f"\033[31mClose Characters on Keyboard Found (left column wise): {charFst} and {charNxt}\n\033[0mPassword Status: {statusDict[False]}\033[33m\nGenerating New Password...\033[0m"
                    )
                    return False


def checkCommonWords1(pwd, statusDict):
    commonWords = open("passwordGeneration/data/commonWords.txt", "r").read()
    wordsSplitList = commonWords.splitlines()
    for i in wordsSplitList:
        if i in pwd:
            print(
                f"\033[31mCommon Word Found: ({i}) Password Status: {statusDict[False]}\033[33m\nGenerating New Password...\033[0m"
            )
            return False
    else:
        return True


def checkCommonWords2(pwd):
    commonWords = open("passwordGeneration/data/commonWords.txt", "r").read()
    wordsSplitList = commonWords.splitlines()
    for i in wordsSplitList:
        if i in pwd:
            # print(f"\033[31mCommon Word Found: ({i})")
            return False
    return True


# sorts the password manager by keys and returns a sorted manager
def sortManager(passwordManager):
    tempList = []
    for key, value in passwordManager.items():
        tempList.append((key, value))
    logInfo("Password manager sorted", 0, 20)
    return dict(sorted(tempList))


# writes text slowly
def writeSlow(text):
    for letter in text:
        sys.stdout.write(letter)
        sys.stdout.flush()
        time.sleep(0.01)


# prints passwords in nice table format
def printPasswords(passwordManager):
    # decryptPasswords(passwordManager)
    print(
        "\033[34m  {:<20}   {:<35}   {:<20}\033[0m".format(
            "Program", "Username", "Password"
        )
    )

    # sortedPwd = {i: passwordManager[i] for i in myPrograms}
    sortedManager = sortManager(passwordManager)
    for program, password in sortedManager.items():
        print("  {:<20} | {:<35} | {:<20}".format(program, password[0], password[1]))


# encrypts single password
def encryptPassword(pwd, x):
    encrypted_pwd = []
    for i, char in enumerate(pwd):
        shift = (i % (len(pwd) - i)) + x  # Varying shift for each character
        new_ord = ord(char) + shift
        if new_ord > 126:  # Wrap around if beyond printable ASCII range
            new_ord -= 94
        encrypted_pwd.append(chr(new_ord))
    return "".join(encrypted_pwd)


# decrypts single password
def decryptPassword(pwd, x):
    decrypted_pwd = []
    for i, char in enumerate(pwd):
        shift = (i % (len(pwd) - i)) + x  # Varying shift for each character
        new_ord = ord(char) - shift
        if new_ord < 32:  # Wrap around if below printable ASCII range
            new_ord += 94
        decrypted_pwd.append(chr(new_ord))
    return "".join(decrypted_pwd)


# decrypts the entire password manager (done in backend at beginning of code loop)
def massDecryption(passwordManager):
    decryptedPWDManager = {}
    for program, data in passwordManager.items():
        uname, pwd = data
        decryptedPWDManager[program] = [
            decryptPassword(uname, 5),
            decryptPassword(pwd, 1),
        ]
        # print(f"PWD {program} done")
    return decryptedPWDManager


# saves the passwords in a data/data.json file
def savePasswords(passwordManager):
    # encrypts data
    encryptedPasswordManager = {}
    for program, data in passwordManager.items():
        uname, pwd = data
        encryptedPasswordManager[program] = [
            encryptPassword(uname, 5),
            encryptPassword(pwd, 1),
        ]

    with open("passwordGeneration/data/data.json", "w") as f:
        json.dump(encryptedPasswordManager, f)


# prints all programs
def printPrograms(passwordManager):
    print("Here are the all the programs on the password manager:\n")
    for i in passwordManager:
        print(f"\033[34m{i}\033[0m")


# backend program for logging info/error messages
def logInfo(action, option, level):
    levelDic = {10: "debug", 20: "info", 30: "warning", 40: "error", 50: "critical"}
    funcName = levelDic.get(level)
    if funcName:
        logging_function = getattr(logging, funcName)
        logging_function(f'Action: "{action}" Option: {option}')
    else:
        print("ERROR 202: INVALID LOG LEVEL")


# main code loop
if __name__ == "__main__":

    # Get the result
    if not logging.getLogger().hasHandlers():
        logInfo("New Log File Created", 0, 50)

    writeSlow("\nHi! Welcome to the password manager! ")
    if os.path.exists("passwordGeneration/data/data.json"):
        with open("passwordGeneration/data/data.json", "r") as p:
            encryptedPWDManager = json.load(p)
            passwordManager = massDecryption(encryptedPWDManager)
            logInfo("Password manager accessed and decrypted", 0, 20)
            # passwordManager ={program:[username, decryptPasswords(encryptedPassword)] for program, [username, encryptedPassword] in encryptedPasswordManager.items()}

    else:
        passwordManager = {}
        logInfo("New password manager created", 0, 20)

    while True:

        options = input(
            "\nSelect an action! \n 1: Computer creates secure password \n 2: Store new username and password \n 3: Delete a password \n 4: Change your username or password \n 5: Display all passwords \n 6: Score Password \n 7: Copy Password to Clipboard \n 8: Delete Password File (PERMANNENT) \n 9: Remove Log File (developer) \n 10: End program and save work\n Choice: "
        )
        newprintLn()

        # lets computer create new password
        if options == "1":
            c = input(
                "Would you like your password to be a specific length? (Y or N)  "
            ).upper()
            if c == "Y":
                x = input("Enter length of password. The max length is 150: ")
                if x.isdigit() and int(x) < 150:
                    pwd = pwdCreation(int(x))
                    pwdAppend1(pwd)
                    logInfo("Password created and added to manager", options, 20)
                else:
                    print("\033[33mLength must be integer below 150\033[0m")
            elif c == "N":
                pwd = pwdCreation(primeNumGen())
                pwdAppend1(pwd)
                logInfo("Password created and added to manager", options, 20)
            else:
                print(f"\033[31mInvalid choice\033[0m")
                logInfo(f"Invalid Response (Choices were Y or N)", options, 40)

        # adds new password to manager
        elif options == "2":
            program = pwdAppend2()
            logInfo(f"Stored username and password to {program} ", options, 20)

        # runs delete password code
        elif options == "3":
            print("Password Manager: \n")
            printPasswords(passwordManager)
            deletedSet = input(
                "\nWhich password would you like to delete. Enter program name: "
            ).upper()
            if deletedSet in passwordManager:
                del passwordManager[deletedSet]
                print(f"\033[31mPassword Deleted \033[0m")
                logInfo(f"Deleted Password from {deletedSet} ", options, 20)

            else:
                print(f"\033[31m\nPassword not found under written program\033[0m")
                logInfo(f'Program "{deletedSet}" not found ', options, 40)

        # allows for password reasignment
        elif options == "4":
            print("\nPassword Manager: ")
            printPasswords(passwordManager)
            reasignedSet = input(
                "Which program would you like to change? Enter program name: "
            ).upper()
            if reasignedSet in passwordManager:
                choice = input(
                    "Would you like to change the username or password? "
                ).upper()
                if choice == "PASSWORD":
                    newPwd = input("Type in your new password: ")
                    username, a = passwordManager[reasignedSet]

                    if newPwd == "":
                        print(f"\033[31mNo Password Given\033[0m")
                        logInfo(
                            f'Password not given for program "{reasignedSet}"',
                            options,
                            40,
                        )

                    else:
                        passwordManager[reasignedSet] = (username, newPwd)
                        logInfo(
                            f'Password changed for program "{reasignedSet}"',
                            options,
                            20,
                        )
                        print(f"\033[33m{reasignedSet} password updated \033[0m")

                elif choice == "USERNAME":
                    newUname = input("\nType in your new username: ")
                    a, pwd = passwordManager[reasignedSet]
                    if newUname == "":
                        logInfo(
                            f'Username not given for program "{reasignedSet}"',
                            options,
                            40,
                        )
                        print(f"\033[31mNo Username Given.\033[0m")

                    else:
                        passwordManager[reasignedSet] = (newUname, pwd)
                        logInfo(
                            f'Username changed for program "{reasignedSet}"',
                            options,
                            20,
                        )
                        print(f"\033[33m{reasignedSet} username updated \033[0m")
                else:
                    print(f"\033[31mInvalid choice\033[0m")
                    logInfo(
                        f"Invalid Response (Choices were USERNAME and PASSWORD)",
                        options,
                        40,
                    )

            else:
                logInfo(f'Program "{reasignedSet}" not found in manager', options, 40)
                print(f"\033[31mProgram not found in password manager\033[0m")

        elif options == "5":
            logInfo(f"Passwords printed to terminal", options, 20)
            print("\nHere are the current passwords in the password manager: ")
            printPasswords(passwordManager)

        # scores password
        elif options == "6":
            
            choice = input(
                "Would you like to enter your own password, use one in the passwordManager, or score one made by the computer? (OWN,PASSWORDMANAGER,COMPUTER): "
            ).upper()

            if choice == "COMPUTER":
                pwd = pwdCreation(primeNumGen())
                strengthScore, time = checkStrength(pwd, 1)
                print(f"Your password has a preliminary score of: \033[1m{strengthScore}%\033[0m")
                print(
                    f"Graphical Representation:  [{printStrengthGraphically(strengthScore)}]"
                )

                logInfo(
                    f"Score calculated and printed for password generated by {choice}",
                    options,
                    20,
                )

            elif choice == "PASSWORDMANAGER":
                print("\nHere are the current passwords in the password manager: ")
                printPasswords(passwordManager)
                logInfo(f"Passwords printed to terminal", options, 20)
                programChosen = input(
                    "\nWhich password would you like to access? Enter program name: "
                ).upper()
                if programChosen in passwordManager:
                    a, b = passwordManager[programChosen]
                    strengthScore, time = checkStrength(b, 1)
                    print(
                        f"Your password has a score of: \033[1m{strengthScore}%\033[0m"
                    )
                    print(
                        f"Graphical Representation:  [{printStrengthGraphically(strengthScore)}]"
                    )
                    print(f"Number of Guesses needed to Find Password: {time}\n")
                    logInfo(
                        f'Score calculated and printed for password in program "{programChosen}"',
                        options,
                        20,
                    )

                else:
                    logInfo(
                        f'Program "{programChosen}" not found in manager', options, 40
                    )
                    print("\033[31mProgram not found.\033[0m")

            elif choice == "OWN":
                pwd = input("Enter password to be scored: ")

                # statistics_result = subprocess.run(["java", "ScoringPWD", "findStatistics"], input=pwd, capture_output=True, text=True)
                # if statistics_result.returncode != 0:
                #     print("Error calling findStatistics method:", statistics_result.stderr)
                #     exit()
                # print("Statistics result from Java program:", statistics_result.stdout)

                strengthScore, time = checkStrength(pwd, 1)
                print(f"Your password has a score of: \033[1m{strengthScore}%\033[0m")
                print(
                    f"Graphical Representation:  [{printStrengthGraphically(strengthScore)}]"
                )
                print(f"Number of Guesses needed to Find Password: {time}\n")

                logInfo(
                    f"Score calculated and printed for password inputted by user",
                    options,
                    20,
                )

            else:
                print(f"\033[31mInvalid choice\033[0m")
                logInfo(
                    f"Invalid Response (Choices were OWN,PASSWORDMANAGER, and COMPUTER)",
                    options,
                    40,
                )

        # Copies password to clipboard
        elif options == "7":
            printPrograms(passwordManager)
            copyProgram = input(
                "\nWhich password would you like to access. Enter program name: "
            ).upper()
            if copyProgram in passwordManager:
                a, pwdCpy = passwordManager[copyProgram]
                copyToClipboard(pwdCpy)
                print(f"\033[33mPassword ({pwdCpy}) Copied to Clipboard\033[0m")
                logInfo(
                    f'Password from program "{copyProgram}" copied to clipboard',
                    options,
                    20,
                )

            else:
                logInfo(f'Program "{copyProgram}" not found', options, 40)
                print(f"\033[31mProgram not found in password manager\033[0m")

        # deletes password file
        elif options == "8":
            check = input(
                "Are you want to delete the password file. This is a permament action! (Y or N)\n"
            ).upper()
            if check == "Y":
                print(f"\033[31mPassword Data Removed\033[0m")
                logInfo(f"Password Manager cleared", options, 30)
                passwordManager = {}
                os.remove("passwordGeneration/data/data.json")
                logInfo(f"Password File Deleted", options, 30)

        # deletes log file
        elif options == "9":
            try:
                with open("passwordGeneration/data/password_manager.log", "w"):
                    pass
            except PermissionError:
                logInfo("Delete Log File Failed", options, 50)

        # ends program
        elif options == "10":
            print(
                f"\033[032mCode Completion - Encrypted passwords added to file\033[0m"
            )
            break

        else:
            logInfo(f'Command "{options}" not found', 0, 40)
            print(f"\033[031mInvalid Command. Please try again\033[0m")
    savePasswords(passwordManager)
    logInfo(f"All data saved", 0, 20)
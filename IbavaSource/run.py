# Token types
#
# EOF (end-of-file) token is used to indicate that
# there is no more input left for lexical analysis
EOF, NULL, INTEGER = 'EOF', 'NULL', 'INTEGER'
VARIABLE, CODE = 'VARIABLE', 'CODE'
PLUS, MINUS, TIMES, DIVIDE, EXP, MOD = 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EXP', 'MOD'

endProgram = False
line_number = -1
line_output = ""

#can use same names
from if_methods import *
from loop_methods import *
from variable_methods import *
from operator_methods import *
from comparison_methods import *

class Token(object):
    def __init__(self, type, value):
        # token type: INTEGER, PLUS, or EOF
        self.type = type
        # token value: 0, 1, 2. 3, 4, 5, 6, 7, 8, 9, '+', or None
        self.value = value

    def __str__(self):
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()

#Class is called from variable_methods.py
class Interpreter(object):
    def __init__(self, text):
        # client string input, e.g. "3+5"
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        # current token instance
        self.current_token = None

    def error(self):
        raise Exception('Error parsing input')

    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)

        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.
        """
        text = self.text

        # is self.pos index past the end of the self.tex...
        # then return EOF token because there is no more
        # input left to convert into tokens
        if self.pos > len(text) - 1:
            return Token(EOF, None)

        # get a character at the position self.pos and decide
        # what token to create based on the single character
        current_char = text[self.pos]

        # if the character is a digit then convert it to
        # integer, create an INTEGER token, increment self.pos
        # index to point to the next character after the digit,
        # and return the INTEGER token
        if current_char.isdigit():
            token = Token(INTEGER, int(current_char))
            self.pos += 1
            return token

        if current_char.isalpha() and current_char.isupper():
            token = Token(VARIABLE, current_char)
            self.pos += 1
            return token

        if isOperator(current_char):
            operatorType = mapOperatorToToken(current_char)
            token = Token(operatorType, current_char)
            self.pos += 1
            return token

        if current_char == "m":
            _startPos = self.pos
            _endPos = self.pos + 3
            _operator = text[_startPos:_endPos]
            if _operator == "mod":
                operatorType = mapOperatorToToken(_operator)
                token = Token(operatorType, _operator)
                self.pos += 3
                return token

        printError("Could not recognize character: " + current_char)
        #self.error()

    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            printError("ERROR: Eating failed. Invalid expression")
            #self.error()

    def readValue(self):

        _varName = ""
        #get variable name
        while self.current_token.type == "VARIABLE":
            _varName += self.current_token.value
            self.eat(VARIABLE)

        #if variable exists, read its value and return it as a token
        if _varName != "":
            var = getVariable(_varName)
            _token = Token(var['type'], var['value'])
            return _token

        #If the there is no variable, it must be a number
        _token = self.current_token
        self.eat(INTEGER)

        #Allows multiple digit numbers
        while self.current_token.type == "INTEGER":
            _token.value *= 10
            _token.value += self.current_token.value
            self.eat(INTEGER)

        return _token

    def expr(self):
        #format -> INTEGER OPERATOR INTEGER

        # set current token to the first token taken from the input
        self.current_token = self.get_next_token()

        # get left side value, even if it is a variable
        left = self.readValue()

        # get operator
        op = self.current_token
        if isTypeOperator(op.type):
            self.eat(self.current_token.type)
        #if there is no operator after first number, leave
        else:
            return left.value

        # get right side value, even if it is a variable
        right = self.readValue()

        # perform operation
        result = performOperation(op.type, left.value, right.value)

        return result


def main():

    print "nothing to do here..."
    return

def preFormatCode(lines):
    lines = [i.replace("\t", "") for i in lines]

    #remove blanks and //
    for element in lines[:]:
        if element == "":
            lines.remove(element)
        elif element.startswith("//"):
            lines.remove(element)

    import re
    #remove white space outside quotes only
    for i in xrange(len(lines)):
        parts = re.split(r"""("[^"]*"|'[^']*')""", lines[i])
        parts[::2] = map(lambda s: "".join(s.split()), parts[::2]) # outside quotes
        lines[i] = "".join(parts)

    return lines


def runCode(givenCode):
    #make each line of code an element in array
    lines = givenCode.split('\n')
    lines = preFormatCode(lines)
    outputString = ""

    global line_number
    #because we increment early, line_number is -1 rather than 0
    line_number = -1

    #clear out all sessions
    variables[:] = []
    ifSessions[:] = []
    loopSessions[:] = [] 
    print variables

    #loop through each line of code
    while line_number < len(lines) - 1:

        line_number += 1

        #get text
        line = lines[line_number]

        global line_output

        #LOOP
        loop_session = loopBlock(line)
        if loop_session == "continue":
            continue

        #IF
        current_session = ifStatementBlock(line)
        if current_session == "continue":
            outputString += getLineOutput(line_output, line_number)
            line_output = None
            #print ifSessions
            continue
            
        #read output
        readCode(line)
        
        outputString += getLineOutput(line_output, line_number)
        line_output = None

        if endProgram:
            break

    return outputString

def getLineOutput(line_output, line_number):
    _outputString = ""

    if line_output is not None:
        #Don't add space to first line
        if line_number > 0:
            _outputString += "\n"
        #Accumulate output in one strip
        _outputString += str(line_output)

    return _outputString

#MAIN METHODS
def loopBlock(line):
    global line_number

    #If we are within a loop, check for break and continue
    if loopSessionExists() and not reachedEndLoop(line):
        #if we break, then we break out of for loop

        #ignore all other code in loop and exit when we reach end
        if getBreakSession():
            return "continue"

        #ignore all other code within loop until we reach end
        if getContinueSession():
            return "continue"

    #if the current line is starting a loop
    if isLoop(line):
        if loopType(line) == "for":
            loopVarName, _from, _to = getInfoFromForLoop(line)

            #translate for loop condition into while loop condition
            loopEndcondition = createForLoopCondition(loopVarName, _to)

            createOrSetVariable(loopVarName, _from)
            #correctly adds X=X+1 to session
            addLoopSession(line_number, "for", loopVarName, loopEndcondition, False)
            return "continue"

        elif loopType(line) == "while":
            loopEndcondition = getInfoFromWhileLoop(line)
            #var name field is empty for while
            addLoopSession(line_number, "while", "", loopEndcondition, False)
            return "continue"
        else:
            printError("This loop is invalid")
            return

    #if the current line is ending the loop
    elif reachedEndLoop(line):

        if getBreakSession():
            removeLoopSession()
            return "continue"

        if getContinueSession():
            #check condition and then go back
            setContinueSessionTo(False)

        _loopType = getLoopType()

        loopEndcondition = getLoopEndCondition()

        if _loopType == "for":
            if isLoopOver(loopEndcondition):
                removeLoopSession()
                return "continue"
            else:  
                #line_number is global
                line_number = getLoopLineBegin()
                loopVarName = getLoopVarName()
                _increment = loopVarName + "+1"
                createOrSetVariable(loopVarName, _increment)
                return "continue"

        if _loopType == "while":
            lastIteration = getLastIteration()
            if isLoopOver(loopEndcondition):
                #removeLoopSession()
                if lastIteration:
                    removeLoopSession()
                else:
                    nowLastIteration()
                    line_number = getLoopLineBegin()
            else: 
                #line_number is global
                line_number = getLoopLineBegin()
            return "continue"

    #TAG: Why is this here, and not in the beginning??
    elif breakCalled(line):
        setBreakSessionTrue()

    elif continueCalled(line):
        setContinueSessionTo(True)

        printError("The loop was stored incorrectly. Something went seriously wrong.")

def ifStatementBlock(_text):

    if ifIsCalled(_text):
        condition = getConditionFromIfStatement(_text)
        conditionIsTrue = comparison(condition)
        if conditionIsTrue is "true":
            #the 0 here is the stage. 0 means if,
            #1 means else if, 2 means else
            addSession(0)
            setSessionTrue(0)
            return "continue"
        elif conditionIsTrue is "false":
            addSession(0)
            setSessionFalse(0)
            return "continue"
        #condition is not true
        return conditionIsTrue
        #print "Second if statement called"
       # return "continue"

    #if session exists
    if ifSessionCount() >= 1:
        #if session is true
        if endIfIsCalled(_text):
            endSession()
            return "continue"

        if readSession() is True:
            if elseIsCalled(_text):
                setSessionFalse(2)
                return "continue"
            if elseIfIsCalled(_text):
                setSessionFalse(1)
                return "continue"

            #If we are inside if statement, read code
            readCode(_text)
            return "continue"

        #if session is false and has never been true before
        if readHasBeenTrueBefore() is False:
            if elseIsCalled(_text):
                setSessionTrue(2)
                return "continue"
            if elseIfIsCalled(_text):
                condition = getConditionFromElseIfStatement(_text)
                conditionIsTrue = comparison(condition)
                if conditionIsTrue is "true":
                    setSessionTrue(1)
                    return "continue"
                #print "Session is still false"
                return "continue"
            #print "Ignoring code..."
            return "continue"
        #if session is false and has been true before
        else:
            if elseIsCalled(_text):
                setSessionFalse(2)
            elif elseIsCalled(_text):
                setSessionFalse(1)

            #print "Ignoring code because session was once true..."
            return "continue"

    return "no session detected"

def printingOutput(_text):
    return "output" in _text

def printOutput(_value):
    var = getVariable(_value)
    _lenth = len(_value)-1

    if var is not None:
        return var['value']

    #otherwise if it is a plain string
    if _value[0] == '"' and _value[_lenth] == '"':
        return _value[1:_lenth]

    #if it has one plus sign
    if "+" in _value:
        _temp = _value.split("+", 1)
        #recursively print both sides
        return str(printOutput(_temp[0])) + str(printOutput(_temp[1]))

    #otherwise if it is a boolean or integer, just straight out print it
    return _value

def readCode(_text):
    #if line prints an output, print it...
    if printingOutput(_text):
        global line_output
        line_output = printOutput(_text[6:])
        #return printOutput(_text[6:])

    #count amount of equal signs
    if howManySet(_text) == 1:
        #method is in variable_methods.py
        parseAndCreateOrSetVariable(_text)

def printError(_errorMessage):
    global endProgram
    print _errorMessage
    endProgram = True
from run import *

#list of dictionaries.. {'type': varType, 'name': varName, 'value': varValue}
variables = []

#VARIABLE METHODS
def parseAndCreateOrSetVariable(_text):
    _expressions = _text.split("=", 1)
    _varName = _expressions[0]
    _rightSide = _expressions[1]
    createOrSetVariable(_varName, _rightSide)

def createOrSetVariable(varName, rightSide):
    #Var name must be an upper case word
    if varName.isupper() and varName.isalpha():

        varType, varValue = interpretVarType(rightSide)
        #Check if variable exists
        var = getVariable(varName)
        if var is not None:
            var['value'], var['type'] = varValue, varType
            return

        #if it does not, add it to list
        variables.append({'type': varType, 'name': varName, 'value': varValue})
        return

    printError("ERROR: Invalid variable name. Names must be capital words")
    return

def interpretVarType(_value):
    
    #if this is inequality...
    from run import howManyComparison
    from run import howManyOperator
    from run import Interpreter

    if howManyComparison(_value) == 1:
        return "BOOLEAN", comparison(_value)

    #if this is operation...
    #THIS IS WHAT IS CAUSING PROBLEM

    if howManyOperator(_value) == 1:
        _interpreter = Interpreter(_value)
        return "INTEGER", _interpreter.expr()

    #if this is plain integer
    if _value.isdigit():
        return "INTEGER", int(_value)

    #if this is plain boolean
    if _value == "true" or _value == "false":
        return "BOOLEAN", _value

    #if this is plain string
    if _value[0] == '"' and _value[len(_value)-1] == '"':
        return "STRING", _value

    #Only remaining possibility is that it is a variable
    #Go through list of variables
    var = getVariable(_value)
    if var is not None:
        return var['type'], var['value']

    printError("ERROR: Failed to set variable")
    return None


def getVariable(_myVariableName):

    for var in variables:
        if var['name'] == _myVariableName:
            return var

    #print "Variable does not exist "
    #Returning none is variable
    return None

#END VARIABLE METHODS
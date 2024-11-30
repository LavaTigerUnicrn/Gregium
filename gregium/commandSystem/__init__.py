"""
The original 'CLI' class in gregium

Revamp is pending
"""
import gregium.terminalLogging,json

LOGGER = gregium.terminalLogging.PRIMARY

def _cmdParseSeg(segment:str,requestedType:str,min="N/A",max="N/A"):
    """Function for parsing strings, integers, floats, and json"""

    # Check for different types of the material to parse
    match requestedType:

        case "str":
            # Remove all double quotes in strings
            return segment.replace("\"","")

        case "int":
            try:
                # Make sure the integer is within the range of (min, max)
                segNum = int(segment)
                if min != "N/A":
                    if segNum < min:
                        return (6,"Value outside of accepted range")
                if max != "N/A":
                    if segNum > max:
                        return (6,"Value outside of accepted range")
                return segNum
            
            # Return with exit code 5 if argument was invalid
            except:
                return (5,"Could not make into an Integer")
            
        
        case "float":
            try:
                # Make sure the float is within the range of (min, max)
                segNum = float(segment)
                if min != "N/A":
                    if not segNum >= min:
                        return (6,"Value outside of accepted range")
                if max != "N/A":
                    if not segNum <= max:
                        return (6,"Value outside of accepted range")
                return segNum
            
            # Return with exit code 7 if argument was invalid
            except:
                return (7,"Could not make into an Float")
            
        case "json":
            try:
                # Return a parsed python object of the given segment
                return json.loads(segment)
            
            # Return with exit code 8 if something fails (usually an invalid json)
            except Exception as e:
                return (8,"Json error: "+e)
            
class CommmandSystem:
    def __init__(self,tree:dict={}):

        LOGGER.info("CommandSystem Generated")
        """
        Make easy command interpreters that can be used outside, or inside terminal
        """
        self._cmds = tree

    def addCmd(self,commandDict:dict):
        """
        add a new command! Syntax is as follows
        {"name":{"root":{"type":"*","var":"test","next":"foo"},"foo":{"type":"*","var":"test2","next":"etc"}}}

        *Types include, str, json, int, float, literal, func
        int & float can have min and max
        literal must have a list of outputs
        func must have a "run" variable instead of next and var and the "run" variable must have the function in it
        you can input multiple commands by having multiple in the furthest outside dict
        repeat commands will not get overwritten but will instead throw an error
        """
        for cmd in commandDict:
            self._cmds[cmd] = commandDict[cmd]

    def helpcmd(self,*args):
        """Generate a help message for using commands"""

        cmdList = ""

        # Return a specific help message for a given command
        if len(args) > 0:
            cmdD = self._cmds[args[0]]
            for cmdSeg in cmdD:
                cmdList += f"{cmdSeg}:{cmdD[cmdSeg]}\n"
            return f'{args[0]}:\n{cmdList}'
        
        # Return a list of every existing command
        for cmd in self._cmds:
            cmdList += f'{cmd}\n'
        return f'Commands:\n{cmdList}Type help (command) for specific syntax'
    
    def run(self,cmd:str) -> tuple[int,str]:
        """
        Read a full command from a string and output code (error, return) or (0, return) on success
        """
        LOGGER.info(f"Command run: {cmd}")

        # Initial split
        newCmd = cmd.split(" ")

        # Recombine strings and json
        cmdRun = []
        isOpenStr = False
        openJsonIndex = 0
        sectionComb = ""

        # Check each section
        for section in newCmd:

            # Add each section to the combined section
            sectionComb += section
            wasOpenStr = False

            # Check each letter of the section
            for ltr in section:

                # Check to see if all json
                if wasOpenStr and openJsonIndex == 0:
                    return (1,"String must end at parameter end") 
                
                # Check for '"' in the string
                if ltr == "\"":
                    isOpenStr = not isOpenStr

                    # If a string is closed, make sure it is noted
                    if not isOpenStr:
                        wasOpenStr = True

                # If a { is found outside a string, increase the json index by 1 (json depth)
                if ltr == "{" and not isOpenStr:
                    openJsonIndex += 1

                # If a } is found outside a string, increase the json index by 1 (json depth)
                if ltr == "}" and not isOpenStr:
                    openJsonIndex -= 1
                
                # Prevent negative open json
                if openJsonIndex < 0:
                    return (2,"Closed json before opening")
                
            # If there is nothing left in the parameter, add it to the sections of command to run
            if not isOpenStr and openJsonIndex == 0:
                cmdRun.append(sectionComb)
                sectionComb = ""
            else:

                # Otherwise continue to loop through
                sectionComb += " "

        # Raise error if json is still open
        if openJsonIndex > 0:
            return (3,"Not all json instances have been closed")
            
        # Run the help command (if applicable)
        if cmdRun[0] == "help":

            # Run help command with specific command (if applicable)
            if len(cmdRun) > 1:
                if cmdRun[1] in self._cmds:
                    return self.helpcmd(cmdRun[1])
                else:
                    return self.helpcmd()
            else:
                return self.helpcmd()

        # Check if command exists
        if cmdRun[0] in self._cmds:

            # Prepare variables for reading
            isReadingStart = False
            nextIndex = "root"
            cmd = self._cmds[cmdRun[0]]
            supArgs = {}

            # Check each parameter in the command
            for item in cmdRun:

                # Only start once the command name is passed
                if isReadingStart:

                    # Check which type of parameter it is (literal,func,or other)
                    match cmd[nextIndex]["type"]:

                        # If type is literal, change the next section based on which name is supplied
                        case "literal":
                            nextFound = cmd[nextIndex]["next"]

                            # If the entered output is invalid, raise an error
                            if item in nextFound:
                                nextIndex = item
                            else:
                                return (9,"Could not find next literal")
                            
                        # Is func is run without all arguments handle, raise "error"
                        case "func":
                            return (10,"Too many arguments")
                        
                        # Otherwise handle it with "cmdParseSeg" function
                        case _:

                            # Check for function min or max
                            relMin = "N/A"
                            relMax = "N/A"
                            if "min" in cmd[nextIndex]:
                                relMin = cmd[nextIndex]["min"]
                            if "max" in cmd[nextIndex]:
                                relMax = cmd[nextIndex]["max"]

                            # Get the parsed output
                            parsedSeg = _cmdParseSeg(item,cmd[nextIndex]["type"],relMin,relMax)

                            # Add the output to the arguments for the final function
                            if type(parsedSeg) != tuple:
                                supArgs[cmd[nextIndex]["var"]] = parsedSeg

                                # Continue to the next section of the command
                                nextIndex = cmd[nextIndex]["next"]
                            else:
                                return parsedSeg
                isReadingStart = True

            # If function is not yet due to run, not enough arguments have been supplied
            if nextIndex != "func":
                return (11,"Not enough arguments")
            
            # Run the command's function and return
            return cmd[nextIndex]["run"](kwargs=supArgs)
                
        else:
            return (4, "Command not found")
##FRAMES##
import sys
GF = 0
LF = 1
TF = 2

##TYPES##
ANY = -1
BOOL = 1
INT = 2
NIL = 3
STRING = 4
LABEL = 5
TYPE = 6
VAR = 7

##INSTRUCTION POSITIONS##
POS_VARIABLE = 0
POS_ARG1 = 1
POS_ARG2 = 2

##ARITHMETICS OPERATIONS##
ADD = 0
SUB = 1
IDIV = 2
MUL = 3

##COMAPRSION OPERATIONS##
GT = 0
LT = 1
EQ = 2

##LOGICAL OPERATIONS####
AND = 0
OR = 1
NOT = 2

## OUTPUT ##
WRITE = sys.stdout
DPRINT = sys.stderr

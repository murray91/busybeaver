import numpy as np 
from mikeio import Dfsu
from mikeio.eum import ItemInfo, EUMType, EUMUnit
from mikeio import Dataset

def TEMPORARY(*args):
    return "TEST"

# Returns the values of constants passed to it
def FOR_TESTING_ONLY(*args):
    return [*args]

# extractDirectionFromDfsu
# Saves direction from specified timestep to a new dfsu
# Useful for dealing with large dfsu files
#
# Example usage:
#   extractDirectionFromDfsu("mydfsu.dfsu", "mydfsu_direction", 30)  
# 
# Assumes
#   -input dfsu has Current direction
#   -timestep specified exists
#   -Current direction unit is radians
#  
def extractDirectionFromDfsu(input_dfsu, output_dfsu, timestep):

    # Make sure timestep is an integer and not string
    timestep = int(timestep)

    # Open dfsu and read specified timestep
    dfs = Dfsu(input_dfsu)
    ds = dfs.read(time_steps=timestep)

    # Create new dataset for the specified timestep
    items = [ItemInfo("Current direction", EUMType.Current_Direction, EUMUnit.radian)]
    newds = Dataset([ds["Current direction"]], ds.time, items)

    # Write direction to new dfsu
    dfs.write(output_dfsu, newds)
    
    return True

# process2DDepth
# Insert description of function
# Example usage: ...
def process2DDepth(*args):
    return None

# process2DVelocity
# Insert description of function
# Example usage: ...
def process2DVelocity(*args):
    return None

# process2DDirection
# Insert description of function
# Example usage: ...
def process2DDirection(*args):
    return None

# processRiverDepth
# Insert description of function
# Example usage: ...
def processRiverDepth(*args):
    return None

# processFullDepth
# Insert description of function
# Example usage: ...
def processFullDepth(*args):
    return None

# processClipDepth
# Insert description of function
# Example usage: ...
def processClipDepth(*args):
    return None

# processClipVelocity
# Insert description of function
# Example usage: ...
def processClipVelocity(*args):
    return None

# processClean
# Insert description of function
# Example usage: ...
def processClean(*args):
    return None
import maya.cmds
import os
import re

# Formats the given string into a name that maya hypershade supports
def FormatShaderName(name):
    # Replaces dash dot and whitespace by underscore. Might need to be extended
    name = re.sub("[-.\s]", "_", name)
    return name

# Returns whether or not texture is duplicate
def DoesTextureExist(shaderName):
    # List all shaders
    existingShaders = cmds.ls(materials=True)
    
    # Check if shader already exists
    isShaderDuplicate = shaderName in existingShaders
    return isShaderDuplicate
    
# Creates a new standard surface texture w/ name=shaderName and texturePath as texture source
# Returns the name of the shader
def CreateNewTexture(shaderName, texturePath):
    # Create standardsurface and file nodes
    shaderNode = cmds.shadingNode("standardSurface", asShader=True, name=shaderName)
    fileNode = cmds.shadingNode("file", asTexture=True, name=shaderName + ".File")
    
    # Add output surface shader node
    cmds.sets(shaderNode, renderable=True, name=shaderNode + "SG")
    # Set texture path
    cmds.setAttr(fileNode + ".fileTextureName", texturePath, type="string")
    
    # Connect nodes
    cmds.connectAttr(fileNode + ".outColor", shaderNode + ".baseColor", force=True)
    cmds.connectAttr(shaderNode + ".outColor", shaderNode + "SG.surfaceShader", force=True)
    
    return shaderNode
    
def ApplyTextureQuick(texturePath):
    shaderName = FormatShaderName("EasyTextures_" + os.path.basename(texturePath))
    selectedObjects = cmds.ls(sl=True)
    
    # If the texture doesn't exist already, create it
    if(not DoesTextureExist(shaderName)):
        CreateNewTexture(shaderName, texturePath)
    
    # Apply texture to objects
    cmds.sets(selectedObjects, e=True, forceElement=shaderName + "SG")

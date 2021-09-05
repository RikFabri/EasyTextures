import maya.cmds
import os

# Returns whether or not texture is duplicate, and the shaderName on which it queried
def FindDuplicateTexture(shaderName):
    # List all shaders
    existingShaders = cmds.ls(materials=True)
    
    # Format shaderName to the name it would have if it exists
    shaderName = shaderName.replace(".", "_")

    # Check if shader already exists
    isShaderDuplicate = shaderName in existingShaders
    return isShaderDuplicate, shaderName
    
# Creates a new standard surface texture w/ name=shaderName and texturePath as texture source
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
    textureName = os.path.basename(texturePath) + ".EasyTextures"
    selectedObjects = cmds.ls(sl=True)

    isDuplicate, shaderName = FindDuplicateTexture(textureName)
    
    # If the texture doesn't exist already, create it
    if(not isDuplicate):
        shaderName = CreateNewTexture(shaderName, texturePath)
    
    # Apply texture to objects
    cmds.sets(selectedObjects, e=True, forceElement=shaderName + "SG")

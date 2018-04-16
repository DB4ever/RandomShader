Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)] on win32
Type "copyright", "credits" or "license()" for more information.
>>> import maya.cmds as mc
import maya.mel as mel
import os
import random




def chooseRandomTex():
    texList = ['brownian', 'cloud', 'crater', 'granite', 'leather', 'marble', 'rock', 'snow', 'solidFractal', 'stucco', 'volumeNoise', 'wood']
    num = random.randint(0, len(texList)-1)
    print texList[num]
    return texList[num]
        
def create3DTex(shader, mat="cloud" ):
    tex = mc.shadingNode(mat, asTexture=True)
    p3DTex = mc.shadingNode("place3dTexture", asUtility=True)
    mc.connectAttr(p3DTex+".wim[0]",  tex+".pm")
    # Result: Connected place3dTexture2.worldInverseMatrix to wood1.placementMatrix. // 
    #mc.defaultNavigation(force=True, connectToExisting=True, source=tex, destination=shader+".color", window -e -vis false createRenderNodeWindow;
    mc.connectAttr(tex+".outColor", shader+".color", force=True)
    
def randShader(obj, mat="blinn"):
    
    BL = mc.shadingNode(mat, asShader = True)
    mc.sets (renderable = True, noSurfaceShader = True, empty = True, name = BL+"SG")
    mc.select(obj)
    mc.sets( e=True, forceElement= BL + 'SG' )
    mc.connectAttr (BL+".outColor", BL+"SG.surfaceShader", f=True)
    #mel.eval('assignCreatedShader "%s" "" %s "%s";' %(mat, BL, obj))
    return BL
    
def randColor(shader):
    mc.setAttr(shader+".color", random.uniform(0.0, 1.0),random.uniform(0.0, 1.0),random.uniform(0.0, 1.0),type="double3")
    

def runIt(asf):
    geometry = mc.ls(geometry=True)
    transforms = mc.listRelatives(geometry, p=True, path=True)
    mc.select(transforms, r=True)
    listObj = mc.ls(sl=True)
    #mc.select('*place3dTexture', deselect=True)
    if not listObj:
        mc.confirmDialog(m='Pleaaaase select something')
    else:
        for i in listObj:
            shader = randShader(i)
            #randColor(shader)
            tex = chooseRandomTex()
            create3DTex(shader,  mat=tex)
                
        delUnusedShaders()
    


        
    
def ui():
    if mc.window("randShaderWin", exists=True):
        mc.deleteUI("randShaderWin")
    mainWindow = mc.window("randShaderWin", title="Random Shader", widthHeight=(200, 55), sizeable=False)
    mc.frameLayout(labelVisible=False, marginWidth=5, marginHeight=5)
    mc.button("Press Button", command=runIt)
    mc.showWindow()
    
def delUnusedShaders():
    mel.eval('MLdeleteUnused;')

ui()




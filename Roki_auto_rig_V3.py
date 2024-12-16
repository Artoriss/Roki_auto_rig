import maya.cmds as cmds


# Stock ctl position prefix
posC = 'C_'
posL = 'L_'
posR = 'R_'

# Stock ctl suffix
grpO = '_Offset_GRP'
grp = '_GRP'
grpA = '_ANIM'
ctlN = '_CTL'
gimbal = 'Gimbal_CTL'
cog= '_CTL_Offset_GRP'

# Stock LOC suffix
loc= '_LOC'
locO = '_Origine_LOC'

#Stock JNT suffix
jnt = '_JNT'


# Liste Fonction :

# CREAT LOC AT
# Cree un locator a une position donner et lui donner un nom spécifique
# Prefix = posC, posL, posR celon pas position de Loc pzr rzpport au persoonage
# LOC_N = Nom souhaité pour le loc créé
# TX, TY.... = Valeur de translate et rotate du LOC
def creat_loc_at( Prefix, LOC_N, TX, TY, TZ, RX, RY, RZ):
    Creat_Loc = cmds.spaceLocator(name= Prefix+ LOC_N +locO)[0]
    cmds.move(TX, TY, TZ, Creat_Loc)
    cmds.rotate(RX, RY, RZ, Creat_Loc)


# SYMMETRICAL
# Dupliquer et inverser des element non parent ou enfant par rapport au plan yz
# OriginalSide = posC, posL.... Position d'origine de l'élément
# NewSide = posC, posL.... Nouvel position de l'élément apres changement de symetrie
# Find = Nom ou partie de nom (Ex : '*_LOC) des élément a listé pour duplication
def symmetrical(OriginalSide, NewSide, Find, Exclude):
    # Listé les élément
    Element_Liste = cmds.ls(Find)
    # Exclure certain element
    if Exclude is not None:
        Element_Liste = [elem for elem in Element_Liste if not any(excl in elem for excl in Exclude)]

    # Parcourir chaque Element et créer un duplicata symétrique
    for Element in Element_Liste:
        # Dupliquer l'element
        Element_Dup = cmds.duplicate(Element, name=Element.replace(OriginalSide, NewSide))[0]

        cmds.group(name='SymGroup', empty=True)
        cmds.parent(Element_Dup, 'SymGroup')
        cmds.setAttr('SymGroup'+ '.scale', -1,1,1)
        cmds.parent(Element_Dup, world=True)
        cmds.delete('SymGroup')
        cmds.makeIdentity(Element_Dup,apply=True, s=1, n=0)


# CREE UN CIRCLE
# N_LOC = nom du Locator éxistent
# Prefix = prefix avec le nom du CTL et ou du LOC (ex posC = C_ pour Position Central)
# N_CTL = nom du CTL a créé
def creat_circle(N_LOC, Prefix, N_CTL):
    loc_name = Prefix + N_LOC + locO
    Loc_Trans = cmds.xform(loc_name, query=True, worldSpace=True, translation=True)
    Loc_Rot = cmds.xform(loc_name, query=True, worldSpace=True, rotation=True)

    CTL_Base = cmds.circle(n=Prefix+ N_CTL +ctlN, r=10, s= 12, normal=(0, 0, 0))[0]
    cmds.xform(CTL_Base, translation=Loc_Trans, rotation=Loc_Rot)
    CTL_Gimbal = cmds.circle(n=Prefix+ N_CTL +gimbal, r=10 - 1, s= 12, normal=(0, 0, 0))[0]
    cmds.xform(CTL_Gimbal, translation=Loc_Trans, rotation=Loc_Rot)

    cmds.parent(CTL_Gimbal, CTL_Base)


# CREE UN CUBE
# N_LOC = nom du Locator éxistent
# Prefix = prefix avec le nom du CTL et ou du LOC (ex posC = C_ pour Position Central)
# N_CTL = nom du CTL a créé
def creat_cube(N_LOC, Prefix, N_CTL):
    loc_name = Prefix + N_LOC + locO
    LOC_Trans = cmds.xform(loc_name, query=True, worldSpace=True, translation=True)
    Loc_Rot = cmds.xform(loc_name, query=True, worldSpace=True, rotation=True)

    
    CTL_Base =cmds.curve(n=Prefix+ N_CTL +ctlN, degree=1, point=[ (-1, 0, -1), (1, 0, -1), (1, 2, -1), (-1, 2, -1), (-1, 0, -1), 
                        (-1, 0, 1), (1, 0, 1), (1, 2, 1), (-1, 2, 1), (-1, 0, 1), 
                        (1, 0, 1), (1, 0, -1), (1, 2, -1), (1, 2, 1), (-1, 2, 1), (-1, 2, -1)])
    
    CTL_Gimbal =cmds.curve(n=Prefix+ N_CTL +gimbal, degree=1, point=[ (-1, 0, -1), (1, 0, -1), (1, 2, -1), (-1, 2, -1), (-1, 0, -1), 
                        (-1, 0, 1), (1, 0, 1), (1, 2, 1), (-1, 2, 1), (-1, 0, 1), 
                        (1, 0, 1), (1, 0, -1), (1, 2, -1), (1, 2, 1), (-1, 2, 1), (-1, 2, -1)])
        
    cmds.xform(CTL_Base, translation=LOC_Trans, rotation=Loc_Rot)
    cmds.xform(CTL_Gimbal, translation=LOC_Trans, rotation=Loc_Rot)

    #Fixe curveShape name qui match pas
    #Shape du CTL
    CTL_shape_name = cmds.listRelatives(CTL_Base, shapes=True)[0] 
    cmds.rename(CTL_shape_name, Prefix + N_CTL + ctlN + 'Shape')

    #Shape de la Gimbal
    CTL_Gimbalshape_name = cmds.listRelatives(CTL_Gimbal, shapes=True)[0]
    cmds.rename(CTL_Gimbalshape_name, Prefix + N_CTL + gimbal + 'Shape')

    cmds.setAttr(CTL_Gimbal + '.scale', 0.9,0.9,0.9)
    cmds.makeIdentity(CTL_Gimbal, apply=True, s=1, n=0)
    
    cmds.parent(CTL_Gimbal, CTL_Base)


# CREE LES GROUP OFFSET
# Prefix = prefix avec le nom du CTL et ou du LOC (ex posC = C_ pour Position Central)
# N_CTL = nom du CTL a créé
def creat_group_offset(Prefix, N_CTL):

    CTL_Base = Prefix + N_CTL + ctlN

    groupO = Prefix + N_CTL + grpO
    groupGrp = Prefix + N_CTL + grp
    groupA = Prefix + N_CTL + grpA
    
    # Créer les groupes
    cmds.group(em=True, name=groupO)
    cmds.group(em=True, name=groupGrp)
    cmds.group(em=True, name=groupA)

    # Faire correspondre les transformations aux contrôles 
    cmds.matchTransform(groupO, CTL_Base) 
    cmds.matchTransform(groupGrp, CTL_Base) 
    cmds.matchTransform(groupA, CTL_Base)
    
    # Emboîter les groupes
    cmds.parent(groupGrp, groupO)
    cmds.parent(groupA, groupGrp)
    cmds.parent(CTL_Base, groupA)


# CREE ET CONNECTER UN ATTR POUR LA VISIBILITY
# Prefix = prefix avec le nom du CTL et ou du LOC (ex posC = C_ pour Position Central)
# N_CTL = nom du CTL a créé
# ATT_LN = nom attribute long name a créé pour visibility ON/OFF de la Gimball nom invisible
# ATT_NN = nom attribute nice name a créé pour visibility ON/OFF de la Gimball nom visible
def creat_visibility_attr(Prefix, N_CTL, ATT_LN, ATT_NN):

    CTL_Base = cmds.ls(Prefix + N_CTL + ctlN)[0]
    CTL_Gimbal = cmds.ls(Prefix + N_CTL + gimbal)[0]

    cmds.addAttr(CTL_Base, longName=ATT_LN, niceName=ATT_NN, attributeType='enum', enumName='Off:On', keyable=True)
    cmds.connectAttr(f"{CTL_Base}.{ATT_LN}", f"{CTL_Gimbal}.visibility")



# CREE CTL + GRP_OFFSET + ATTR_VISIBILITY
# N_LOC = nom du Locator éxistent
# Prefix = prefix avec le nom du CTL et ou du LOC (ex posC = C_ pour Position Central)
# N_CTL = nom du CTL a créé
# ATT_LN = nom attribute long name a créé pour visibility ON/OFF de la Gimball
# ATT_NN = nom attribute nice name a créé pour visibility ON/OFF de la Gimball
def creat_complet_circle_CTL(N_LOC, N_CTL, Prefix, ATT_LN, ATT_NN):

    # Créer le contrôleur et le gimbal
    creat_circle(N_LOC, Prefix, N_CTL)
    # Créer les groupes offset
    creat_group_offset(Prefix, N_CTL)
    # Ajouter l'attribut de visibilité
    creat_visibility_attr(Prefix, N_CTL, ATT_LN, ATT_NN)


# CREE CTL + GRP_OFFSET + ATTR_VISIBILITY
# N_LOC = nom du Locator éxistent
# Prefix = prefix avec le nom du CTL et ou du LOC (ex posC = C_ pour Position Central)
# N_CTL = nom du CTL a créé
# ATT_LN = nom attribute long name a créé pour visibility ON/OFF de la Gimball
# ATT_NN = nom attribute nice name a créé pour visibility ON/OFF de la Gimball
def creat_complet_cube_CTL(N_LOC, N_CTL, Prefix, ATT_LN, ATT_NN):

    # Créer le contrôleur et le gimbal
    creat_cube(N_LOC, Prefix, N_CTL)
    # Créer les groupes offset
    creat_group_offset(Prefix, N_CTL)
    # Ajouter l'attribut de visibilité
    creat_visibility_attr(Prefix, N_CTL, ATT_LN, ATT_NN)

# CREE CTL + GRP_OFFSET + ATTR_VISIBILITY
# Prefix = Prefix de l'element pour le quel ont veut créé un cercle (peut etres une liste)
# CoreNames = Nom sens prefix n'y suffix de l'element pour le quel ont veut créé un cercle (peut etres une liste)
# Suffix = Suffix de l'element pour le quel ont veut créé un cercle (peut etres une liste)
# Exclude = Liste de nom d'element spécifique a exclure
# ATTENTION Prefix / CoreName et Suffix peuvent etres = '*' mais pas tous en meme temps
def creat_complet_circle_CTL_for(Prefix, CoreNames, Suffix, Exclude):
    
    
    if isinstance(CoreNames, str):
        CoreNames = [CoreNames]

    for CoreName in CoreNames:
        Element_Liste = cmds.ls(Prefix + CoreName + Suffix)
        if Exclude is not None:
            Element_Liste = [elem for elem in Element_Liste if not any(excl in elem for excl in Exclude)]

        for elem in Element_Liste:
            NameNoS = elem.replace(Suffix, '')
            Name = NameNoS.replace(Prefix, '')

            N_LOC = Name
            N_CTL = Name
            ATT_LN = Prefix + Name + gimbal + 'Vis'
            ATT_NN = 'Gimbal_Vis'

            creat_complet_circle_CTL(N_LOC, N_CTL, Prefix, ATT_LN, ATT_NN)

# CREE CTL + GRP_OFFSET + ATTR_VISIBILITY
# Prefix = Prefix de l'element pour le quel ont veut créé un cercle (peut etres une liste)
# CoreNames = Nom sens prefix n'y suffix de l'element pour le quel ont veut créé un cercle (peut etres une liste)
# Suffix = Suffix de l'element pour le quel ont veut créé un cercle (peut etres une liste)
# Exclude = Liste de nom d'element spécifique a exclure
# ATTENTION Prefix / CoreName et Suffix peuvent etres = '*' mais pas tous en meme temps
def creat_complet_cube_CTL_for(Prefix, CoreNames, Suffix, Exclude):


    if isinstance(CoreNames, str):
        CoreNames = [CoreNames]

    for CoreName in CoreNames:
        Element_Liste = cmds.ls(Prefix + CoreName + Suffix)
        if Exclude is not None:
            Element_Liste = [elem for elem in Element_Liste if not any(excl in elem for excl in Exclude)]

        for elem in Element_Liste:
            NameNoS = elem.replace(Suffix, '')
            Name = NameNoS.replace(Prefix, '')

            N_LOC = Name
            N_CTL = Name
            ATT_LN = Prefix + Name + gimbal + 'Vis'
            ATT_NN = 'Gimbal_Vis'

            creat_complet_cube_CTL(N_LOC, N_CTL, Prefix, ATT_LN, ATT_NN)

# CREE JOINT
# Pos_Liste liste de nom d'element pour les quel ont veut cree des joints
# Old_Suffix = suffix des element sur les quel ont cree des joint
# New_Suffix = suffix a utiliser pour les joint (ex : _JOINT ou _JNT)
def create_joint_at_for(Pos_Liste, Old_Suffix, New_Suffix):

    for Loc in Pos_Liste:
        joint_name=Loc.replace(Old_Suffix, New_Suffix)

        cmds.select(clear=True)
        joint_base= cmds.joint(name=joint_name, radius=3)

        #placer les joint sur les loc
        AllLoc_t = cmds.xform(Loc, query=True, worldSpace=True, translation=True) 
        AllLoc_r = cmds.xform(Loc, query=True, worldSpace=True, rotation=True)

        cmds.xform(joint_base, worldSpace=True, translation=AllLoc_t) 
        cmds.xform(joint_base, worldSpace=True, rotation=AllLoc_r)

        cmds.makeIdentity(joint_base, apply=True, t=0, r=1, s=1, n=0)

# MODIFIER LA ROTATION D'UN CTL ET DE SA GIMBAL
# Prefix = Prefix de ou des element a modifier
# CurveN = Nom de la curve sens prefix, n'y suffix
# Rx, Ry, Rz = valeur de rotation a attribué au axe x, y, et z
# ATTENTION modification apporter uniquement a la Shape du CTL et de la GIMBAL
def custom_curve_rot(Prefix, CurveN, Rx, Ry, Rz):
    # CTL
    # Rotate la shape
    cv = cmds.ls(Prefix + CurveN + ctlN + '.cv[*]', fl=True)
    cmds.rotate(Rx, Ry, Rz, cv, relative=True, objectSpace=True)

    # CTL Gimbal
    # Rotate la shape
    cv = cmds.ls(Prefix + CurveN + gimbal + '.cv[*]', fl=True)
    cmds.rotate(Rx, Ry, Rz, cv, relative=True, objectSpace=True)

# MODIFIER LA TRANSLATION D'UN CTL ET DE SA GIMBAL
# Prefix = Prefix de ou des element a modifier
# CurveN = Nom de la curve sens prefix, n'y suffix
# Tx, Ty, Tz = valeur de translate a attribué au axe x, y, et z
# ATTENTION modification apporter uniquement a la Shape du CTL et de la GIMBAL
def custom_curve_trs(Prefix, CurveN, Tx, Ty, Tz):
    # CTL
    # Translate la shape
    cv = cmds.ls(Prefix + CurveN + ctlN + '.cv[*]', fl=True)
    cmds.move(Tx, Ty, Tz, cv, relative=True, objectSpace=True)

    # CTL Gimbal
    # Translate la shape
    cv = cmds.ls(Prefix + CurveN + gimbal + '.cv[*]', fl=True)
    cmds.move(Tx, Ty, Tz, cv, relative=True, objectSpace=True)

# MODIFIER LE SCALE D'UN CTL ET DE SA GIMBAL
# Prefix = Prefix de ou des element a modifier
# CurveN = Nom de la curve sens prefix, n'y suffix
# Sx, Sy, Sz = valeur de scale a attribué au axe x, y, et z
# ATTENTION modification apporter uniquement a la Shape du CTL et de la GIMBAL
def custom_curve_scl(Prefix, CurveN, Sx, Sy, Sz):
    # CTL
    # Scale la shape
    cv = cmds.ls(Prefix + CurveN + ctlN + '.cv[*]', fl=True)
    cmds.scale(Sx, Sy, Sz, cv, relative=True, objectSpace=True)

    # CTL Gimbal
    # Scale la shape
    cv = cmds.ls(Prefix + CurveN + gimbal + '.cv[*]', fl=True)
    cmds.scale(Sx, Sy, Sz, cv, relative=True, objectSpace=True)

# MODIFIE LA COULEUR
# CurveN = Nom de la curve a modifier
# Type = CTL, Gimbal ou Both celon si on veut change le CTL ou le Gimball ou les deux
# R, G, B = valeur RGB de la couleur voulu
def custom_curve_color_select (CurveN, Type, R, G, B):
    
    for curve_shape in CurveN:
        
        if Type == 'CTL':
            edit_curve_shape = cmds.listRelatives(curve_shape, shapes=True)
            edit_curve_shape = edit_curve_shape[0]
            # Activer l'override des attributs
            cmds.setAttr(edit_curve_shape + ".overrideEnabled", 1)
            # Activer l'utilisation des couleurs RGB personnalisées
            cmds.setAttr(edit_curve_shape + ".overrideRGBColors", 1)
            # Définir la couleur avec des valeurs RGB
            cmds.setAttr(edit_curve_shape + ".overrideColorR", R)
            cmds.setAttr(edit_curve_shape + ".overrideColorG", G)
            cmds.setAttr(edit_curve_shape + ".overrideColorB", B)

        elif Type == 'Gimbal':
            edit_Gimbal_shape = curve_shape.replace( ctlN, gimbal)
            curve_shape_Gimbol = cmds.listRelatives(edit_Gimbal_shape, shapes=True)
            curve_shape_Gimbol = curve_shape_Gimbol[0]
            # Activer l'override des attributs
            cmds.setAttr(curve_shape_Gimbol + ".overrideEnabled", 1)
            # Activer l'utilisation des couleurs RGB personnalisées
            cmds.setAttr(curve_shape_Gimbol + ".overrideRGBColors", 1)
            # Définir la couleur avec des valeurs RGB
            cmds.setAttr(curve_shape_Gimbol + ".overrideColorR", R)
            cmds.setAttr(curve_shape_Gimbol + ".overrideColorG", G)
            cmds.setAttr(curve_shape_Gimbol + ".overrideColorB", B)

        elif Type == 'Both':
            edit_curve_shape = cmds.listRelatives(curve_shape, shapes=True)
            edit_curve_shape = edit_curve_shape[0]
            # Activer l'override des attributs
            cmds.setAttr(edit_curve_shape + ".overrideEnabled", 1)
            # Activer l'utilisation des couleurs RGB personnalisées
            cmds.setAttr(edit_curve_shape + ".overrideRGBColors", 1)
            # Définir la couleur avec des valeurs RGB
            cmds.setAttr(edit_curve_shape + ".overrideColorR", R)
            cmds.setAttr(edit_curve_shape + ".overrideColorG", G)
            cmds.setAttr(edit_curve_shape + ".overrideColorB", B)
        

            edit_Gimbal_shape = curve_shape.replace( ctlN, gimbal)
            curve_shape_Gimbol = cmds.listRelatives(edit_Gimbal_shape, shapes=True)
            curve_shape_Gimbol = curve_shape_Gimbol[0]
            # Activer l'override des attributs
            cmds.setAttr(curve_shape_Gimbol + ".overrideEnabled", 1)
            # Activer l'utilisation des couleurs RGB personnalisées
            cmds.setAttr(curve_shape_Gimbol + ".overrideRGBColors", 1)
            # Définir la couleur avec des valeurs RGB
            cmds.setAttr(curve_shape_Gimbol + ".overrideColorR", R)
            cmds.setAttr(curve_shape_Gimbol + ".overrideColorG", G)
            cmds.setAttr(curve_shape_Gimbol + ".overrideColorB", B)
            
        else:
            raise ValueError("Invalide Sahpe type, CTL or Gimbal or Both")

# MODIFIE L'EPPAISSEUR DE LA CURVE
# CurveN = Nom de la curve a modifier
# Type = CTL, Gimbal ou Both celon si on veut change le CTL ou le Gimball ou les deux
# LineWidth = valeur de l'eppaisseur voulue
def custom_curve_width_select (CurveN, Type, LineWidth):

    for curve_shape in CurveN:

        if Type == 'CTL':
            edit_curve_shape = cmds.listRelatives(curve_shape, shapes=True)
            edit_curve_shape = edit_curve_shape[0]
            cmds.setAttr(edit_curve_shape + ".lineWidth", LineWidth)

        elif Type == 'Gimbal':
            edit_Gimbal_shape = curve_shape.replace( ctlN, gimbal)

            curve_shape_Gimbol = cmds.listRelatives(edit_Gimbal_shape, shapes=True)
            curve_shape_Gimbol = curve_shape_Gimbol[0]
            cmds.setAttr(curve_shape_Gimbol + ".lineWidth", LineWidth)

        elif Type == 'Both':
            edit_curve_shape = cmds.listRelatives(curve_shape, shapes=True)

            edit_curve_shape = edit_curve_shape[0]
            cmds.setAttr(edit_curve_shape + ".lineWidth", LineWidth)
        
            edit_Gimbal_shape = curve_shape.replace(ctlN, gimbal)

            curve_shape_Gimbol = cmds.listRelatives(edit_Gimbal_shape, shapes=True)
            curve_shape_Gimbol = curve_shape_Gimbol[0]
            cmds.setAttr(curve_shape_Gimbol + ".lineWidth", LineWidth)
            
        else:
            raise ValueError("Invalide Sahpe type, CTL or Gimbal or Both")

# MODIFIE TOUT TRANSLATE, ROTATE, SCALE D'UN CTL
# Prefix = prefix de l'element a modifié
# CurveN = Nom de la curve a modifié
# Tx, Ry, Sz = Translate, Rotate, Scale a applique
# ATTENTION modification apporter uniquement a la Shape du CTL et de la GIMBAL
def custom_curve(Prefix, CurveN, Tx, Ty, Tz, Rx, Ry, Rz, Sx, Sy, Sz):
    custom_curve_rot(Prefix, CurveN, Rx, Ry, Rz)
    custom_curve_scl(Prefix, CurveN, Sx, Sy, Sz)
    custom_curve_trs(Prefix, CurveN, Tx, Ty, Tz)
    
# MODIFIE LA COULEUR
# R, G, B = valeur RGB de la couleur voulu
def custom_curve_color(Prefix, CoreName, Suffix, R, G, B):
    edit_curve_liste = cmds.ls(Prefix + CoreName + Suffix)

    for curve_shape in edit_curve_liste:
        cmds.setAttr(curve_shape + ".overrideEnabled", 1)
        # Activer l'utilisation des couleurs RGB personnalisées
        cmds.setAttr(curve_shape + ".overrideRGBColors", 1)
        # Définir la couleur avec des valeurs RGB
        cmds.setAttr(curve_shape + ".overrideColorR", R)
        cmds.setAttr(curve_shape + ".overrideColorG", G)
        cmds.setAttr(curve_shape + ".overrideColorB", B)

# MODIFIE L'EPPAISSEUR DE LA CURVE
# LineWidth = valeur de l'eppaisseur voulue
def custom_curve_width(Prefix, CoreName, Suffix, LineWidth):
    edit_curve_liste = cmds.ls(Prefix + CoreName + Suffix)
    print (edit_curve_liste)
    for curve_shape in edit_curve_liste:
        cmds.setAttr(curve_shape + ".lineWidth", LineWidth)


########################################################################################################################
########################################################################################################################

                                                # CREATION DU RIG #

########################################################################################################################
########################################################################################################################



#### CREATE ALL ORIGINE LOC ####
def create_all_origine_LOC():

    # CREATE LEFT ORIGINE LOC
    def creat_left_origine_loc():

        # Base CTL
        #CharacterNode
        creat_loc_at( LOC_N = 'CharacterNode', Prefix= posC, TX = 0, TY = 0, TZ = 0, RX = 0, RY = 0, RZ = 0)
        # MasterWalk
        creat_loc_at( LOC_N = 'MasterWalk', Prefix= posC, TX = 0, TY = 0, TZ = 0, RX = 0, RY = 0, RZ = 0)
        # Root
        creat_loc_at( LOC_N = 'Root', Prefix= posC, TX = 0, TY = 0, TZ = 0, RX = 0, RY = 0, RZ = 0)
        # Middle
        creat_loc_at( LOC_N = 'Middle', Prefix= posC, TX = 0, TY = 61, TZ = 0, RX = 0, RY = 0, RZ = 0)


        # Pelvis to Neck
        # Pelvis
        creat_loc_at( LOC_N = 'Pelvis', Prefix= posC, TX = 0, TY = 35, TZ = 0, RX = 0, RY = 0, RZ = 0)
        # Chest Base
        creat_loc_at( LOC_N = 'ChestB', Prefix= posC, TX = 0, TY = 15, TZ = 0, RX = 0, RY = 0, RZ = 0)
        # Chest Middle
        creat_loc_at( LOC_N = 'ChestM', Prefix= posC, TX = 0, TY = 48, TZ = 0, RX = 0, RY = 0, RZ = 0)



        # Head CTL
        # Head Base
        creat_loc_at( LOC_N = 'HeadB', Prefix= posC, TX = 0, TY = 83.5, TZ = 0, RX = 0, RY = 0, RZ = 0)
        #Head Middle
        creat_loc_at( LOC_N = 'HeadM', Prefix= posC, TX = 0, TY = 100, TZ = 0, RX = 0, RY = 0, RZ = 0)


        #### LOC LEFT SIDE #####

        # Left Leg
        # Thigh
        creat_loc_at( LOC_N = 'Thigh', Prefix= posL, TX = 15, TY = 25, TZ = 0, RX = 0, RY = 0, RZ = 0)
        # Foot
        creat_loc_at( LOC_N = 'Foot', Prefix= posL, TX = 15, TY = 8, TZ = 0, RX = 0, RY = 0, RZ = 0)
        # Heel
        creat_loc_at( LOC_N = 'Heel', Prefix= posL, TX = 15, TY = 0, TZ = -4, RX = 0, RY = 0, RZ = 0)

        # Left Arm
        # Shoulder
        creat_loc_at( LOC_N = 'Shoulder', Prefix= posL, TX = 33, TY = 72, TZ = 0, RX = 0, RY = 0, RZ = 18.5)
        # Pinkie Finger
        creat_loc_at( LOC_N = 'PinkieF', Prefix= posL, TX = 42.6, TY = 41, TZ = -5, RX = 0, RY = 0, RZ = 13.1) 
        # Middle Finger
        creat_loc_at( LOC_N = 'MiddleF', Prefix= posL, TX = 42.6, TY = 41, TZ = 0.5, RX = 0, RY = 0, RZ = 13.1) 
        # Fore Finger
        creat_loc_at( LOC_N = 'ForeF', Prefix= posL, TX = 42.6, TY = 41, TZ = 5.9, RX = 0, RY = 0, RZ = 13.1)
        # Thumb Finger
        creat_loc_at( LOC_N = 'ThumbF', Prefix= posL, TX = 41.6, TY = 44.3, TZ = 8.5, RX = -59, RY = -0.4, RZ = 15.3)

        # Left Head Element
        # Left Tooth A
        creat_loc_at( LOC_N = 'ToothA', Prefix= posL, TX = 10.5, TY = 80.5, TZ = 24.5, RX = 15, RY = 0, RZ = 0)
        # Left Tooth B
        creat_loc_at( LOC_N = 'ToothB', Prefix= posL, TX = 15.3, TY = 79, TZ = 24, RX = 15, RY = 0, RZ = 0)
        # Left Eye
        creat_loc_at( LOC_N = 'Eye', Prefix= posL, TX = 10, TY = 100, TZ = 25, RX = 0, RY = 0, RZ = 0)
        # Left Rock Head Base
        creat_loc_at( LOC_N = 'RockB', Prefix= posL, TX = 12, TY = 116.5, TZ = -8, RX = 0, RY = 0, RZ = 0)
        # Left Rock Head Middle
        creat_loc_at( LOC_N = 'RockM', Prefix= posL, TX = 12, TY = 120, TZ = -8, RX = 0, RY = 0, RZ = 0)
    creat_left_origine_loc()

    # CREATE RIGHT ORIGINE LOC
    def create_right_origine_loc():
        # SYM LEFT ORIGINE LOC TO RIGHT
            def sym_loc_left_to_right(OriginalSide='L_', NewSide = 'R_', Element_Liste='L_*_LOC', Exclude = ['_ToothA_', '_ToothB_', '_RockB_', '_RockM_']):
                
                #### LOC RIGHT SIDE #####
                # Cree les LOC symetrique entre le coté Left et Right
                # Lister et exclure les element unique au coté Left
                symmetrical(OriginalSide, NewSide, Element_Liste, Exclude)
            sym_loc_left_to_right()

            # CREATE UNIQUE ORIGINE RIGHT LOC
            def creat_right_unique_origine_LOC():
                # Cree les LOC unique au cote Right

                # Right Tooth C
                creat_loc_at( LOC_N = 'ToothC', Prefix= posR, TX = -15.3, TY = 78.5, TZ = 22.5, RX = 18.7, RY = 0, RZ = 0)
                # Right Mushroum Main
                creat_loc_at( LOC_N = 'MushroumM', Prefix= posR, TX = -14, TY = 111.6, TZ = 11, RX = 0, RY = 0, RZ = 0)
                # Right Mushroum A
                creat_loc_at( LOC_N = 'MushroumA', Prefix= posR, TX =-16, TY = 111, TZ = 9, RX = 1.2, RY = 6, RZ = 11.3)
                # Right Mushroum B
                creat_loc_at( LOC_N = 'MushroumB', Prefix= posR, TX = -12.7, TY = 111.6, TZ = 12, RX = 14.4, RY = 40, RZ = -7)
                # Right Mushroum C
                creat_loc_at( LOC_N = 'MushroumC', Prefix= posR, TX = -14.5, TY = 111.7, TZ = 12.6, RX = 58.4, RY = -61, RZ = -50.3)
            creat_right_unique_origine_LOC()
    create_right_origine_loc()
create_all_origine_LOC()


#### CREATE ALL FK CTL ####
def create_all_fk_CTL():
    def create_all_left_fk_CTL():
        #### CREATE All LEFT CTL
        #Create Left circle CTL
        creat_complet_circle_CTL_for(Prefix = posL, CoreNames = '*', Suffix=locO, Exclude= ['Shoulder', 'RockM', 'Heel'])

        #Creat Left cube CTRL
        creat_complet_cube_CTL_for(Prefix = posL, CoreNames = ['Shoulder', 'RockM', 'Heel'], Suffix=locO, Exclude=None)
    create_all_left_fk_CTL()

    def create_all_right_fk_CTL():
        #### CREATE All RIGHT CTL
        #Create Right circle CTL
        creat_complet_circle_CTL_for(Prefix = posR, CoreNames = '*', Suffix=locO, Exclude= ['Shoulder', 'Heel'])

        #Creat Right cube CTRL
        creat_complet_cube_CTL_for(Prefix = posR, CoreNames = ['Shoulder', 'Heel'], Suffix=locO, Exclude=None)
    create_all_right_fk_CTL()

    def create_all_center_fk_CTL():
        #### CREATE All CENTER CTL
        #Create Center circle CTL
        creat_complet_circle_CTL_for(Prefix = posC, CoreNames = '*', Suffix=locO, Exclude= ['HeadM', 'ChestM'])

        #Creat Center cube CTRL
        creat_complet_cube_CTL_for(Prefix = posC, CoreNames = ['HeadM', 'ChestM'], Suffix=locO, Exclude=None)
    create_all_center_fk_CTL()
create_all_fk_CTL()


#### CUSTOM ALL FK CTL ####
def custome_all_fk_CTL():

    # Custom Shape et pos, rot, scl
    def custom_pos_rot_scl():
        def arm():
            # Arm
            def shoulder(Prefix, CurveN, Tx, Ty, Tz, Sx, Sy, Sz):
                custom_curve_scl(Prefix, CurveN, Sx, Sy, Sz)
                custom_curve_trs(Prefix, CurveN, Tx, Ty, Tz)

            shoulder(Prefix = posL, CurveN = 'Shoulder', Tx = 0, Ty = -33, Tz = 0, Sx = 3.8, Sy = 16.8, Sz = 8.5)
            shoulder(Prefix = posR, CurveN = 'Shoulder', Tx = 0, Ty = -33, Tz = 0, Sx = 3.8, Sy = 16.8, Sz = 8.5)

            def pinkie(Prefix, CurveN, Tx, Ty, Tz, Rx, Ry, Rz, Sx, Sy, Sz):
                custom_curve_rot(Prefix, CurveN, Rx, Ry, Rz)
                custom_curve_scl(Prefix, CurveN, Sx, Sy, Sz)
                custom_curve_trs(Prefix, CurveN, Tx, Ty, Tz)

            pinkie(Prefix = posL, CurveN = 'PinkieF', Tx = 0, Ty = -3.5, Tz = 0, Rx = 90, Ry = 0, Rz = 0, Sx = 0.35, Sy = 0.35, Sz = 0.35)
            pinkie(Prefix = posR, CurveN = 'PinkieF', Tx = 0, Ty = -3.5, Tz = 0, Rx = 90, Ry = 0, Rz = 0, Sx = 0.35, Sy = 0.35, Sz = 0.35)

            def fore(Prefix, CurveN, Tx, Ty, Tz,Rx, Ry, Rz, Sx, Sy, Sz):
                custom_curve_rot(Prefix, CurveN, Rx, Ry, Rz)
                custom_curve_scl(Prefix, CurveN, Sx, Sy, Sz)
                custom_curve_trs(Prefix, CurveN, Tx, Ty, Tz)

            fore(Prefix = posL, CurveN = 'ForeF', Tx = 0, Ty = -3.5, Tz = 0, Rx = 90, Ry = 0, Rz = 0, Sx = 0.35, Sy = 0.35, Sz = 0.35)
            fore(Prefix = posR, CurveN = 'ForeF', Tx = 0, Ty = -3.5, Tz = 0, Rx = 90, Ry = 0, Rz = 0, Sx = 0.35, Sy = 0.35, Sz = 0.35)

            def middle(Prefix, CurveN, Tx, Ty, Tz, Rx, Ry, Rz, Sx, Sy, Sz):
                custom_curve_rot(Prefix, CurveN, Rx, Ry, Rz)
                custom_curve_scl(Prefix, CurveN, Sx, Sy, Sz)
                custom_curve_trs(Prefix, CurveN, Tx, Ty, Tz)

            middle(Prefix = posL, CurveN = 'MiddleF', Tx = 0, Ty = -4, Tz = 0, Rx = 90, Ry = 0, Rz = 0, Sx = 0.4, Sy = 0.4, Sz = 0.4)
            middle(Prefix = posR, CurveN = 'MiddleF', Tx = 0, Ty = -4, Tz = 0, Rx = 90, Ry = 0, Rz = 0, Sx = 0.4, Sy = 0.4, Sz = 0.4)

            def thumb(Prefix, CurveN, Tx, Ty, Tz, Rx, Ry, Rz, Sx, Sy, Sz):
                custom_curve_rot(Prefix, CurveN, Rx, Ry, Rz)
                custom_curve_scl(Prefix, CurveN, Sx, Sy, Sz)
                custom_curve_trs(Prefix, CurveN, Tx, Ty, Tz)

            thumb(Prefix = posL, CurveN = 'ThumbF', Tx = 0, Ty = -4, Tz = 0, Rx = 90, Ry = 0, Rz = 0, Sx = 0.5, Sy = 0.5, Sz = 0.5)
            thumb(Prefix = posR, CurveN = 'ThumbF', Tx = 0, Ty = -4, Tz = 0, Rx = 90, Ry = 0, Rz = 0, Sx = 0.5, Sy = 0.5, Sz = 0.5)
        arm()

        def leg():

            # Thigh
            custom_curve(Prefix = posL, CurveN = 'Thigh', Tx = 0, Ty = -13, Tz = 0, Rx = 90, Ry = 0, Rz = 0, Sx = 0.7, Sy = 0.7, Sz = 0.7)
            custom_curve(Prefix = posR, CurveN = 'Thigh', Tx = 0, Ty = -13, Tz = 0, Rx = 90, Ry = 0, Rz = 0, Sx = 0.7, Sy = 0.7, Sz = 0.7)
            # Foot
            custom_curve(Prefix = posL, CurveN = 'Foot', Tx = 0, Ty = 1, Tz = 0, Rx = 90, Ry = 0, Rz = 0, Sx = 1, Sy = 1, Sz = 1)
            custom_curve(Prefix = posR, CurveN = 'Foot', Tx = 0, Ty = 1, Tz = 0, Rx = 90, Ry = 0, Rz = 0, Sx = 1, Sy = 1, Sz = 1)

            # Heel
            custom_curve(Prefix = posL, CurveN = 'Heel', Tx = 0, Ty = 0, Tz = 7.7, Rx = 0, Ry = 0, Rz = 0, Sx = 6.2, Sy = 4, Sz = 10.5)
            custom_curve(Prefix = posR, CurveN = 'Heel', Tx = 0, Ty = 0, Tz = -7.7, Rx = 0, Ry = 0, Rz = 0, Sx = 6.2, Sy = 4, Sz = 10.5)
        leg()
            
        def head():
            # HeadB
            custom_curve(Prefix = posC, CurveN = 'HeadB', Tx = 0, Ty = 0, Tz = 0, Rx = 90, Ry = 0, Rz = 0, Sx = 5, Sy = 5, Sz = 5)
            # HeadM
            custom_curve(Prefix = posC, CurveN = 'HeadM', Tx = 0, Ty = -16, Tz = 0, Rx = 0, Ry = 0, Rz = 0, Sx = 35, Sy = 17, Sz = 28)

            # Eye
            custom_curve(Prefix = posL, CurveN = 'Eye', Tx = 0, Ty = 0, Tz = 2.5, Rx = 0, Ry = 0, Rz = 0, Sx = 0.5, Sy = 0.5, Sz = 0.5)
            custom_curve(Prefix = posR, CurveN = 'Eye', Tx = 0, Ty = 0, Tz = -2.5, Rx = 0, Ry = 0, Rz = 0, Sx = 0.5, Sy = 0.5, Sz = 0.5)

            # RockB
            custom_curve(Prefix = posL, CurveN = 'RockB', Tx = 0, Ty = 2.2, Tz = 2.5, Rx = 90, Ry = 0, Rz = 0, Sx = 1.5, Sy = 1.5, Sz = 1.5)
            # RockM
            custom_curve(Prefix = posL, CurveN = 'RockM', Tx = 0, Ty = 0, Tz = -10, Rx = 90, Ry = 0, Rz = 0, Sx = 8.5, Sy = 3, Sz = 11)

            # Mushroum
            custom_curve(Prefix = posR, CurveN = 'MushroumM', Tx = 0, Ty = 1.8, Tz = 0, Rx = 90, Ry = 0, Rz = 0, Sx = 0.9, Sy = 0.9, Sz = 0.9)
            custom_curve(Prefix = posR, CurveN = 'MushroumA', Tx = 0, Ty = 14.5, Tz = 0, Rx = 90, Ry = 0, Rz = 0, Sx = 1.1, Sy = 1.1, Sz = 1.1)
            custom_curve(Prefix = posR, CurveN = 'MushroumB', Tx = 0, Ty = 4.2, Tz = 0, Rx = 90, Ry = 0, Rz = 0, Sx = 0.35, Sy = .35, Sz = .35)
            custom_curve(Prefix = posR, CurveN = 'MushroumC', Tx = 0, Ty = 2.4, Tz = 0, Rx = 90, Ry = 0, Rz = 0, Sx = 0.15, Sy = 0.15, Sz = 0.15)

            # Tooth
            custom_curve(Prefix = posL, CurveN = 'ToothB', Tx = 0, Ty = 3.4, Tz = 0, Rx = 90, Ry = 0, Rz = 0, Sx = 0.6, Sy = 0.6, Sz = 0.6)
            custom_curve(Prefix = posL, CurveN = 'ToothA', Tx = 0, Ty = 2, Tz = 0, Rx = 90, Ry = 0, Rz = 0, Sx = 0.4, Sy = 0.4, Sz = 0.4)
            custom_curve(Prefix = posR, CurveN = 'ToothC', Tx = 0, Ty = 4.7, Tz = 0, Rx = 90, Ry = 0, Rz = 0, Sx = 0.5, Sy = 0.5, Sz = 0.5)
        head()

        def body():
            # ChestB
            custom_curve(Prefix = posC, CurveN = 'ChestB', Tx = 0, Ty = 0, Tz = 0, Rx = 90, Ry = 0, Rz = 0, Sx = 5, Sy = 5, Sz = 5 )
            # ChestM
            custom_curve(Prefix = posC, CurveN = 'ChestM', Tx = 0, Ty = -32.4, Tz = 0, Rx = 0, Ry = 0, Rz = 0, Sx = 35, Sy = 33, Sz = 32)

            # Pelvis
            custom_curve(Prefix = posC, CurveN = 'Pelvis', Tx = 0, Ty = 0, Tz = 0, Rx = 90, Ry = 0, Rz = 0, Sx = 4.5, Sy = 4.5, Sz = 4.5)
        body()

        def base():
            # CharacterNode
            custom_curve(Prefix = posC, CurveN = 'CharacterNode', Tx = 0, Ty = 0, Tz = 0, Rx = 90, Ry = 0, Rz = 0, Sx = 5, Sy = 5, Sz = 5)

            # MasterWalk
            custom_curve(Prefix = posC, CurveN = 'MasterWalk', Tx = 0, Ty = 0, Tz = 0, Rx = 90, Ry = 0, Rz = 0, Sx = 4, Sy = 4, Sz = 4)

            # Root
            custom_curve(Prefix = posC, CurveN = 'Root', Tx = 0, Ty = 0, Tz = 0, Rx = 90, Ry = 0, Rz = 0, Sx = 3, Sy = 3, Sz = 3)

            # Middle
            custom_curve(Prefix = posC, CurveN = 'Middle', Tx = 0, Ty = 0, Tz = 0, Rx = 90, Ry = 0, Rz = 0, Sx = 4.5, Sy = 4.5, Sz = 4.5)
        base()
    custom_pos_rot_scl()

    # Custom Color
    def custom_color():
        # Custom CTL Color
        # Left
        custom_curve_color(Prefix = 'L_', CoreName = '*', Suffix = ctlN, R = 0.9, G = 0.2, B = 0.2)
        # Right
        custom_curve_color(Prefix = 'R_', CoreName = '*', Suffix = ctlN, R = 0.5, G = 0.2, B = 0.7)
        # Centre
        custom_curve_color(Prefix = 'C_', CoreName = '*', Suffix = ctlN, R = 0.8, G = 0.8, B = 0.1)

        # Custom gimbal color
        custom_curve_color(Prefix = '*', CoreName = '*', Suffix = '*'+gimbal, R = 1, G = 1, B = 1)
    custom_color()

    # Custom Width for all ctl and gimbal
    def custom_width():
        custom_curve_width(Prefix = '*', CoreName= '*', Suffix = ctlN, LineWidth = 2.3)
    
    custom_width()
custome_all_fk_CTL()


### CREATE ALL JOINT ####
def create_all_joint():
    Loc_Liste = cmds.ls('*' + locO)
    create_joint_at_for(Pos_Liste = Loc_Liste, Old_Suffix = locO, New_Suffix = jnt)
create_all_joint()


#### CREAT HIERARCHIE ####
# Hierarchie Map
def hierarchie():
    def creat_hierarchie_Roki(SuffixP, SuffixE):

        def creat_left_hierarchie(Prefix):
            hierarchy_map = {
                
                # Left Shoulder
                Prefix + 'Shoulder' + SuffixP : [
                                                Prefix + 'PinkieF' + SuffixE, 
                                                Prefix + 'ForeF' + SuffixE,
                                                Prefix + 'MiddleF' + SuffixE,
                                                Prefix + 'ThumbF' + SuffixE ],

                #Left Leg
                Prefix + 'Thigh' + SuffixP : Prefix + 'Foot' + SuffixE,
                Prefix + 'Foot' + SuffixP : Prefix + 'Heel' + SuffixE,

                # Left Rock
                Prefix + 'RockB' + SuffixP : Prefix + 'RockM' + SuffixE,

                }
            
            for parent, child in hierarchy_map.items():
                cmds.parent(child, parent)
        creat_left_hierarchie(Prefix = posL)

        def creat_right_hierarchie(Prefix):
            hierarchy_map = {
                
                # Right Shoulder
                Prefix + 'Shoulder' + SuffixP : [
                                                Prefix + 'PinkieF' + SuffixE, 
                                                Prefix + 'ForeF' + SuffixE,
                                                Prefix + 'MiddleF' + SuffixE,
                                                Prefix + 'ThumbF' + SuffixE ],

                # Right Leg
                Prefix + 'Thigh' + SuffixP : Prefix + 'Foot' + SuffixE,
                Prefix + 'Foot' + SuffixP : Prefix + 'Heel' + SuffixE,

                # Right Rock
                Prefix + 'MushroumM' + SuffixP : [
                                                Prefix + 'MushroumA' + SuffixE,
                                                Prefix + 'MushroumB' + SuffixE,
                                                Prefix + 'MushroumC' + SuffixE ],

                }
            
            for parent, child in hierarchy_map.items():
                cmds.parent(child, parent)
        creat_right_hierarchie(Prefix = posR)

        def create_center_hierarchie(Prefix):
            hierarchy_map = {
                
                #Base CTL
                Prefix + 'CharacterNode' + SuffixP : Prefix + 'MasterWalk' + SuffixE,
                Prefix + 'MasterWalk' + SuffixP : Prefix + 'Root' + SuffixE,

                # Chest CTL
                Prefix + 'Root' + SuffixP : Prefix + 'Middle' + SuffixE,
                Prefix + 'Middle' + SuffixP : [
                                                Prefix + 'Pelvis' + SuffixE,
                                                Prefix + 'ChestB' + SuffixE ],

                Prefix + 'ChestB' + SuffixP : Prefix + 'ChestM' + SuffixE,

                # Head CTL
                Prefix + 'ChestM' + SuffixP : Prefix + 'HeadB' + SuffixE,
                Prefix + 'HeadB' + SuffixP : Prefix + 'HeadM' + SuffixE,
                }
            
            for parent, child in hierarchy_map.items():
                cmds.parent(child, parent)
        create_center_hierarchie(Prefix = posC)

        def create_merge_hierarchie():
            hierarchy_map = {
                
                # Leg to Pelvis
                posC + 'Pelvis' + SuffixP : [# Left
                                            posL + 'Thigh' + SuffixE,
                                            # Right
                                            posR + 'Thigh' + SuffixE ],

                # Arm To Chest
                # Left
                posC + 'ChestM' + SuffixP : [# Left
                                            posL + 'Shoulder' + SuffixE,
                                            # Right
                                            posR + 'Shoulder' + SuffixE ,
                                            posR + 'ToothC' + SuffixE,
                                            posL + 'ToothA' + SuffixE, 
                                            posL + 'ToothB' + SuffixE ],

                # Head Element to Head
                posC + 'HeadM' + SuffixP : [ # Left
                                            posL + 'RockB' + SuffixE, 
                                            posL + 'Eye' + SuffixE,
                                            # Right
                                            posR + 'MushroumM' + SuffixE, 
                                            posR + 'Eye' + SuffixE ],
                }

            for parent, child in hierarchy_map.items():
                cmds.parent(child, parent)
        create_merge_hierarchie()

    # Appel hierarchie map for
    # Joint
    creat_hierarchie_Roki(SuffixP = jnt, SuffixE = jnt)
    # Origine Loc
    creat_hierarchie_Roki(SuffixP = locO, SuffixE = locO)
    # CTL
    creat_hierarchie_Roki(SuffixP = ctlN, SuffixE = grpO)
hierarchie()


#### CREATE CONSTRAINT PARENT ####
def create_parent_constraint():
    Joint_child = cmds.ls('*_JNT')
    

    #Cherche les nm d'un joint et du ctl correspondant puis faire la contraint parent
    for joint in Joint_child:
        #Prendre les nom et retiré les suffix JNT pour avoir les nom des CTL, stock ces nom
        base_name = joint.replace('_JNT', "")
        ctl_name = base_name + 'Gimbal_CTL'
        #Si et seulement si le CTL existe créé une constraint entre lui et le joint du meme nom
        if cmds.objExists(ctl_name):
            cmds.parentConstraint(ctl_name, joint)
create_parent_constraint()


#### CREATE BIND SKIN ####
def create_bind_skin():
    Joint_child = cmds.ls('*_JNT')
    # Chercher les noms d'un joint et du mesh correspondant puis créer le skinCluster 
    for joint in Joint_child: 
        # Prendre le nom de base en retirant le suffixe JNT 
        base_name_msh = joint.replace('_JNT', "") 
        mesh_name = base_name_msh + '_MSH' 
        # Si le mesh existe, créer le skinCluster 
        if cmds.objExists(mesh_name): 
            cmds.skinCluster(joint, mesh_name, toSelectedBones=True)
create_bind_skin()
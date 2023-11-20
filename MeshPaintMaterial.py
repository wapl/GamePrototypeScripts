import unreal

AssetTools=unreal.AssetToolsHelpers.get_asset_tools()
MaterialEditLibrary=unreal.MaterialEditingLibrary
EditorAssetLibrary=unreal.EditorAssetLibrary
#connect param nodes to lerps
def connectParamtToLerpnodes(paramNode,chanel,lerps,oneMinusNode):
    print(paramNode)
    for i in range(5):
        if i != 4:
            MaterialEditLibrary.connect_material_expressions(paramNode[i],chanel, lerps[i], 'B')
        else:
            MaterialEditLibrary.connect_material_expressions(paramNode[4], chanel, lerps[4], "A")
            MaterialEditLibrary.connect_material_expressions(paramNode[4], chanel, lerps[0], "A")
    MaterialEditLibrary.connect_material_expressions(oneMinusNode,'', lerps[0], "Alpha")
def connectVertexToLerpNodes(VertexNode,lerps,OneMinusNode):
    MaterialEditLibrary.connect_material_expressions(VertexNode, "A", OneMinusNode,'')
    Channels = ['R', 'G', 'B', 'A']
    enum_Channels = enumerate(Channels)
    for i in range(4):
        channel = next(enum_Channels)
        MaterialEditLibrary.connect_material_expressions(VertexNode, channel[1], lerps[i + 1],'Alpha')
def makeLerpConnections(lerps,mp):
    for i in range(5):
        if i != 4:
            MaterialEditLibrary.connect_material_expressions(lerps[i], '', lerps[i + 1], 'A')
        else:
            MaterialEditLibrary.connect_material_property(lerps[4], '',mp)

#Create the material
MeshPaintMaterial=AssetTools.create_asset("m_MeshPaint","/Game/materials",unreal.Material,unreal.MaterialFactoryNew())

#add Texture params for each surface
base_colors=[]
normals=[]
orm=[]

#create vertex color nodes
NodePositionX=-500
NodePositionY=-300

VertexColorNode_color=MaterialEditLibrary.create_material_expression(MeshPaintMaterial,unreal.MaterialExpressionVertexColor.static_class(),NodePositionX,NodePositionY*100)
VertexColorNode_color.set_editor_property("desc","Base_Color")

VertexColorNode_Normal=MaterialEditLibrary.create_material_expression(MeshPaintMaterial,unreal.MaterialExpressionVertexColor.static_class(),NodePositionX,NodePositionY*75)
VertexColorNode_Normal.set_editor_property("desc","Normal")


VertexColorNode_r=MaterialEditLibrary.create_material_expression(MeshPaintMaterial,unreal.MaterialExpressionVertexColor.static_class(),NodePositionX,NodePositionY*25)
VertexColorNode_r.set_editor_property("desc","Occlusion")

VertexColorNode_g=MaterialEditLibrary.create_material_expression(MeshPaintMaterial,unreal.MaterialExpressionVertexColor.static_class(),NodePositionX,NodePositionY*15)
VertexColorNode_g.set_editor_property("desc","Roughness")

VertexColorNode_b=MaterialEditLibrary.create_material_expression(MeshPaintMaterial,unreal.MaterialExpressionVertexColor.static_class(),NodePositionX,NodePositionY*10)
VertexColorNode_b.set_editor_property("desc","Mettalic")

#create one_minus node
OneMinusColor=MaterialEditLibrary.create_material_expression(MeshPaintMaterial,unreal.MaterialExpressionOneMinus.static_class(),NodePositionX*2,NodePositionY*80)
OneMinusNormal=MaterialEditLibrary.create_material_expression(MeshPaintMaterial,unreal.MaterialExpressionOneMinus.static_class(),NodePositionX*2,NodePositionY*60)
OneMinus_R=MaterialEditLibrary.create_material_expression(MeshPaintMaterial,unreal.MaterialExpressionOneMinus.static_class(),NodePositionX*2,NodePositionY*40)
OneMinus_G=MaterialEditLibrary.create_material_expression(MeshPaintMaterial,unreal.MaterialExpressionOneMinus.static_class(),NodePositionX*2,NodePositionY*20)
OneMinus_B=MaterialEditLibrary.create_material_expression(MeshPaintMaterial,unreal.MaterialExpressionOneMinus.static_class(),NodePositionX*2,NodePositionY*10)


#create material parameters
for i in range(5):
    BaseColorParam=MaterialEditLibrary.create_material_expression(MeshPaintMaterial,unreal.MaterialExpressionTextureSampleParameter2D.static_class(),NodePositionX,NodePositionY+i*150)
    NormalParam=MaterialEditLibrary.create_material_expression(MeshPaintMaterial,unreal.MaterialExpressionTextureSampleParameter2D.static_class(),NodePositionX,NodePositionY+i*150)
    ORMParam=MaterialEditLibrary.create_material_expression(MeshPaintMaterial,unreal.MaterialExpressionTextureSampleParameter2D.static_class(),NodePositionX,NodePositionY+i*150)

    #set editor property
    BaseColorParam.set_editor_property("ParameterName",unreal.Name("BaseColor_{}".format(i)))
    BaseColorParam.set_editor_property("sampler_source",unreal.SamplerSourceMode.SSM_WRAP_WORLD_GROUP_SETTINGS)

    NormalParam.set_editor_property("ParameterName", unreal.Name("Normal_{}".format(i)))
    NormalParam.set_editor_property("sampler_source", unreal.SamplerSourceMode.SSM_WRAP_WORLD_GROUP_SETTINGS)
    NormalParam.set_editor_property("sampler_type", unreal.MaterialSamplerType.SAMPLERTYPE_NORMAL)

    ORMParam.set_editor_property("ParameterName", unreal.Name("Normal_{}".format(i)))
    ORMParam.set_editor_property("sampler_source", unreal.SamplerSourceMode.SSM_WRAP_WORLD_GROUP_SETTINGS)
    ORMParam.set_editor_property("sampler_type", unreal.MaterialSamplerType.SAMPLERTYPE_LINEAR_COLOR)

    base_colors.append(BaseColorParam)
    normals.append(NormalParam)
    orm.append(ORMParam)
base_color_lerps=[]
normal_lerps=[]
orm_r_lerps=[]
orm_g_lerps=[]
orm_b_lerps=[]
for i in range(5):
    base_color_lerp=MaterialEditLibrary.create_material_expression(MeshPaintMaterial,unreal.MaterialExpressionLinearInterpolate.static_class(),NodePositionX,NodePositionY+i*200)
    normal_lerp=MaterialEditLibrary.create_material_expression(MeshPaintMaterial,unreal.MaterialExpressionLinearInterpolate.static_class(),NodePositionX,NodePositionY+i*200)
    orm_r_lerp=MaterialEditLibrary.create_material_expression(MeshPaintMaterial,unreal.MaterialExpressionLinearInterpolate.static_class(),NodePositionX,NodePositionY+i*200)
    orm_g_lerp=MaterialEditLibrary.create_material_expression(MeshPaintMaterial,unreal.MaterialExpressionLinearInterpolate.static_class(),NodePositionX,NodePositionY+i*200)
    orm_b_lerp=MaterialEditLibrary.create_material_expression(MeshPaintMaterial,unreal.MaterialExpressionLinearInterpolate.static_class(),NodePositionX,NodePositionY+i*200)

    base_color_lerps.append(base_color_lerp)
    normal_lerps.append(normal_lerp)
    orm_r_lerps.append(orm_r_lerp)
    orm_g_lerps.append(orm_g_lerp)
    orm_b_lerps.append(orm_b_lerp)

#connect base color param
connectParamtToLerpnodes(base_colors,'',base_color_lerps,OneMinusColor)
#Connect Vertex Color node to Base Color lerps
connectVertexToLerpNodes(VertexColorNode_color,base_color_lerps,OneMinusColor)
#make lerp connections
makeLerpConnections(base_color_lerps,unreal.MaterialProperty.MP_BASE_COLOR)

#Connect normals to normal lerps
connectParamtToLerpnodes(normals,'',normal_lerps,OneMinusNormal)
#connect vertex normals to lerp normals
connectVertexToLerpNodes(VertexColorNode_Normal,normal_lerps,OneMinusNormal)
#make lerp connections
makeLerpConnections(normal_lerps,unreal.MaterialProperty.MP_NORMAL)

#connect occlusion param
connectParamtToLerpnodes(orm,'R',orm_r_lerps,OneMinus_R)
connectVertexToLerpNodes(VertexColorNode_r,orm_r_lerps,OneMinus_R)
makeLerpConnections(orm_r_lerps,unreal.MaterialProperty.MP_AMBIENT_OCCLUSION)


connectParamtToLerpnodes(orm,'G',orm_g_lerps,OneMinus_G)
connectVertexToLerpNodes(VertexColorNode_g,orm_g_lerps,OneMinus_G)
makeLerpConnections(orm_g_lerps,unreal.MaterialProperty.MP_ROUGHNESS)

connectParamtToLerpnodes(orm,'B',orm_b_lerps,OneMinus_B)
connectVertexToLerpNodes(VertexColorNode_b,orm_b_lerps,OneMinus_B)
makeLerpConnections(orm_b_lerps,unreal.MaterialProperty.MP_METALLIC)


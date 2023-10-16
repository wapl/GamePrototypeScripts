import unreal

assetTools=unreal.AssetToolsHelpers.get_asset_tools()
MaterialEditLibrary=unreal.MaterialEditingLibrary
EditorAssetLibrary=unreal.EditorAssetLibrary


masterMaterial=assetTools.create_asset("M_InteracbleORD" ,"/Game/materials",unreal.Material,unreal.MaterialFactoryNew())


# create base color


baseColorTexture=MaterialEditLibrary.create_material_expression(masterMaterial,unreal.MaterialExpressionMaterialFunctionCall,-384,-207)
baseColorTexture.set_editor_property("MaterialFunction",unreal.load_asset('/Game/materials/MF_BaseColor'))
MaterialEditLibrary.connect_material_property(baseColorTexture,"",unreal.MaterialProperty.MP_BASE_COLOR)


#Metalic
metalParam=MaterialEditLibrary.create_material_expression(masterMaterial,unreal.MaterialExpressionScalarParameter,-125,70)

metalParam.set_editor_property("ParameterName","Metalic")
metalParam.set_editor_property("DefaultValue",0.0)
MaterialEditLibrary.connect_material_property(metalParam,"",unreal.MaterialProperty.MP_METALLIC)

#normal
normalTexture=MaterialEditLibrary.create_material_expression(masterMaterial,unreal.MaterialExpressionMaterialFunctionCall,-125,-50)
normalTexture.set_editor_property("MaterialFunction",unreal.load_asset('/Game/materials/MF_Normals'))
MaterialEditLibrary.connect_material_property(normalTexture,"",unreal.MaterialProperty.MP_NORMAL)

#specular
lerpNode=MaterialEditLibrary.create_material_expression(masterMaterial,unreal.MaterialExpressionLinearInterpolate,-125,-25)
constantColor=MaterialEditLibrary.create_material_expression(masterMaterial,unreal.MaterialExpressionConstant3Vector,-150,-25)
mf_Pulse=MaterialEditLibrary.create_material_expression(masterMaterial,unreal.MaterialExpressionMaterialFunctionCall,-170,-50)
mf_Pulse.set_editor_property("MaterialFunction",unreal.load_asset('/Game/materials/MF_Pulse'))
pulsing=MaterialEditLibrary.create_material_expression(masterMaterial,unreal.MaterialExpressionScalarParameter,-190,70)
pulsing.set_editor_property("ParameterName","Pulsing")
pulsing.set_editor_property("DefaultValue",0.0)

MaterialEditLibrary.connect_material_property(lerpNode,"",unreal.MaterialProperty.MP_EMISSIVE_COLOR)
MaterialEditLibrary.connect_material_expressions(constantColor,"",lerpNode,"A")
MaterialEditLibrary.connect_material_expressions(mf_Pulse,"",lerpNode,"B")
MaterialEditLibrary.connect_material_expressions(pulsing,"",lerpNode,"Alpha")

#ORD
ORDTextureParam=MaterialEditLibrary.create_material_expression(masterMaterial,unreal.MaterialExpressionTextureSampleParameter2D,-125,0)
ORDTextureParam.set_editor_property("ParameterName","ORD")
MaterialEditLibrary.connect_material_property(ORDTextureParam,"R",unreal.MaterialProperty.MP_AMBIENT_OCCLUSION)
MaterialEditLibrary.connect_material_property(ORDTextureParam,"G",unreal.MaterialProperty.MP_ROUGHNESS)


EditorAssetLibrary.save_asset("/Game/materials/M_InteracbleORD",True)
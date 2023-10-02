import unreal

levelTools=unreal.Level
editorLevelLibrary= unreal.EditorLevelLibrary
levelSubSys=unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)

new_level="myNewLevel"

myNewLevel=levelSubSys.new_level("/Game/levels/newLevel")



levelSubSys.save_current_level()
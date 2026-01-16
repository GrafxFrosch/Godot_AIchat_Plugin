@tool
extends EditorPlugin

var button

func _enter_tree():
	# Button in der SceneTree-Dock-Leiste hinzufügen
	button = Button.new()
	button.text = "Add AI Manager"
	button.connect("pressed", Callable(self, "_on_add_ai_manager_pressed"))

	
	add_control_to_container(CONTAINER_TOOLBAR, button)

func _exit_tree():
	# Button entfernen, wenn Plugin deaktiviert wird
	remove_control_from_container(CONTAINER_TOOLBAR, button)
	button.free()
# =================================================================
# Callback für Button
# =================================================================
func _on_add_ai_manager_pressed():
	var current_scene = get_editor_interface().get_edited_scene_root()
	if not current_scene:
		push_error("No scene open! Please open a scene first.")
		return

	# AI_Manager Node erstellen
	var ai_manager_scene = load("res://addons/aichat/AI_Manager.tscn")
	var ai_manager_instance = ai_manager_scene.instantiate()
	
	current_scene.add_child(ai_manager_instance)
	ai_manager_instance.owner = current_scene  # Damit es gespeichert wird

	# Optional: Fokus auf neuen Node
	get_editor_interface().edit_node(ai_manager_instance)
	print("AI_Manager Node added to scene")

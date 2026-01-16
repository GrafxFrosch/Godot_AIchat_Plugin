extends Node
class_name AIChat
signal response_received(response)
@export var api_key: String
@export var endpoint: String
var exe_path := ProjectSettings.globalize_path("res://addons/aichat/dist/ai_chat.exe")
var historyMem = []
func askAI(prompt: String):
	ask(prompt, historyMem, endpoint,api_key)
	
func ask(prompt: String, history: String, endpoint: String, apikey: String) -> String:
	var output = []
	OS.execute(
		exe_path,
		[
			"--prompt", prompt,
			"--history", history,
			"--endpoint", endpoint,
			"--apikey", apikey
		],
		output,
		true,
	)
	var text = output[0]
	emit_signal("response_received", text)
	historyMem.append(text)
	return text

func _ready() -> void:
	print(ask("I just started the Scene! Answer in max 5 words!", " ", endpoint,api_key))

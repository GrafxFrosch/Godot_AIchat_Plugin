extends Node
class_name AIChat

signal response_received(response)

# Der API Key kann hier oder im Inspektor gesetzt werden
@export var api_key: String 

# Pfad zur .exe (Achte darauf, dass du das Python-Skript mit PyInstaller als .exe exportiert hast)
var exe_path := ProjectSettings.globalize_path("res://addons/aichat/dist/ai_chat.exe")

# Speichert den Verlauf der Nachrichten
var history_mem: Array[String] = []

func askAI(prompt: String):
	# Wir wandeln das Array in einen einzelnen String um, damit Python es leicht lesen kann
	var history_string = " | ".join(history_mem)
	return ask(prompt, history_string, api_key)

func ask(prompt: String, history: String, apikey: String) -> String:
	var output = []
	
	# OS.execute ist blockierend. Das heißt, Godot "friert" kurz ein, bis die KI antwortet.
	# Das ist für den Anfang okay, bei langen Texten wäre ein Thread besser.
	var exit_code = OS.execute(exe_path, [
	"--prompt", prompt, 
	"--history", history, 
	"--apikey", apikey
	], output, true)

	print("Exit Code: ", exit_code)
	print("Full Output: ", output) # Schau hier genau hin!

	if exit_code == 0 and output.size() > 0:
		var text = output[0].strip_edges() # strip_edges entfernt unnötige Zeilenumbrüche
		
		# Verlauf aktualisieren (Prompt und Antwort speichern)
		history_mem.append("User: " + prompt)
		history_mem.append("AI: " + text)
		
		emit_signal("response_received", text)
		return text
	else:
		var error_msg = "Error: AI script failed with code %d" % exit_code
		printerr(error_msg)
		return error_msg

func _ready() -> void:
	# Kleiner Test beim Start
	if api_key == "":
		print("Warnung: Kein API Key gesetzt!")
	else:
		print("Anfrage an KI gesendet...")
		var response = askAI("I just started the Scene! Answer in max 5 words!")
		print("Antwort erhalten: ", response)

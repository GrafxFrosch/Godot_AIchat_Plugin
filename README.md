"# Godot_AIchat_Plugin" 

This Plugin makes it easy to have AI-Convos in your Game.

How to Install:
-Download the ZIP file
-Put it in the addons Folder of the Project you want to use it in and unpack it.
-Go to Projectsettings -> Plugins and click the checkbox to enable it

How to Use it:
-if the Plugin is enabled there schould be a button on the top right of the editor
-click it and it will generate a Node2D 
  -The Node has a exported variable:
  -put your API-Key in                    Tutorial how to get it: https://www.youtube.com/watch?v=OB99E7Y1cMA
-TEST: It wil generate a test message from openAI everytime you start your Scene in Godot
-Now you can use it in your Project call the AImanager node with the funktion askAI("Your Prompt!") for example

extends Node
@export var ai_manager: Node2D  #hast to be set in the editor

func _ready() -> void:
  print(ai_manager.askAI("What's up?"))

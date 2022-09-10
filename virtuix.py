
# Wolframalpha conveniently provides an API, which is found at https://developer.wolframalpha.com/portal/myapps/
# This documentation was also very usefel for finding modules: https://wolframalpha.readthedocs.io/en/latest/?badge=latest#wolframalpha.Document




"""
This is the basic way to get a question from the user, which can then be inputted into wolfram alpha in order to return an answer

import wolframalpha            
client = wolframalpha.Client("HW58H7-YWAU8WL4XE")

user = input("What's your question?")
result = client.query(user)
print(next(result.results).text)    # .results is the function that allows us to query simply for the 'result' tile, which is the primary answer, and only answer, that we are looking for

"""




import wolframalpha
client = wolframalpha.Client("HW58H7-YWAU8WL4XE")  # Wolframalpha uses a client key to access it, which is done by using .Client

import wikipedia  # Wikipedia will also be used to provide a description about an answer


# Using the input() function is quite a crude solution, so instead I will build a GUI
# The goal is to have the user input their question in a window, not in a terminal console
# A simple GUI I found to use is PySimpleGUI, documentation here: https://pypi.org/project/PySimpleGUI/
# PySimpleGui already does some of the work for me, in terms of formatting the GUI. What is left is to take the question, input it into Wolfram, and output the answer.

import PySimpleGUI as sg

import pyttsx3  # This library provides text-to-speech funcionality, which will "read" the answer out loud to the user



# Setting up the GUI:

sg.theme("DarkBlue9")  # GUI theme


layout = [  [sg.Text("What is your question?")],  # This GUI will have text that prompts the user for a question,
            [sg.Text("Enter question:"), sg.InputText()],  # A box to input the question,
            [sg.Button("Ok"), sg.Button("Cancel")]  ]  # And a button to submit the question

window = sg.Window("Virtuix", layout)  # The window function then allows the layout above to be added to a window





while True:
    event, values = window.read()  # .read() will read the input from the user (from the window)
                                   # Values will store the actual input, and event will end the program if the user presses "Cancel", or does not submit a question
    if event in (None, "Cancel"):
        break
    try:        
        question = client.query(values[0])  # The user's question is stored in question
        wolfram_res = next(question.results).text  # Wolfram_res will then store wolfram's answer, which is acquired by the .results() function
        wiki_res = wikipedia.summary(values[0], sentences=3)  # Wikipedia is then used to provide the first three sentences on the wikipedia page about the answer
            

        answer_popup = sg.PopupNonBlocking("Answer:  " + wolfram_res, "Description:  " + wiki_res)  # After the user submits a question, a pop up will state wolfram alpha's answer, and wikipedia's summary



# Setting up the text-to-speech. The documentation can be found here: https://pypi.org/project/pyttsx3/

        engine = pyttsx3.init()  # Object creation
        voices = engine.getProperty('voices')  # Get details about voices
        engine.setProperty('voice', voices[1].id)  # Change voice, voices[1] sets voice to female
        engine.setProperty('rate', 155)  # Change the speaking rate

# Once the text-to-speech is set up, it can now "say" the answer to the user

        if wolfram_res != "(data not available)":  # If there is an answer:
            engine.say(wolfram_res)  # Say the answer
        
        engine.say(wikipedia.summary(values[0], sentences=1))  # Then, say the the first sentence of the wikipedia summary only

        engine.runAndWait()



    except wikipedia.exceptions.PageError:  # If wikipedia can not return an answer, simply only output wolfram alpha's answer
        print("Page Error occured")  
        sg.PopupNonBlocking(wolfram_res)  # Output wolfram alpha's answer in the popup

        # Read the answer
        engine = pyttsx3.init()  
        voices = engine.getProperty('voices')   
        engine.setProperty('voice', voices[1].id)
        engine.say(wolfram_res)
        engine.runAndWait()
    
    except wikipedia.exceptions.DisambiguationError:  # If the question is too general for wikipedia, do the same as above
        print("Please specify your question")
        sg.PopupNonBlocking(wolfram_res)
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')   
        engine.setProperty('voice', voices[1].id)
        engine.say(wolfram_res)
        engine.runAndWait()


    except:  # If both can not return an answer
        sg.Popup("Invalid Question, please try again.")


window.Close()  # Once the program is done, close the window













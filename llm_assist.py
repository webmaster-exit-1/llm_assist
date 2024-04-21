import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from gtts import gTTS
import os
import subprocess
from pysearch import Search
from configparser import ConfigParser
import json
import speech_recognition as sr
import pyaudio
import nmap

# Load the configuration file
config = ConfigParser()
CONFIG_NAME = 'testbot_auth.ini'

def create_config():
    # Ask the user for the search engine
    search_engine = input("Enter your preferred search engine (e.g., Google, Bing, DuckDuckGo): ")
    # Create a new config file with the provided search engine
    config['SEARCH'] = {
        'engine': search_engine
    }
    # Save the config file
    with open(CONFIG_NAME, 'w') as f:
        config.write(f)

def check_for_config():
    # Check if the config file exists
    if os.path.exists(CONFIG_NAME):
        # Load the existing config file
        config.read(CONFIG_NAME)
        return
    # If the config file doesn't exist, create a new one
    create_config()

# Check for the config file and load it if it exists
check_for_config()

# Ask the user for the full path to the GPT model they want to use
model_path = input("Enter the full path to the GPT model you want to use: ")

# Load the GPT model and tokenizer
model = AutoModelForCausalLM.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)

# Define the function to perform speech recognition
def recognize_speech():
    # Create an instance of PyAudio
    audio = pyaudio.PyAudio()
    # Open a stream for recording
    with sr.Microphone() as source:
        print("Listening...")
        audio_data = r.record(source, duration=5)  # Record audio for 5 seconds
    # Perform speech recognition
    try:
        text = r.recognize_google(audio_data)
        print("Recognized text:", text)
        return text
    except sr.UnknownValueError:
        print("Speech recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service:", str(e))

# Define the function to interact with the GPT model
def ask_gpt(prompt):
    input_ids = tokenizer.encode(prompt, return_tensors="pt")
    outputs = model.generate(input_ids=input_ids, max_new_tokens=2500, temperature=0.7)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

# Define the function to perform search
def perform_search(search_query):
    search_engine = config['SEARCH']['engine']
    search = Search(using=search_engine)
    results = search.search(search_query)
    return results

# Define the function to generate speech from text using gTTS
def generate_speech(text):
    tts = gTTS(text=text, lang="en")
    tts.save("./output.mp3")
    subprocess.run(["mpg123", "./output.mp3"])

# Define the function to perform Nmap scan
def perform_nmap_scan(target):
    nm = nmap.PortScanner()
    results = nm.scan(target, '1-1024')
    return results

# Define the chatbot loop
def chatbot():
    print("Hi user! (Type 'quit' to exit)")
    while True:
        try:
            user_input = recognize_speech()
            if user_input.lower() == "quit":
                break
            if user_input.startswith("!search"):
                search_query = user_input[len("!search"):].strip()
                if search_query:
                    results = perform_search(search_query)
                    # Display search results
                    if results:
                        print("Search Results:")
                        for result in results:
                            print(f"Title: {result['title']}")
                            print(f"URL: {result['url']}")
                            print(f"Description: {result['description']}")
                            print()
                    else:
                        print("No results found.")
            elif user_input.startswith("!nmap"):
                target = user_input[len("!nmap"):].strip()
                if target:
                    results = perform_nmap_scan(target)
                    # Display Nmap scan results
                    if results:
                        print("Nmap Scan Results:")
                        for host, ports in results.items():
                            print(f"Host: {host}")
                            for port, data in ports.items():
                                print(f"Port: {port}")
                                print(f"Service: {data['name']}")
                                print()
                    else:
                        print("No results found.")
            else:
                prompt = f"user: {user_input}"
                response = ask_gpt(prompt)
                generate_speech(response)
                print(f"ARIA: {response}")
        except Exception as e:
            print(f"An error
        except Exception as e:
            print(f"An error occurred: {str(e)}")

        input("Press Enter to respond...")

# Execute the chatbot
if __name__ == "__main__":
    chatbot()

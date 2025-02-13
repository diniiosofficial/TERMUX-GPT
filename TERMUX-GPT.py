import requests
import time
import os

RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[32m"
CYAN = "\033[36m"
MAGENTA = "\033[35m"
YELLOW = "\033[33m"
BLUE = "\033[34m"

VERSION = "1.0"
AUTHOR = "@DINI_IOS"
LICENSE = "MIT License"
COPYRIGHT_HOLDER = "DINI_IOS" 

def save_conversation(question, answer):
    with open("chat_history.txt", "a", encoding="utf-8") as file:
        file.write(f"You: {question}\n")
        file.write(f"AI: {answer}\n\n")

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def handle_rate_limits():
    time.sleep(1) 

def show_help():
    print("\nCommands:")
    print("  - Type 'exit' or 'quit' to end the chat.")
    print("  - Type 'clear' to clear the screen.")
    print("  - Type 'help' to show this menu.")
    print("  - Type 'license' to show the license information.")
    print("  - Type 'version' to show the script version.")
    print("  - Type 'credits' to show the author information.")

def show_license():
    print(f"\nLicense: {LICENSE}")
    print(f"Copyright (c) {COPYRIGHT_HOLDER}")
    print("Permission is hereby granted, free of charge, to any person obtaining a copy")
    print("of this software and associated documentation files (the 'Software'), to deal")
    print("in the Software without restriction, including without limitation the rights")
    print("to use, copy, modify, merge, publish, distribute, sublicense, and/or sell")
    print("copies of the Software, and to permit persons to whom the Software is")
    print("furnished to do so, subject to the following conditions:")
    print("\nThe above copyright notice and this permission notice shall be included in all")
    print("copies or substantial portions of the Software.")
    print("\nTHE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR")
    print("IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,")
    print("FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE")
    print("AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER")
    print("LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,")
    print("OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE")
    print("SOFTWARE.")

def show_version():
    print(f"\nTermux ChatGPT Version: {VERSION}")
    print(f"Created by: {AUTHOR}")

def show_credits():
    print(f"\nCreated by: {AUTHOR}")
    print("Special thanks to source community for their contributions.")

def ask_chatgpt(question):
    formatted_question = question.replace(" ", "%20")
    api_url = f"https://deepseek.privates-bots.workers.dev/?question={formatted_question}"
    
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            message = data.get("message", "")
            if "<think>" in message:
                while "<think>" in message:
                    start = message.find("<think>")
                    end = message.find("</think>") + len("</think>")
                    message = message[:start] + message[end:]
            return message.strip()
        else:
            return f"Error: Unable to fetch response. Status code: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Network error: {e}"
    except ValueError as e:
        return f"Invalid API response: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

def main():
    clear_screen()
    terminal_width = os.get_terminal_size().columns

    def center_text(text):
        return text.center(terminal_width)

    print(center_text(f"{GREEN}╔════════════════════════════════════════╗{RESET}"))
    print(center_text(f"{BOLD}{CYAN}            ║    🚀 Welcome to {MAGENTA}Termux ChatGPT!{CYAN}       ║{RESET}"))
    print(center_text(f"{BOLD}{CYAN}             ║            Version: {YELLOW}{VERSION}{CYAN}                ║{RESET}"))
    print(center_text(f"{BOLD}{CYAN}             ║        Created by: {BLUE}{AUTHOR}{CYAN}           ║{RESET}"))
    print(center_text(f"{GREEN}╚════════════════════════════════════════╝{RESET}\n"))

    print(center_text(f"{MAGENTA}💬 Your AI-powered conversational assistant, right in your terminal!{RESET}\n"))
    print(center_text(f"{YELLOW}          💡 Type '{BOLD}help{RESET}{YELLOW}' to see available commands.{RESET}\n"))
    
    while True:
        question = input("\nYou: ")
        
        if question.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        elif question.lower() == "clear":
            clear_screen()
            continue
        elif question.lower() == "help":
            show_help()
            continue
        elif question.lower() == "license":
            show_license()
            continue
        elif question.lower() == "version":
            show_version()
            continue
        elif question.lower() == "credits":
            show_credits()
            continue
        
        handle_rate_limits() 
        response = ask_chatgpt(question)
        print(response)
        save_conversation(question, response) 

if __name__ == "__main__":
    main()
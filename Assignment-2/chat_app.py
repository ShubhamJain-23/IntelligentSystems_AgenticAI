import os
import json
from datetime import datetime
from openai import OpenAI

def main():
    # Initialize the OpenAI-styled client pointing to the local server
    # base_url and api_key as per 'LMStudio-bionic' setup
    client = OpenAI(
        base_url="http://localhost:1234/v1",
        api_key="dummy_api_key" # API key is usually not required for local servers
    )
    
    # Mode Name
    MODEL_NAME = "qwen/qwen3-4b"

    # Seed the first message
    seed_message = input("Enter the seed message to start the conversation: ")

    # Ask the user for the number of rounds
    try:
        max_iterations_input = input("Enter the number of rounds required (default 5): ")
        MAX_ITERATIONS = int(max_iterations_input) if max_iterations_input.strip() else 5
    except ValueError:
        print("Invalid input for rounds. Defaulting to 5.")
        MAX_ITERATIONS = 5

    # System prompts to give the bots distinct personalities.
    # To reduce the size of the responses, we explicitly instruct the models to be very concise.
    bot1_system_prompt = (
        "You are Agent 1, a curious and imaginative philosopher who asks deep questions. "
        "Keep your responses extremely concise, strictly under 3 sentences. You also have to reply to the questions asked by Agent 2.You may also ask a follow-up question."
    )
    bot2_system_prompt = (
        "You are Agent 2, a highly pragmatic scientist who always looks for empirical answers and logical structure. "
        "Keep your responses extremely concise, strictly under 3 sentences. Also, you may leave an open-ended question for Agent1 to respond."
    )

    # Initialize conversation histories
    bot1_history = [{"role": "system", "content": bot1_system_prompt}]
    bot2_history = [{"role": "system", "content": bot2_system_prompt}]

    # We will maintain a separate log of the conversation to save it later
    chat_log = []

    print(f"\nAgent 1 (Seed): {seed_message}\n")
    print("-" * 50)
    
    # Add seed message to histories
    bot1_history.append({"role": "assistant", "content": seed_message})
    bot2_history.append({"role": "user", "content": seed_message})
    chat_log.append({"speaker": "Agent 1", "message": seed_message})

    for i in range(MAX_ITERATIONS):
        # Bot 2 (Agent 2) responds to Bot 1 (Agent 1)
        try:
            response_bot2 = client.chat.completions.create(
                model=MODEL_NAME,
                messages=bot2_history,
                temperature=0.7,
                max_tokens=1024
            )
            bot2_reply = response_bot2.choices[0].message.content
        except Exception as e:
            bot2_reply = f"[Error communicating with bionic model: {e}]"
            
        print(f"Agent 2: {bot2_reply}\n")
        print("-" * 50)
        
        # Update histories
        bot2_history.append({"role": "assistant", "content": bot2_reply})
        bot1_history.append({"role": "user", "content": bot2_reply})
        chat_log.append({"speaker": "Agent 2", "message": bot2_reply})
        
        # If there was an error, we break the loop to avoid sending error messages back and forth
        if "[Error" in bot2_reply:
            break

        # Bot 1 (Agent 1) responds to Bot 2 (Agent 2)
        try:
            response_bot1 = client.chat.completions.create(
                model=MODEL_NAME,
                messages=bot1_history,
                temperature=0.8,
                max_tokens=1024
            )
            bot1_reply = response_bot1.choices[0].message.content
        except Exception as e:
            bot1_reply = f"[Error communicating with bionic model: {e}]"
            
        print(f"Agent 1: {bot1_reply}\n")
        print("-" * 50)
        
        # Update histories
        bot1_history.append({"role": "assistant", "content": bot1_reply})
        bot2_history.append({"role": "user", "content": bot1_reply})
        chat_log.append({"speaker": "Agent 1", "message": bot1_reply})
        
        if "[Error" in bot1_reply:
            break

    # Save the chat version to a JSON file in the chat_history folder
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    history_dir = "chat_history"
    if not os.path.exists(history_dir):
        os.makedirs(history_dir)
        
    filename = os.path.join(history_dir, f"chat_log_{timestamp}.json")
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(chat_log, f, indent=4)
        
    print(f"\nConversation saved to {filename}")

if __name__ == "__main__":
    main()

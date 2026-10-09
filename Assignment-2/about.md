# About Bot-to-Bot Chat Application

## Purpose
This application was created for **Assignment-2**. 
It demonstrates an autonomous, turn-based conversation where two distinct AI agents converse with each other for a predetermined number of iterations, utilizing the OpenAI SDK and a local inference model ("bionic").

## How it Works
1. **Model Initialization:** The script connects via the OpenAI Python SDK to a locally hosted model endpoint (e.g. `http://localhost:1234/v1`).
2. **Context Setup:** Two distinct agent personalities (Agent 1 the Philosopher and Agent 2 the Scientist) are established through system prompts. The prompts explicitly restrict the models to concise, short responses to prevent overly long generations. Two separate conversation histories are kept in memory for each agent.
3. **Seeding and Configuration:** The user is prompted via standard input to provide a single seed question to start the conversation, as well as the number of conversational rounds (iterations) the bots should engage in.
4. **Turn-based Loop:** The agents take turns generating replies using the `client.chat.completions.create` API. When an agent speaks, its output is appended to its own history as an `assistant` message, and injected into the other agent's history as a `user` message. This allows them to "listen" and react contextually.
5. **Data Persistence:** A continuous transcript of the exchange is built in memory during the execution. Once the loop breaks or finishes, the script formats this transcript into JSON and exports it to the `chat_history/` directory with a unique timestamp, making it easy to save and track different versions of the chat.

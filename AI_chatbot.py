def chatbot_response(user_input):
    # Convert input to lowercase to handle case-insensitive matches
    user_input = user_input.lower()

    # Predefined responses for specific inputs
    if "hello" in user_input:
        return "Hello! How can I help you today?"
    elif "how are you" in user_input:
        return "I'm just a bot, but I'm doing great! How about you?"
    elif "bye" in user_input:
        return "Goodbye! Have a great day!"
    elif "help" in user_input:
        return "Sure, I can assist you. What do you need help with?"
    else:
        return "Sorry, I didn't understand that. Can you please rephrase?"

# Chat loop
if __name__ == "__main__":
    print("Chatbot: Hello! Type 'bye' to exit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "bye":
            print("Chatbot: Goodbye!")
            break
        response = chatbot_response(user_input)
        print("Chatbot:", response)

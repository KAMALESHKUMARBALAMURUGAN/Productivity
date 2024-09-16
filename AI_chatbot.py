import tkinter as tk

# Chatbot logic
def chatbot_response(user_input):
    user_input = user_input.lower()

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

# Function to handle the send button
def send_message():
    user_input = entry_box.get()  # Get the input from the entry box
    chat_log.config(state=tk.NORMAL)  # Allow editing the text widget
    chat_log.insert(tk.END, "You: " + user_input + "\n")  # Display user input
    entry_box.delete(0, tk.END)  # Clear the input box

    response = chatbot_response(user_input)  # Get chatbot response
    chat_log.insert(tk.END, "Chatbot: " + response + "\n\n")  # Display chatbot response
    chat_log.config(state=tk.DISABLED)  # Disable editing again
    chat_log.yview(tk.END)  # Scroll to the bottom of the chat log

# Set up the main window
root = tk.Tk()
root.title("KAMAL")

# Create a chat log to display conversation
chat_log = tk.Text(root, bd=1, bg="white", height=15, width=50)
chat_log.config(state=tk.DISABLED)  # Disable editing

# Create a scrollbar
scrollbar = tk.Scrollbar(root, command=chat_log.yview)
chat_log['yscrollcommand'] = scrollbar.set

# Entry box for user input
entry_box = tk.Entry(root, bd=1, bg="white", width=40)

# Send button to submit input
send_button = tk.Button(root, text="Send", width=10, command=send_message)

# Arrange elements on the window using grid layout
chat_log.grid(row=0, column=0, columnspan=2)
scrollbar.grid(row=0, column=2, sticky='ns')
entry_box.grid(row=1, column=0)
send_button.grid(row=1, column=1)

# Start the Tkinter event loop
root.mainloop()

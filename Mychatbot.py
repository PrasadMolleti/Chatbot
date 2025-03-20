import streamlit as st
import csv
import json
from langchain_groq import ChatGroq

# Initialize Groq AI Model (Use a valid API key)
lln = ChatGroq(model="llama3-70b-8192", api_key="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")

# CSV File Path to store chat history
csv_filename = "chat_history.csv"

# Initialize Streamlit app
st.title("🤖 AI Chatbot using Groq (Llama3)")
st.write("Type your message below and get responses in real time!")

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Function to chat with AI and update history
def chat_with_ai(user_prompt):
    """Sends prompt to AI, saves response, and updates UI."""
    if user_prompt.lower() == "exit":
        st.write("Chat session ended. History saved to CSV.")
        return

    try:
        # Get AI response
        response = lln.invoke(user_prompt)
        response_text = response.content if hasattr(response, "content") else str(response)

        # Save to chat history
        st.session_state.chat_history.append({"prompt": user_prompt, "response": response_text})

        # Save chat to CSV
        with open(csv_filename, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([user_prompt, response_text])

        # Return JSON response
        return json.dumps({"prompt": user_prompt, "response": response_text})

    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

# Chat input field
user_input = st.text_input("Enter your prompt:", "")

# If user submits a prompt
if st.button("Send"):
    if user_input:
        response_json = chat_with_ai(user_input)
        st.json(json.loads(response_json))  # Display JSON response

# Display chat history
st.subheader("Chat History")
for chat in st.session_state.chat_history:
    st.write(f"**You:** {chat['prompt']}")
    st.write(f"**AI:** {chat['response']}")
    st.write("---")

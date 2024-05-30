import streamlit as st
import google.generativeai as genai

generation_config = {
  "temperature": 0.5,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}
safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
]

# genai.configure(api_key=os.environ["GEMINI_API_KEY"])
genai.configure(api_key=st.secrets["google_secret"])

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  safety_settings=safety_settings,
  generation_config=generation_config,
)

# Define your lateral thinking puzzle (text and answer)
puzzle_text = "Laura is restrained all night long, with her hands pinned to her sides, and cries out occasionally, while someone watches her on a video camera. No one is alarmed, and Laura is happy in the morning. Why?"
puzzle_answer = "Laura is a baby who is swaddled, and her mother is watching her via a baby monitor. Though she cries out a few times during the night, she goes back to sleep and is well rested in the morning."  # Modify this with your actual answer

if 'chat_session' not in st.session_state:
      st.session_state['chat_session'] = model.start_chat(
          history=[
                {
                    "role": "user",
                    "parts": [
                          { "text": "We are playing a lateral thinking puzzle game where you are the host. You are given a puzzle question and a single correct asnwer. The player can ask you questions and you can only answer in yes, no or irrelevant based on whether they are correct, wrong or irrelevant to the answer. Note that if the question cannot be answered in yes or no, you are to reply in irrelevant. You cannot give any other answer with the exception of a congratulations message when the user is able to guess the correct answer. Note that the user does not need to get the asnwer word for word but the right idea. That being said, the question is the following: " + puzzle_text + ". And the asnwer is :" + puzzle_answer + ". Note that the congratulations message should be exactly the following text in between the quotations without the quotes: 'Congratulations!, you have guessed correctly'" }
                    ] 
                }
          ]
      )

def chat(user_input):
    chat = st.session_state['chat_session']
    response = chat.send_message(user_input)
    st.session_state['chat_session'] = chat
    return response.text


# Streamlit app layout
st.title("Lateral Puzzle Chatbot")
st.subheader(puzzle_text)  # Display the puzzle text
st.write("You have to deduce what is happening. You can either ask a question with a Yes or No answer or Take a guess as to what is happening.")
st.write("The model will reply in Yes, No or irrelevant. The game will end when you guess correctly. Let's see if you can get it in 10 questions.")

num_questions = st.session_state.get('num_questions', 0)
user_input = st.text_input("Question:", key="user_input", placeholder="Please enter your question or solution and press the ASK button below")  # Assign a unique key
ask_button = st.button("Ask", disabled=num_questions >= 10, type="primary")

if 'history' not in st.session_state:
  st.session_state['history'] = []
history = st.session_state['history']

if ask_button:
    bot_response = chat(user_input)
    history.append(str(user_input) + " : " + str(bot_response))
    num_questions += 1
    st.session_state['num_questions'] = num_questions

    if bot_response == "Congratulations!, you have guessed correctly":
        num_questions = 10
        st.session_state['num_questions'] = num_questions
    elif num_questions > 10:
        history.append("You've reached the limit of 10 questions.")
        history.append(f"The answer is: {puzzle_answer}")

st.subheader("Number of questions left: " + str(10 - num_questions))

if len(history) > 0:
    for line in history:
        st.write(line)
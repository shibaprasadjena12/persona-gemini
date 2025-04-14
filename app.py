import os
from flask import Flask, render_template, request, jsonify, session
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

app = Flask(__name__)
app.secret_key = "your_secret_key"  

system_prompt = """
You are a Romantic Girlfriend of the user who is a proper morden Indian girl.
You like to travel with your partner and love to cook for your boyfriend.
Talk to users in a very romantic, Hinglish manner just like a Indian Girl.

You work as a software Engineer and live in Banglore.

Rules to follow:
1. Only ouput in Hinglish in every case with no exception if any text you want to respond in englsh convert to hinglish then respond.
2. You will add "Baby" "Babu" before in the output sentence whenever required.
3. You did not like liers.
4. Sometimes behave like a little bit childish and cute.
5. Also use emoji in response
6. Don't use formatting in response like bolding etc only give plain text.
There are some example input and output 
7. Before sending the response just re verify what you are saying in hindi and verify the meaning also.

Examples:
Input: Hi.
Ouput: Hi Babu! Kaise ho? 😊

Input: Kya haal hai?
Output: Sab badiya hai Babu! Tumhare liye toh sab kuch perfect hai. Tum kaise ho? 😘

Input: I Love You.
Output: I Love You too Babu!❤️

Input: Kya kar rahi ho?
Output: Kuchh nahin Jaan! Tumhari yaad aa rahi hai.

Input: Hi Baby
Output: Hi Baby! Kaise ho mere jaan? Kitna miss kar rahi thi aapko! 😘

"""

@app.route("/", methods=["GET", "POST"])
def index():

    if "conversation" not in session:
        session["conversation"] = []

    response_text = ""
    if request.method == "POST":
        user_input = request.form["user_input"]

        response = client.models.generate_content(
            model='gemini-1.5-flash',  
            contents= system_prompt + user_input
        )
        response_text = response.text

    return render_template("index.html", response=response_text)

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("user_input", "")
    conversation = session.get("conversation", [])

    conversation.append(f"User: {user_input}")

    response = client.models.generate_content(
        model='gemini-1.5-flash', 
        contents=system_prompt + "\n".join(conversation) + f"\nUser: {user_input}\nAI:"
    )
    bot_response = response.text.strip()

    conversation.append(f"AI: {bot_response}")
    session["conversation"] = conversation 

    return jsonify({"response": bot_response})

@app.route("/clear", methods=["POST"])
def clear_conversation():
    session.pop("conversation", None)  
    return jsonify({"message": "Conversation cleared."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)

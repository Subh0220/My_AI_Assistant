# AI ASSISTANT

## Description
An interactive AI Assistant built with Flask, OpenAI, HTML, CSS, and JavaScript.
This project provides a simple conversational interface where users can ask questions, get AI-generated answers, and give feedback on responses.

## Features
- Ask questions and get instant AI-powered answers
- Beautiful UI with space-themed design
- Typing animation for better user experience
- Feedback system (👍 / 👎) stored locally in feedback.txt
- Easy to run on any system with Python 3

## Project Structure
- /app.py               <!--Flask backend-->
- /requirements.txt     <!--Python dependencies-->
- templates/
  - index.html           <!--Frontend HTML-->
- static/
  - style.css            <!--Styling-->
  - script.js            <!--Frontend logic-->
- /feedback.txt         <!--Stores user feedback-->
- /.env                 <!--Stores your API key (not shared in repo)-->

## Requirements
- Python 3.8+
- OpenAI API key (or GitHub token if using models through GitHub endpoint)
- Install dependencies:
  - pip install -r requirements.txt

## Environment Setup
- Create a .env file in the project root:
  - GITHUB_TOKEN or API_KEY=your_github_token_here or your_api_key_here

## Running the project:
1. Clone this repository:
- git clone https://github.com/Subh0220/My_AI_Assistant.git
- cd My_AI_Assistant
2. Install dependencies:
pip install -r requirements.txt
3. Run the Flask app:
python app.py
4. Open your browser and go to:
http://127.0.0.1:5000

## Example Usage
- Type: “Summarize climate change in 3 sentences.”
- The AI Assistant will generate a concise, creative response.
- Provide feedback with 👍 or 👎 to record in feedback.txt.

## Technologies Used
- Backend: Flask, Python, OpenAI Model, Github Token
- Frontend: HTML, CSS, JavaScript
- Styling: Custom space-themed design

---

🙏 Thank you for checking out this project!  
Contributions, feedback, and suggestions are always welcome. 🚀

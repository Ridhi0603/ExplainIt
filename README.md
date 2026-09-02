# ExplainIt 🧠

ExplainIt is an AI-powered learning tool I built to make technical concepts easier to understand.

The idea is simple: enter a concept, choose how detailed you want the explanation to be, and ExplainIt breaks it down into an explanation, a real-world analogy, an example, common mistakes, and practice questions.

I built this project while learning how to work with AI APIs and wanted to put together a complete application instead of just experimenting with an API.

## ✨ Features

- 📘 **Concept explanations** — Get structured explanations of technical topics.
- 🎯 **Difficulty levels** — Choose between Beginner, Student, and Advanced explanations.
- 🌍 **Real-world analogies** — Understand concepts through relatable examples.
- 💻 **Examples** — See the concept applied in a practical context.
- ⚠️ **Common mistakes** — Learn about mistakes students commonly make.
- 📝 **Practice questions** — Test your understanding after reading an explanation.
- ✅ **Answer checking** — Submit your answers and get them evaluated by the AI.
- 💡 **Explain differently** — Ask for the same concept to be explained in a simpler, step-by-step, analogy-based, or more technical way.
- 🔄 **Regenerate** — Generate another explanation for the same concept.
- 📚 **History** — Save explanations and revisit them later.
- 👍👎 **Feedback** — Give feedback on whether an explanation was helpful.
- 🗑️ **Delete history** — Remove explanations you no longer need.
- 🪄 **New Explanation** — Quickly start learning a new concept.

## 🛠️ Tech Stack

- **Python** — Application logic and AI integration
- **Streamlit** — Web interface
- **Google Gemini API** — AI-generated explanations and answer evaluation
- **SQLite** — Local storage for explanation history and feedback

## 🔍 How It Works

1. The user enters a technical concept.
2. A difficulty level is selected.
3. The concept and difficulty are sent to the Gemini API.
4. Gemini generates a structured response.
5. The response is displayed through the Streamlit interface.
6. The explanation is saved locally in SQLite.
7. The user can revisit previous explanations, regenerate them, or ask for a different explanation style.
8. Practice questions can be answered directly in the app and checked using the AI.

## 📂 Project Structure
-app.py — Main application logic, Gemini API integration, database operations, history, feedback, and error handling.
-streamlit_app.py — Streamlit interface and user interaction.
-.streamlit/config.toml — Streamlit theme configuration.
-.gitignore — Specifies files and folders that should not be tracked by Git.
-README.md — Project documentation.

## 💭 Why I Built It

This was my first independent project where I worked with an AI API and connected multiple parts of an application together.

I wanted to move beyond just learning Python concepts and build something where I had to deal with things like API requests, user input, databases, UI design, error handling, and keeping track of application state.

It also gave me a chance to experiment with how AI can be used as a learning assistant rather than simply as a chatbot.

## 🚧 Future Improvements

Some things I'd like to explore in the future:

👤 User accounts and personalized learning history
📊 Progress tracking
🧩 More interactive practice modes
🎨 More control over explanation formatting
☁️ Deploying the application online
📱 Making the interface more accessible across different screen sizes

## 👩‍💻 About

ExplainIt was built as a personal learning project while exploring Python, AI APIs, Streamlit, and application development.
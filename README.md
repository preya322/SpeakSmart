# Alera – AI Desktop Assistant

![Alera Banner](https://github.com/preya322/SpeakSmart/blob/main/logo.png)

---

## 🚀 Overview

**Alera** is an AI-powered voice-controlled desktop assistant designed to automate daily tasks, generate creative content, and provide seamless natural interaction.  
Through smart AI classification, Alera processes multiple voice commands simultaneously, performs real-time actions, generates documents, videos, images, and more — all hands-free!

---

## ✨ Key Features

- 🎤 **Voice Command Input** – Control your desktop and online activities with natural voice commands.
- 🧠 **AI-Based Command Categorization**:
  - **General Queries** (e.g., "What is the time?")
  - **Real-Time Queries** (e.g., "Who is Elon Musk?")
  - **Automation Queries** (e.g., "Open YouTube", "Generate an image")
- 🖥️ **Application and Website Automation** – Launch apps and browse sites effortlessly.
- 📑 **Presentation Generation** – Create structured PowerPoint presentations by simply describing the topic.
- ✍️ **Content Generation** – Generate paragraphs, essays, poems, or blog posts using Google Gemini AI.
- 🎥 **Short Story Video Generation** – Produce AI-generated videos based on user ideas.
- 🖼️ **Image Generation** – Generate creative images using Hugging Face API.
- 🗣️ **Text-to-Speech Responses** – Get immediate verbal feedback for every action.
- 🛠️ **Multi-Command Execution** – Execute multiple tasks from a single voice command input.
- 🛡️ **Hotword Detection** – Instantly wake the assistant with a hotword (e.g., "Hey Alera").

---

## 🛠️ Technology Stack

| Layer         | Technologies                            |
|---------------|-----------------------------------------|
| **Frontend**  | HTML, CSS, JavaScript, jQuery            |
| **Backend**   | Python, SQLite                          |
| **Framework** | EEL (Frontend-Backend Communication)    |
| **APIs Used** | Google Gemini (content generation), Hugging Face (image generation), Porcupine (hotword detection) |

---

## 📈 System Architecture

![System Architecture Diagram](https://github.com/preya322/SpeakSmart/blob/main/SystemArchitecture.png)

**Flow:**
1. Voice Input
2. NLP Engine (Command understanding)
3. AI Command Classifier
4. Categorization:
   - General Query
   - Real-Time Query
   - Automation Query
5. Action Execution Module
6. Text-to-Speech Response

---

## 🧩 Use Case Examples

- **Presentation Generation**  
  _"Create a 5-slide presentation on AI Trends 2025"_

- **Short Story Video Creation**  
  _"Generate a short video about a journey to Mars"_

- **Multi-command Execution**  
  _"What is the time and open YouTube"_

- **Content Generation**  
  _"Write a paragraph about the benefits of AI"_

---

## 🚀 How to Run Alera

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/alera-desktop-assistant.git
   ```
2. **Navigate to the Project Directory**:
   ```bash
   cd alera-desktop-assistant
   ```
3. **Install Dependencies:**:
   - Make sure you have Python 3.x installed.
   - Install required packages:
     ```bash
     pip install -r requirements.txt
     ```
4. **Setup API Keys**:
   - Add your Google Gemini, Hugging Face, and Porcupine API keys in the configuration file or environment variables.
5. **Run the Application**:
   ```bash
   python main.py
   ```
6. **Activate Hotword Detection**:
   - Use the default hotword (e.g., "Hey Alera") to start issuing commands.

## 🛡️ Security Considerations
- User data is handled locally using **SQLite** for enhanced privacy.
- API keys are securely stored and accessed through environment variables.

## 🎯 Future Enhancements
- 🌐 Multilingual support
- 📱 Mobile integration (Android App)
- 🏡 Smart Home device control
- 🎨 Personalized user profiles
- 🤖 Improved AI conversational memory

## 👨‍💻 Team Members
- Preya Patel
- Vedansh Rathod
- Astha Prajapati
- Nidar Prajapati

## 📢 Contact
- LinkedIn: [PREYA PATEL](https://www.linkedin.com/in/preya-patel-31a9612b7/)
- GitHub: [preya322](http://github.com/preya322)

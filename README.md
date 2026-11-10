# 🛡️ Nexus | Premium Secure Comms

A high-performance, real-time secure communication protocol built with **FastAPI** and **WebSockets**. Nexus features a fully integrated **Single Page Application (SPA)** frontend, eliminating page reloads and ensuring seamless, encrypted terminal-style communication.

## 🚀 The Architecture
Unlike standard CRUD chat applications, Nexus is designed with a state-driven WebSocket manager that handles live presence, dynamic room allocation, and instant data broadcasting without polling the database.

### 🔐 Core Security & Features
* **Real-Time WebSockets:** Bi-directional communication with zero-latency broadcasting.
* **JWT Authentication:** Secure stateless session management without relying on hardcoded credentials.
* **Screenshot & PrintScreen Ninja Guard:** Built-in keystroke detection that instantly alerts the room if a user attempts to capture the screen (`PrtScn` or `Win+Shift+S`).
* **Base64 Media Pipeline:** Images are converted to Base64 strings and transmitted directly via WebSockets, ensuring no media files are permanently stored on the server.
* **Orphan-Message Guard:** Robust backend error handling to prevent `500 Internal Server Error` crashes caused by deleted user IDs.
* **Live Presence Indicator:** Dynamic tracking of online/offline status for connected nodes.
* **Message Redaction:** Double-click payload unsend functionality across all active clients.

## 🛠️ Tech Stack
* **Backend:** Python, FastAPI, Uvicorn, SQLAlchemy, SQLite
* **Frontend:** Vanilla JavaScript, HTML5, Tailwind CSS (Custom 'Espresso Black' Aesthetic)
* **Protocol:** WebSockets (ws://) & REST APIs (http://)

## ⚙️ Local Setup Instructions
1. Clone the repository: `git clone https://github.com/sifat-dev-code`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the ASGI server: `uvicorn main:app --reload`
4. Access the UI via browser by opening the root `chat_test.html` file.

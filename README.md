# 🛡️ Nexus | Premium Secure Comms

A high-performance, real-time secure communication protocol built with **FastAPI** and **WebSockets**. Nexus features a fully integrated Single Page Application (SPA) frontend, ensuring seamless, encrypted terminal-style communication with zero page reloads.

🔗 **Live Application:** [Nexus Secure Comms](https://sifat-dev-code.github.io/nexus-secure-chat/)

## 🚀 The Architecture
Unlike standard CRUD chat applications, Nexus is powered entirely by a state-driven WebSocket manager that handles live presence, dynamic room allocation, and instant data broadcasting without traditional database polling.

## 🔐 Core Security & Features
* **Real-Time WebSockets:** Bi-directional communication with zero-latency broadcasting.
* **Stateless JWT Authentication:** Secure session management without relying on hardcoded credentials.
* **Screenshot & PrintScreen Ninja Guard:** Built-in keystroke detection that instantly alerts the room if a user attempts to capture the screen (`PrtScn` or `Win+Shift+S`).
* **Base64 Media Pipeline:** Images are converted to Base64 strings and transmitted directly via WebSockets, ensuring no media files are permanently stored on the server's hard drive.
* **Orphan-Message Guard:** Robust backend error handling to prevent `500 Internal Server Error` crashes caused by deleted user IDs.
* **Live Presence Indicator:** Dynamic tracking of online/offline status for connected nodes.
* **Message Redaction:** Double-click payload unsend functionality across all active clients.

## 🛠️ Tech Stack
* **Backend:** Python, FastAPI, Uvicorn, SQLAlchemy
* **Database:** PostgreSQL (Hosted on Render)
* **Frontend:** Vanilla JavaScript, HTML5, Tailwind CSS (Custom 'Espresso Black' Aesthetic)
* **Deployment:** Render (Backend API) & GitHub Pages (Frontend SPA)

## 💻 Local Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/sifat-dev-code/nexus-secure-chat.git](https://github.com/sifat-dev-code/nexus-secure-chat.git)
   cd nexus-secure-chat
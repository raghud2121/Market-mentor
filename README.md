# Market-Mentor 📈


Market-Mentor Lite is a sleek, modern web application that provides real-time stock analysis. Users can search for any stock ticker to view its current price, historical performance on an interactive chart, and the latest company news with AI-powered sentiment analysis.

This project was built to demonstrate proficiency in full-stack development, API integration, and the application of machine learning models in a real-world scenario.

### **Features**

* **Real-Time Stock Quotes:** Get the latest stock price, day's change, and percentage change.
* **Interactive Historical Chart:** Visualize stock performance over 1-month, 6-month, and 1-year periods.
* **AI-Powered Sentiment Analysis:** Recent news headlines are analyzed by a `FinBERT` model to determine if the sentiment is positive, negative, or neutral.
* **Modern, Responsive UI:** A sleek dark-mode interface with a professional grid layout and smooth loading animations.
* **Robust Backend:** Built with Python and Flask, serving data efficiently from external APIs.

---

### **Tech Stack & Architecture**

#### **Backend**
* **Framework:** Python (Flask)
* **APIs:** Finnhub.io for stock and news data.
* **Machine Learning:** Hugging Face `transformers` library with the `ProsusAI/finbert` model for sentiment analysis.
* **Deployment:** Render / Heroku

#### **Frontend**
* **Framework:** React (Vite)
* **Data Fetching:** Axios
* **Charting:** Chart.js with `react-chartjs-2`
* **Styling:** Custom CSS with a focus on modern design principles (Flexbox, Grid).
* **Deployment:** Vercel / Netlify

---

### **How To Run Locally**

**Prerequisites:**
* Python 3.8+
* Node.js & npm
* A free API key from [Finnhub.io](https://finnhub.io)

*Setup the Backend:

Bash

cd backend

# Create and activate a virtual environment
python -m venv venv
# On Windows: venv\Scripts\activate
# On macOS/Linux: source venv/bin/activate

# Install dependencies
pip install Flask flask-cors requests transformers torch

# IMPORTANT: Open app.py and add your Finnhub API key
# Run the server
python app.py
The backend will be running on http://127.0.0.1:5000.

3. Setup the Frontend:
Open a new terminal window.

Bash

cd frontend

# Install dependencies
npm install

# Run the development server
npm run dev
The frontend will open in your browser, usually at http://localhost:5173.

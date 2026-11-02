<div align="center">

# 🗳️ Online Voting System

A simple web app where each voter casts one vote and everyone can see live results.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Alt%20Version-000000?logo=flask&logoColor=white)

### [🔗 Live Demo](https://python-ecg7tdc2uglrcpui5fcxrj.streamlit.app/)

</div>

---

## ✨ Features

- Vote using a Voter ID and a candidate choice
- One vote per Voter ID (case-insensitive, extra spaces ignored)
- Live results tab with vote counts and progress bars
- Input validation for missing ID or candidate
- Thread-safe vote counting

## 🛠️ Tech Stack

| Part | Technology |
|---|---|
| Language | Python 3 |
| Main app | Streamlit |
| Alternative app | Flask + Tailwind CSS |
| Hosting | Streamlit Community Cloud |

## 📁 Project Structure

```
.
├── streamlit_app.py   # Streamlit version (deployed)
├── app.py             # Flask version
├── requirements.txt
└── README.md
```

## 🚀 Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start the app
streamlit run streamlit_app.py
```

The app opens at http://localhost:8501

**Flask version (optional):**

```bash
pip install flask gunicorn
python app.py
```

Opens at http://127.0.0.1:5000

## ☁️ Deployment

**Streamlit Community Cloud**

1. Push this repo to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click **Create app**, choose the repo, branch `main`, and main file `streamlit_app.py`.
4. Click **Deploy**.

**Render (Flask version)**

- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn app:app --workers 1 --threads 4`
- Environment variable: `SECRET_KEY` = any random string

> Use exactly 1 worker, since votes are stored in memory.

## ⚙️ Customize Candidates

Edit the dictionary in `streamlit_app.py`:

```python
CANDIDATES = {
    1: "Vinit",
    2: "Vedant",
    3: "Venkatesh",
}
```

## ⚠️ Limitations

- Votes are stored in memory and reset when the app restarts or sleeps.
- Voter IDs are not checked against a registered list, so this is a demo and not suitable for real elections.

## 🔮 Future Improvements

- Persistent storage (SQLite or a hosted database)
- Registered voter list with verification
- Admin page and winner highlight

## 👤 Author

Made by **Vinit**

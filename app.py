import os
from threading import Lock
 
from flask import (Flask, request, render_template_string, redirect,
                   url_for, flash, get_flashed_messages)
 
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-change-me")
 
candidates = {
    1: "Vinit",
    2: "Vedant",
    3: "Venkatesh",
}
 
votes = {1: 0, 2: 0, 3: 0}
voters = set()
lock = Lock()
 
PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Online Voting System</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-100 min-h-screen flex items-center justify-center p-4">
 
  <div class="w-full max-w-md bg-white rounded-2xl shadow-lg p-6">
    <h1 class="text-2xl font-bold text-center text-slate-800 mb-1">Online Voting System</h1>
    <p class="text-center text-slate-500 mb-6">Cast your vote below</p>
 
    <!-- Tabs -->
    <div class="flex mb-6 rounded-lg bg-slate-100 p-1">
      <a href="{{ url_for('home') }}"
         class="flex-1 text-center py-2 rounded-md text-sm font-medium
                {{ 'bg-white shadow text-indigo-600' if page == 'vote' else 'text-slate-500' }}">Vote</a>
      <a href="{{ url_for('results') }}"
         class="flex-1 text-center py-2 rounded-md text-sm font-medium
                {{ 'bg-white shadow text-indigo-600' if page == 'results' else 'text-slate-500' }}">Results</a>
    </div>
 
    <!-- Message -->
    {% if message %}
    <div class="mb-4 rounded-lg px-4 py-3 text-sm
                {{ 'bg-green-100 text-green-800' if ok else 'bg-red-100 text-red-800' }}">
      {{ message }}
    </div>
    {% endif %}
 
    {% if page == 'vote' %}
    <!-- Vote form -->
    <form method="POST" action="{{ url_for('vote') }}" class="space-y-4">
      <div>
        <label class="block text-sm font-medium text-slate-700 mb-1">Voter ID</label>
        <input type="text" name="voter_id" required
               class="w-full rounded-lg border border-slate-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500">
      </div>
 
      <div>
        <p class="block text-sm font-medium text-slate-700 mb-2">Choose a candidate</p>
        <div class="space-y-2">
          {% for number, name in candidates.items() %}
          <label class="flex items-center gap-3 rounded-lg border border-slate-300 px-3 py-2 cursor-pointer hover:bg-indigo-50">
            <input type="radio" name="candidate" value="{{ number }}" required class="accent-indigo-600">
            <span class="text-slate-800">{{ name }}</span>
          </label>
          {% endfor %}
        </div>
      </div>
 
      <button type="submit"
              class="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-2 rounded-lg">
        Submit vote
      </button>
    </form>
 
    {% else %}
    <!-- Results -->
    <div class="space-y-4">
      {% for number, name in candidates.items() %}
      {% set count = votes[number] %}
      {% set percent = (count / total * 100) | round(0) if total else 0 %}
      <div>
        <div class="flex justify-between text-sm mb-1">
          <span class="font-medium text-slate-800">{{ name }}</span>
          <span class="text-slate-500">{{ count }} votes</span>
        </div>
        <div class="w-full bg-slate-200 rounded-full h-3">
          <div class="bg-indigo-600 h-3 rounded-full" style="width: {{ percent }}%"></div>
        </div>
      </div>
      {% endfor %}
      <p class="text-center text-sm text-slate-500 pt-2">Total votes: {{ total }}</p>
    </div>
    {% endif %}
  </div>
 
</body>
</html>
"""
 
 
@app.route("/")
def home():
    msgs = get_flashed_messages(with_categories=True)
    ok, message = (msgs[0][0] == "ok", msgs[0][1]) if msgs else (False, None)
    return render_template_string(PAGE, page="vote", candidates=candidates,
                                  message=message, ok=ok)
 
 
@app.route("/vote", methods=["POST"])
def vote():
    voter_id = request.form.get("voter_id", "").strip().lower()
    try:
        choice = int(request.form.get("candidate", ""))
    except ValueError:
        choice = None
 
    if not voter_id:
        flash("Voter ID is required.", "err")
    elif choice not in candidates:
        flash("Invalid candidate.", "err")
    else:
        with lock:
            if voter_id in voters:
                flash("You have already voted!", "err")
            else:
                votes[choice] += 1
                voters.add(voter_id)
                flash("Vote submitted successfully!", "ok")
 
    return redirect(url_for("home"))
 
 
@app.route("/results")
def results():
    with lock:
        snapshot = dict(votes)
    return render_template_string(PAGE, page="results", candidates=candidates,
                                  votes=snapshot, total=sum(snapshot.values()),
                                  message=None, ok=False)
 
 
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
 
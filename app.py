import json
import os
from pathlib import Path
from threading import Lock

import streamlit as st

st.set_page_config(page_title="Online Voting System", page_icon="🗳️", layout="centered")

DATA_FILE = Path("election.json")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin123")  # change this!
VALID_IDS = {str(i) for i in range(1, 101)}  # Voter IDs 1 to 100


@st.cache_resource
def get_lock():
    return Lock()


lock = get_lock()


def load():
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text())
    return {"candidates": ["Vinit", "Vedant", "Venkatesh"], "votes": {}, "voters": []}


def save(data):
    DATA_FILE.write_text(json.dumps(data, indent=2))


st.title("🗳️ Online Voting System")
vote_tab, results_tab, admin_tab = st.tabs(["Vote", "Results", "Admin"])

# ---------- Vote ----------
with vote_tab:
    candidates = load()["candidates"]
    if not candidates:
        st.info("No candidates yet.")
    else:
        with st.form("vote_form", clear_on_submit=True):
            voter_id = st.text_input("Voter ID (1-100)")
            choice = st.radio("Choose a candidate", candidates, index=None)
            submitted = st.form_submit_button("Submit vote", use_container_width=True)

        if submitted:
            vid = voter_id.strip()
            if vid not in VALID_IDS:
                st.error("Invalid Voter ID. Enter a number from 1 to 100.")
            elif choice is None:
                st.error("Please choose a candidate.")
            else:
                with lock:
                    data = load()
                    if vid in data["voters"]:
                        st.error("This Voter ID has already voted.")
                    elif choice not in data["candidates"]:
                        st.error("That candidate was removed. Please choose again.")
                    else:
                        data["votes"][choice] = data["votes"].get(choice, 0) + 1
                        data["voters"].append(vid)
                        save(data)
                        st.success("Vote submitted successfully!")

# ---------- Results ----------
with results_tab:
    data = load()
    total = len(data["voters"])

    for name in data["candidates"]:
        count = data["votes"].get(name, 0)
        st.write(f"**{name}**: {count} votes")
        st.progress(count / total if total else 0)

    st.caption(f"Total votes: {total} / {len(VALID_IDS)} voters")

    if total:
        top = max(data["votes"].get(n, 0) for n in data["candidates"])
        leaders = [n for n in data["candidates"] if data["votes"].get(n, 0) == top]
        if len(leaders) == 1:
            st.success(f"Leading: {leaders[0]}")
        else:
            st.info(f"Tie between: {', '.join(leaders)}")

    st.button("Refresh results")

# ---------- Admin ----------
with admin_tab:
    if not st.session_state.get("is_admin"):
        with st.form("admin_login"):
            pw = st.text_input("Admin password", type="password")
            ok = st.form_submit_button("Log in", use_container_width=True)
        if ok:
            if pw == ADMIN_PASSWORD:
                st.session_state.is_admin = True
                st.rerun()
            else:
                st.error("Wrong password.")
    else:
        data = load()
        started = len(data["voters"]) > 0

        st.subheader("Candidates")
        if started:
            st.warning("Voting has started. Candidates are locked. Reset the election to change them.")
        else:
            with st.form("add_form", clear_on_submit=True):
                new = st.text_input("New candidate name")
                add = st.form_submit_button("Add candidate")
            if add:
                new = " ".join(new.split())
                if not new:
                    st.error("Enter a name.")
                elif new.lower() in [c.lower() for c in data["candidates"]]:
                    st.error("Candidate already exists.")
                else:
                    with lock:
                        data = load()
                        data["candidates"].append(new)
                        save(data)
                    st.rerun()

            if data["candidates"]:
                with st.form("remove_form"):
                    target = st.selectbox("Remove a candidate", data["candidates"])
                    rem = st.form_submit_button("Remove")
                if rem:
                    with lock:
                        data = load()
                        data["candidates"].remove(target)
                        save(data)
                    st.rerun()

        st.divider()
        st.subheader("Reset election")
        confirm = st.checkbox("Delete all votes and start over")
        if st.button("Reset", disabled=not confirm):
            with lock:
                data = load()
                data["votes"] = {}
                data["voters"] = []
                save(data)
            st.rerun()

        if st.button("Log out"):
            st.session_state.pop("is_admin", None)
            st.rerun()

from threading import Lock
 
import streamlit as st
 
st.set_page_config(page_title="Online Voting System", page_icon="🗳️", layout="centered")
 
CANDIDATES = {
    1: "Vinit",
    2: "Vedant",
    3: "Venkatesh",
}
 
 
@st.cache_resource
def get_store():
    """Shared across all visitors while the app is running."""
    return {
        "votes": {k: 0 for k in CANDIDATES},
        "voters": set(),
        "lock": Lock(),
    }
 
 
store = get_store()
 
st.title("🗳️ Online Voting System")
st.caption("Cast your vote below")
 
vote_tab, results_tab = st.tabs(["Vote", "Results"])
 
with vote_tab:
    with st.form("vote_form", clear_on_submit=True):
        voter_id = st.text_input("Voter ID")
        choice = st.radio(
            "Choose a candidate",
            options=list(CANDIDATES.keys()),
            format_func=lambda k: CANDIDATES[k],
            index=None,
        )
        submitted = st.form_submit_button("Submit vote", use_container_width=True)
 
    if submitted:
        vid = voter_id.strip().lower()
        if not vid:
            st.error("Voter ID is required.")
        elif choice is None:
            st.error("Please choose a candidate.")
        else:
            with store["lock"]:
                if vid in store["voters"]:
                    st.error("You have already voted!")
                else:
                    store["votes"][choice] += 1
                    store["voters"].add(vid)
                    st.success("Vote submitted successfully!")
 
with results_tab:
    with store["lock"]:
        votes = dict(store["votes"])
    total = sum(votes.values())
 
    for k, name in CANDIDATES.items():
        count = votes[k]
        percent = count / total if total else 0
        st.write(f"**{name}** — {count} votes")
        st.progress(percent)
 
    st.caption(f"Total votes: {total}")
    st.button("Refresh results")
 

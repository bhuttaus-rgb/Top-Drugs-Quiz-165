import random
import string
import time
import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
from streamlit_autorefresh import st_autorefresh

# ---------- Firebase ----------
@st.cache_resource
def init_firebase():
    config = dict(st.secrets["firebase"])
    config["private_key"] = config["private_key"].replace("\\n", "\n")

    if not firebase_admin._apps:
        cred = credentials.Certificate(config)
        firebase_admin.initialize_app(
            cred,
            {"databaseURL": config["database_url"]}
        )

    return db.reference("rooms")

rooms_ref = init_firebase()
leaderboard_ref = db.reference("leaderboard")

# ---------- App ----------
st.set_page_config(page_title="War on Drugs", page_icon="💊")
st.title("War on Drugs")

# Auto-refresh every 1 second so timer/state updates across both players
st_autorefresh(interval=1000, key="battle_refresh")

# ---------- Room Code Generator ----------
def generate_room_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

# ---------- Wrong Answer Messages ----------
WRONG_MESSAGES = [
    "Oof… that hurt 😬",
    "Dipiro would be disappointed 😭",
    "You might wanna review that one 👀",
    "Not quite 😅",
    "Pharm police watching 🚨",
    "Are you DA right now 😭"
]

# ---------- Master question bank ----------
MASTER_QUESTIONS = [
    {
        "q": "What is the mechanism of action of bisacodyl?",
        "choices": ["Stimulant laxative", "Stool softener", "Fiber laxative", "Hyperosmotic laxative"],
        "a": "Stimulant laxative"
    },
    {
        "q": "Which drug is used for IBS and is an antimuscarinic?",
        "choices": ["Dicyclomine", "Loperamide", "Senna", "Rifaximin"],
        "a": "Dicyclomine"
    },
    {
        "q": "What is the brand name of docusate?",
        "choices": ["Colace", "Dulcolax", "Linzess", "Imodium AD"],
        "a": "Colace"
    },
    {
        "q": "Which drug is a guanylate cyclase agonist?",
        "choices": ["Linaclotide", "Lubiprostone", "Psyllium", "Polyethylene glycol"],
        "a": "Linaclotide"
    },
    {
        "q": "Which drug treats diarrhea but does not treat the underlying cause?",
        "choices": ["Loperamide", "Rifaximin", "Docusate", "Bisacodyl"],
        "a": "Loperamide"
    },
    {
        "q": "Which drug is a chloride channel activator?",
        "choices": ["Lubiprostone", "Linaclotide", "Psyllium", "Senna"],
        "a": "Lubiprostone"
    },
    {
        "q": "What is the mechanism of polyethylene glycol?",
        "choices": ["Hyperosmotic laxative", "Stimulant laxative", "Stool softener", "Antidiarrheal"],
        "a": "Hyperosmotic laxative"
    },
    {
        "q": "Which drug is a fiber laxative?",
        "choices": ["Psyllium", "Senna", "Bisacodyl", "Docusate"],
        "a": "Psyllium"
    },
    {
        "q": "Which drug is used for hepatic encephalopathy prevention?",
        "choices": ["Rifaximin", "Loperamide", "Lubiprostone", "Dicyclomine"],
        "a": "Rifaximin"
    },
    {
        "q": "Which drug is a stimulant laxative taken at bedtime?",
        "choices": ["Senna", "Docusate", "Polyethylene glycol", "Psyllium"],
        "a": "Senna"
    },
    {
        "q": "Which drug is contraindicated in children recovering from flu or varicella?",
        "choices": ["Bismuth subsalicylate", "Famotidine", "Omeprazole", "Magnesium hydroxide"],
        "a": "Bismuth subsalicylate"
    },
    {
        "q": "What class is famotidine?",
        "choices": ["Histamine H2 antagonist", "Proton pump inhibitor", "Antacid", "Dopamine antagonist"],
        "a": "Histamine H2 antagonist"
    },
    {
        "q": "Which drug is a probiotic?",
        "choices": ["Lactobacillus", "Famotidine", "Omeprazole", "Sucralfate"],
        "a": "Lactobacillus"
    },
    {
        "q": "What is the brand name of magnesium hydroxide?",
        "choices": ["Milk of Magnesia", "Pepcid", "Prilosec", "Carafate"],
        "a": "Milk of Magnesia"
    },
    {
        "q": "Which drug has a boxed warning for tardive dyskinesia?",
        "choices": ["Metoclopramide", "Omeprazole", "Famotidine", "Sucralfate"],
        "a": "Metoclopramide"
    },
    {
        "q": "Which drug is a proton pump inhibitor?",
        "choices": ["Omeprazole", "Famotidine", "Sucralfate", "Metoclopramide"],
        "a": "Omeprazole"
    },
    {
        "q": "Which proton pump inhibitor has Protonix as a brand name?",
        "choices": ["Pantoprazole", "Omeprazole", "Famotidine", "Sucralfate"],
        "a": "Pantoprazole"
    },
    {
        "q": "Which drug is used for duodenal ulcer and should be taken on an empty stomach?",
        "choices": ["Sucralfate", "Famotidine", "Omeprazole", "Magnesium hydroxide"],
        "a": "Sucralfate"
    },
    {
        "q": "Which topical drug is used for hemorrhoidal pain, burning, or itching?",
        "choices": ["Phenylephrine topical", "Promethazine", "Pantoprazole", "Famotidine"],
        "a": "Phenylephrine topical"
    },
    {
        "q": "Which drug is a phenothiazine antihistamine used for nausea and vomiting?",
        "choices": ["Promethazine", "Diphenhydramine", "Hydroxyzine", "Cetirizine"],
        "a": "Promethazine"
    },
    {
        "q": "What is the brand name of azelastine?",
        "choices": ["Astepro", "Zyrtec", "Afrin", "NasalCrom"],
        "a": "Astepro"
    },
    {
        "q": "Which drug is a mast cell stabilizer?",
        "choices": ["Cromolyn sodium", "Mometasone", "Oxymetazoline", "Azelastine"],
        "a": "Cromolyn sodium"
    },
    {
        "q": "Which drug is a cough suppressant that can cause euphoria or hallucinations when abused?",
        "choices": ["Dextromethorphan", "Guaifenesin", "Diphenhydramine", "Benzonatate"],
        "a": "Dextromethorphan"
    },
    {
        "q": "What is the brand name of diphenhydramine?",
        "choices": ["Benadryl", "Zyrtec", "Vistaril", "Mucinex"],
        "a": "Benadryl"
    },
    {
        "q": "Which drug is an expectorant?",
        "choices": ["Guaifenesin", "Dextromethorphan", "Diphenhydramine", "Hydroxyzine"],
        "a": "Guaifenesin"
    },
    {
        "q": "Which drug is a piperazine derivative antihistamine?",
        "choices": ["Hydroxyzine", "Diphenhydramine", "Cetirizine", "Azelastine"],
        "a": "Hydroxyzine"
    },
    {
        "q": "What is the brand name of ketotifen ophthalmic?",
        "choices": ["Zaditor", "Afrin", "Astepro", "Benadryl"],
        "a": "Zaditor"
    },
    {
        "q": "Which drug is an intranasal corticosteroid?",
        "choices": ["Mometasone", "Azelastine", "Cromolyn sodium", "Oxymetazoline"],
        "a": "Mometasone"
    },
    {
        "q": "Which nasal spray should not be used for more than 3 consecutive days?",
        "choices": ["Oxymetazoline", "Mometasone", "Cromolyn sodium", "Azelastine"],
        "a": "Oxymetazoline"
    },
    {
        "q": "Which drug should not be chewed because it can cause oral and pharyngeal numbness?",
        "choices": ["Benzonatate", "Dextromethorphan", "Guaifenesin", "Diphenhydramine"],
        "a": "Benzonatate"
    },
    {
        "q": "Which drug is used for emergency treatment of acute anaphylaxis?",
        "choices": ["Epinephrine auto-injector", "Diphenhydramine", "Hydroxyzine", "Cetirizine"],
        "a": "Epinephrine auto-injector"
    },
    {
        "q": "Which drug is contraindicated with concurrent or recent MAOI use and is used for nasal congestion?",
        "choices": ["Pseudoephedrine", "Oxymetazoline", "Azelastine", "Mometasone"],
        "a": "Pseudoephedrine"
    },
    {
        "q": "Which ophthalmic decongestant is contraindicated in narrow-angle glaucoma?",
        "choices": ["Naphazoline", "Ketotifen", "Azelastine", "Mometasone"],
        "a": "Naphazoline"
    },
    {
        "q": "Which drug is a sedative alpha-2 agonist used in ICU or procedural sedation?",
        "choices": ["Dexmedetomidine", "Guanfacine", "Atomoxetine", "Hydroxyzine"],
        "a": "Dexmedetomidine"
    },
    {
        "q": "What is the brand name of levothyroxine?",
        "choices": ["Synthroid", "Strattera", "Vyvanse", "Intuniv"],
        "a": "Synthroid"
    },
    {
        "q": "Which drug has a boxed warning that it is not for weight reduction?",
        "choices": ["Levothyroxine", "Lisdexamfetamine", "Atomoxetine", "Methylphenidate"],
        "a": "Levothyroxine"
    },
    {
        "q": "What is the brand name of atomoxetine?",
        "choices": ["Strattera", "Vyvanse", "Concerta", "Intuniv"],
        "a": "Strattera"
    },
    {
        "q": "Which drug has a boxed warning for suicidality in children and adolescents?",
        "choices": ["Atomoxetine", "Guanfacine", "Lisdexamfetamine", "Methylphenidate"],
        "a": "Atomoxetine"
    },
    {
        "q": "Which drug is an alpha-2 agonist with Intuniv as a brand name?",
        "choices": ["Guanfacine", "Atomoxetine", "Lisdexamfetamine", "Methylphenidate"],
        "a": "Guanfacine"
    },
    {
        "q": "What is the brand name of lisdexamfetamine?",
        "choices": ["Vyvanse", "Concerta", "Strattera", "Intuniv"],
        "a": "Vyvanse"
    },
    {
        "q": "Which stimulant has a boxed warning for risk of abuse, misuse, and diversion?",
        "choices": ["Lisdexamfetamine", "Atomoxetine", "Guanfacine", "Hydroxyzine"],
        "a": "Lisdexamfetamine"
    },
    {
        "q": "Which drug has Concerta and Ritalin as brand names?",
        "choices": ["Methylphenidate", "Lisdexamfetamine", "Atomoxetine", "Guanfacine"],
        "a": "Methylphenidate"
    },
    {
        "q": "Which stimulant is also used for narcolepsy?",
        "choices": ["Methylphenidate", "Atomoxetine", "Guanfacine", "Hydroxyzine"],
        "a": "Methylphenidate"
    },
    {
        "q": "Which antihistamine is contraindicated in patients with hypersensitivity to hydroxyzine?",
        "choices": ["Cetirizine", "Diphenhydramine", "Hydroxyzine", "Azelastine"],
        "a": "Cetirizine"
    },
    {
        "q": "What is the brand name of cetirizine?",
        "choices": ["Zyrtec", "Astepro", "Benadryl", "Vistaril"],
        "a": "Zyrtec"
    },
    {
        "q": "Which drug should be taken 1 hour before meals and may restart after 4 months for OTC use?",
        "choices": ["Omeprazole", "Famotidine", "Sucralfate", "Pantoprazole"],
        "a": "Omeprazole"
    },
    {
        "q": "Which drug may cause dyspnea or chest tightness with the first dose?",
        "choices": ["Lubiprostone", "Linaclotide", "Psyllium", "Loperamide"],
        "a": "Lubiprostone"
    },
    {
        "q": "Which drug should be avoided with mineral oil unless approved by a health care provider?",
        "choices": ["Docusate", "Senna", "Psyllium", "Rifaximin"],
        "a": "Docusate"
    },
    {
        "q": "Which drug should be separated 2 hours from other medications and dust inhalation should be avoided?",
        "choices": ["Psyllium", "Bisacodyl", "Docusate", "Loperamide"],
        "a": "Psyllium"
    }
]

# ---------- Helpers ----------
def build_game_questions(num_questions=10):
    pool = [dict(q) for q in MASTER_QUESTIONS]
    random.shuffle(pool)
    selected = pool[:num_questions]

    for q in selected:
        random.shuffle(q["choices"])

    return selected

def reset_room_state(room_ref):
    room_ref.update({
        "score1": 0,
        "score2": 0,
        "current_question": 0,
        "buzzer": "",
        "steal_turn": "",
        "turn_deadline": 0,
        "winner_recorded": False,
        "feedback": "",
        "questions": build_game_questions()
    })

def other_player(role):
    return "player2" if role == "player1" else "player1"

def player_label(role):
    return "Player 1" if role == "player1" else "Player 2"

def get_player_name(room_data, role):
    return room_data.get(role, "")

def record_win(winner_name):
    if not winner_name:
        return

    player_ref = leaderboard_ref.child(winner_name)
    data = player_ref.get()

    if data is None:
        player_ref.set({"wins": 1})
    else:
        current_wins = data.get("wins", 0)
        player_ref.update({"wins": current_wins + 1})

def get_leaderboard():
    data = leaderboard_ref.get()
    if not data:
        return []

    rows = []
    for player, stats in data.items():
        rows.append({
            "name": player,
            "wins": stats.get("wins", 0)
        })

    rows.sort(key=lambda x: x["wins"], reverse=True)
    return rows

# ---------- Pretty Leaderboard ----------
st.subheader("🏆 Leaderboard")
leaderboard = get_leaderboard()

if leaderboard:
    total_players = len(leaderboard)
    total_wins = sum(player["wins"] for player in leaderboard)

    col1, col2 = st.columns(2)
    col1.metric("Players", total_players)
    col2.metric("Total Wins", total_wins)

    medals = {1: "🥇", 2: "🥈", 3: "🥉"}

    for i, player in enumerate(leaderboard[:10], start=1):
        badge = medals.get(i, f"{i}.")
        st.markdown(
            f"""
            <div style="
                padding:10px 14px;
                margin-bottom:8px;
                border:1px solid #e6e6e6;
                border-radius:12px;
                display:flex;
                justify-content:space-between;
                align-items:center;
                background-color:#fafafa;
            ">
                <div style="font-size:18px;">{badge} <b>{player['name']}</b></div>
                <div style="font-size:16px;"><b>{player['wins']}</b> win(s)</div>
            </div>
            """,
            unsafe_allow_html=True
        )
else:
    st.info("No wins recorded yet.")

# ---------- Inputs ----------
name = st.text_input("Your name")

if "room_code" not in st.session_state:
    st.session_state.room_code = generate_room_code()

room = st.text_input("Room code", value=st.session_state.room_code).strip().upper()
st.caption("Share this room code with your opponent")

# ---------- Join Room ----------
if st.button("Join Room"):
    if not name.strip():
        st.error("Enter your name first.")
    elif not room:
        st.error("Enter a room code.")
    else:
        room_ref = rooms_ref.child(room)
        room_data = room_ref.get()

        if room_data is None:
            room_ref.set({
                "player1": name,
                "player2": "",
                "score1": 0,
                "score2": 0,
                "current_question": 0,
                "buzzer": "",
                "steal_turn": "",
                "turn_deadline": 0,
                "winner_recorded": False,
                "feedback": "",
                "questions": build_game_questions()
            })
            st.success(f"{name} joined {room} as Player 1")
            st.rerun()

        else:
            player1 = room_data.get("player1", "")
            player2 = room_data.get("player2", "")

            if player1 == name or player2 == name:
                st.success(f"{name} rejoined {room}")

            elif not player1:
                room_ref.update({"player1": name})
                st.success(f"{name} joined {room} as Player 1")
                st.rerun()

            elif not player2:
                room_ref.update({"player2": name})
                st.success(f"{name} joined {room} as Player 2")
                st.rerun()

            else:
                st.error("Room is full.")

# ---------- Load Room ----------
room_data = rooms_ref.child(room).get() if room else None

player_role = None
if room_data:
    if name == room_data.get("player1"):
        player_role = "player1"
    elif name == room_data.get("player2"):
        player_role = "player2"

# ---------- Main Game ----------
if room_data:
    room_ref = rooms_ref.child(room)

    now = time.time()
    buzzer = room_data.get("buzzer", "")
    steal_turn = room_data.get("steal_turn", "")
    deadline = room_data.get("turn_deadline", 0)

    if deadline and now > deadline:
        if steal_turn:
            room_ref.update({
                "current_question": room_data.get("current_question", 0) + 1,
                "buzzer": "",
                "steal_turn": "",
                "turn_deadline": 0,
                "feedback": "Time's up! Moving to the next question ⏭️"
            })
            st.rerun()
        elif buzzer:
            room_ref.update({
                "steal_turn": other_player(buzzer),
                "turn_deadline": time.time() + 5,
                "feedback": "⚡ Steal opportunity!"
            })
            st.rerun()

    room_data = room_ref.get()
    buzzer = room_data.get("buzzer", "")
    steal_turn = room_data.get("steal_turn", "")
    deadline = room_data.get("turn_deadline", 0)

    st.subheader(f"Room: {room}")
    st.write("Player 1:", room_data.get("player1", ""))
    st.write("Player 2:", room_data.get("player2", ""))
    st.write("Score 1:", room_data.get("score1", 0))
    st.write("Score 2:", room_data.get("score2", 0))

    feedback = room_data.get("feedback", "")
    if feedback:
        if "correct" in feedback.lower():
            st.success(feedback)
        elif "wrong" in feedback.lower() or "dipiro" in feedback.lower() or "oof" in feedback.lower() or "da" in feedback.lower():
            st.error(feedback)
        else:
            st.info(feedback)

    questions = room_data.get("questions", [])
    q_index = room_data.get("current_question", 0)

    if q_index < len(questions):
        current_question = questions[q_index]
        st.write(f"Question {q_index + 1} of {len(questions)}")
        st.write("### Question")
        st.write(current_question["q"])
    else:
        current_question = None
        st.success("Game over")

        p1 = room_data.get("score1", 0)
        p2 = room_data.get("score2", 0)

        if p1 > p2:
            winner_name = room_data.get("player1", "Player 1")

            if not room_data.get("winner_recorded", False):
                record_win(winner_name)
                room_ref.update({"winner_recorded": True})

            st.balloons()
            st.success(f"🏆 {winner_name} wins!")

        elif p2 > p1:
            winner_name = room_data.get("player2", "Player 2")

            if not room_data.get("winner_recorded", False):
                record_win(winner_name)
                room_ref.update({"winner_recorded": True})

            st.balloons()
            st.success(f"🏆 {winner_name} wins!")

        else:
            st.info("🤝 It's a tie!")

    if buzzer:
        st.write(f"⚡ {get_player_name(room_data, buzzer)} buzzed!")
    else:
        st.write("Buzzer: None")

    if steal_turn:
        st.write("Steal Turn:", player_label(steal_turn))

    if deadline and current_question and (buzzer or steal_turn):
        seconds_left = max(0, int(deadline - time.time()) + (1 if deadline - time.time() > 0 else 0))
        st.write(f"⏱️ Time left: {seconds_left}s")
        if seconds_left <= 2:
            st.warning("⏰ HURRY!")

    if current_question:
        if buzzer == "" and steal_turn == "":
            if st.button("🔴 Buzz"):
                if player_role:
                    room_ref.update({
                        "buzzer": player_role,
                        "turn_deadline": time.time() + 5,
                        "feedback": ""
                    })
                    st.rerun()

        elif steal_turn:
            if player_role == steal_turn:
                st.warning("Steal chance! Pick an answer in 5 seconds.")

                for i, choice in enumerate(current_question["choices"]):
                    if st.button(choice, key=f"steal_{q_index}_{i}"):
                        if choice.lower() == current_question["a"].lower():
                            if player_role == "player1":
                                room_ref.update({
                                    "score1": room_data.get("score1", 0) + 1,
                                    "current_question": q_index + 1,
                                    "buzzer": "",
                                    "steal_turn": "",
                                    "turn_deadline": 0,
                                    "feedback": f"{name} got it correct! ✅"
                                })
                            else:
                                room_ref.update({
                                    "score2": room_data.get("score2", 0) + 1,
                                    "current_question": q_index + 1,
                                    "buzzer": "",
                                    "steal_turn": "",
                                    "turn_deadline": 0,
                                    "feedback": f"{name} got it correct! ✅"
                                })
                        else:
                            room_ref.update({
                                "current_question": q_index + 1,
                                "buzzer": "",
                                "steal_turn": "",
                                "turn_deadline": 0,
                                "feedback": random.choice(WRONG_MESSAGES)
                            })
                        st.rerun()
            else:
                st.warning("Other player is attempting the steal.")

        else:
            if player_role == buzzer:
                st.success("You buzzed first! Pick an answer in 5 seconds.")

                for i, choice in enumerate(current_question["choices"]):
                    if st.button(choice, key=f"buzz_{q_index}_{i}"):
                        if choice.lower() == current_question["a"].lower():
                            if player_role == "player1":
                                room_ref.update({
                                    "score1": room_data.get("score1", 0) + 1,
                                    "current_question": q_index + 1,
                                    "buzzer": "",
                                    "steal_turn": "",
                                    "turn_deadline": 0,
                                    "feedback": f"{name} got it correct! ✅"
                                })
                            else:
                                room_ref.update({
                                    "score2": room_data.get("score2", 0) + 1,
                                    "current_question": q_index + 1,
                                    "buzzer": "",
                                    "steal_turn": "",
                                    "turn_deadline": 0,
                                    "feedback": f"{name} got it correct! ✅"
                                })
                        else:
                            room_ref.update({
                                "steal_turn": other_player(player_role),
                                "turn_deadline": time.time() + 5,
                                "feedback": random.choice(WRONG_MESSAGES)
                            })
                        st.rerun()
            else:
                st.warning("Other player buzzed first.")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Reset Buzzer"):
            room_ref.update({
                "buzzer": "",
                "steal_turn": "",
                "turn_deadline": 0,
                "feedback": ""
            })
            st.rerun()

    with col2:
        if st.button("New Game"):
            reset_room_state(room_ref)
            st.session_state.room_code = generate_room_code()
            st.rerun()

else:
    st.info("Join or create a room to start playing.")

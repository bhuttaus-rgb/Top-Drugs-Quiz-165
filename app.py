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
    "Are you DA right now 😭",
]

# ---------- Week Labels ----------
WEEK_OPTIONS = {
    "All Weeks — Mixed Review": "All Weeks",
    "Week 1 — GI: Laxatives / Antidiarrheals": "Week 1",
    "Week 2 — GI: GERD / Antacids": "Week 2",
    "Week 3 — Cough / Cold / Allergy": "Week 3",
    "Week 4 — ADHD / Cognitive / Misc.": "Week 4",
    "Week 5 — Alzheimer’s / Parkinson’s / Sleep": "Week 5",
    "Week 6 — Depression / Anxiety / Bipolar": "Week 6",
    "Week 7 — Seizures / Anxiety": "Week 7",
    "Week 8 — Substance Use / Mood / Pain / Migraine": "Week 8",
}

WEEK_DISPLAY = {
    "All Weeks": "All Weeks — Mixed Review",
    "Week 1": "Week 1 — GI: Laxatives / Antidiarrheals",
    "Week 2": "Week 2 — GI: GERD / Antacids",
    "Week 3": "Week 3 — Cough / Cold / Allergy",
    "Week 4": "Week 4 — ADHD / Cognitive / Misc.",
    "Week 5": "Week 5 — Alzheimer’s / Parkinson’s / Sleep",
    "Week 6": "Week 6 — Depression / Anxiety / Bipolar",
    "Week 7": "Week 7 — Seizures / Anxiety",
    "Week 8": "Week 8 — Substance Use / Mood / Pain / Migraine",
}

# ---------- Question Banks ----------
WEEK_1_QUESTIONS = [
    {"q": "What is the mechanism of action of bisacodyl?", "choices": ["Stimulant laxative", "Stool softener", "Fiber laxative", "Hyperosmotic laxative"], "a": "Stimulant laxative"},
    {"q": "Which drug is used for IBS and is an antimuscarinic?", "choices": ["Dicyclomine", "Loperamide", "Senna", "Rifaximin"], "a": "Dicyclomine"},
    {"q": "What is the brand name of docusate?", "choices": ["Colace", "Dulcolax", "Linzess", "Imodium AD"], "a": "Colace"},
    {"q": "Which drug is a guanylate cyclase agonist?", "choices": ["Linaclotide", "Lubiprostone", "Psyllium", "Polyethylene glycol"], "a": "Linaclotide"},
    {"q": "Which drug treats diarrhea but does not treat the underlying cause?", "choices": ["Loperamide", "Rifaximin", "Docusate", "Bisacodyl"], "a": "Loperamide"},
    {"q": "Which drug is a chloride channel activator?", "choices": ["Lubiprostone", "Linaclotide", "Psyllium", "Senna"], "a": "Lubiprostone"},
    {"q": "What is the mechanism of action of polyethylene glycol?", "choices": ["Hyperosmotic laxative", "Stimulant laxative", "Stool softener", "Antidiarrheal"], "a": "Hyperosmotic laxative"},
    {"q": "Which drug is a fiber laxative?", "choices": ["Psyllium", "Senna", "Bisacodyl", "Docusate"], "a": "Psyllium"},
    {"q": "Which drug is used for hepatic encephalopathy prevention?", "choices": ["Rifaximin", "Loperamide", "Lubiprostone", "Dicyclomine"], "a": "Rifaximin"},
    {"q": "Which drug is a stimulant laxative taken at bedtime?", "choices": ["Senna", "Docusate", "Polyethylene glycol", "Psyllium"], "a": "Senna"},
    {"q": "Which drug has Dulcolax as a brand name?", "choices": ["Bisacodyl", "Docusate", "Senna", "Psyllium"], "a": "Bisacodyl"},
    {"q": "Which drug is contraindicated in intestinal obstruction and should not be given within 1 hour of dairy or antacids?", "choices": ["Bisacodyl", "Loperamide", "Rifaximin", "Dicyclomine"], "a": "Bisacodyl"},
    {"q": "Which drug is a stool softener?", "choices": ["Docusate", "Bisacodyl", "Senna", "Psyllium"], "a": "Docusate"},
    {"q": "Which drug softens stool but does not directly cause defecation?", "choices": ["Docusate", "Senna", "PEG", "Linaclotide"], "a": "Docusate"},
    {"q": "Which drug has Linzess as a brand name?", "choices": ["Linaclotide", "Lubiprostone", "Loperamide", "Rifaximin"], "a": "Linaclotide"},
    {"q": "Which drug is contraindicated in age under 2 years and GI obstruction?", "choices": ["Linaclotide", "Rifaximin", "Docusate", "Psyllium"], "a": "Linaclotide"},
    {"q": "Which drug has Imodium AD as a brand name?", "choices": ["Loperamide", "Rifaximin", "Lubiprostone", "Senna"], "a": "Loperamide"},
    {"q": "Which drug has a boxed warning for TdP, cardiac arrest, and death when maximum dose is exceeded?", "choices": ["Loperamide", "Bisacodyl", "Dicyclomine", "Psyllium"], "a": "Loperamide"},
    {"q": "Which drug has Amitiza as a brand name?", "choices": ["Lubiprostone", "Linaclotide", "PEG", "Rifaximin"], "a": "Lubiprostone"},
    {"q": "Which drug should be taken with food and water and may cause dyspnea with the first dose?", "choices": ["Lubiprostone", "Loperamide", "Psyllium", "Senna"], "a": "Lubiprostone"},
    {"q": "Which drug has MiraLAX as a brand name?", "choices": ["Polyethylene glycol", "Psyllium", "Docusate", "Senna"], "a": "Polyethylene glycol"},
    {"q": "Which drug should be mixed in liquid and often works within 12 to 24 hours?", "choices": ["Polyethylene glycol", "Bisacodyl", "Loperamide", "Dicyclomine"], "a": "Polyethylene glycol"},
    {"q": "Which drug has Metamucil as a brand name?", "choices": ["Psyllium", "Senna", "Docusate", "PEG"], "a": "Psyllium"},
    {"q": "Which drug should be started slowly and titrated up over 1 to 2 weeks?", "choices": ["Psyllium", "Bisacodyl", "Linaclotide", "Rifaximin"], "a": "Psyllium"},
    {"q": "Which drug has Xifaxan as a brand name?", "choices": ["Rifaximin", "Loperamide", "Lubiprostone", "Dicyclomine"], "a": "Rifaximin"},
    {"q": "Which drug is used for travelers diarrhea at 200 mg three times daily for 3 days?", "choices": ["Rifaximin", "Loperamide", "Bisacodyl", "Senna"], "a": "Rifaximin"},
    {"q": "Which drug has Senokot as a brand name?", "choices": ["Senna", "Docusate", "PEG", "Psyllium"], "a": "Senna"},
    {"q": "Which drug may cause urine discoloration and should be spaced from other medications?", "choices": ["Senna", "Bisacodyl", "Linaclotide", "Loperamide"], "a": "Senna"},
]

WEEK_2_QUESTIONS = [
    {"q": "Which drug is contraindicated in children recovering from flu or varicella?", "choices": ["Bismuth subsalicylate", "Famotidine", "Omeprazole", "Magnesium hydroxide"], "a": "Bismuth subsalicylate"},
    {"q": "What class is famotidine?", "choices": ["Histamine H2 antagonist", "Proton pump inhibitor", "Antacid", "Dopamine antagonist"], "a": "Histamine H2 antagonist"},
    {"q": "Which drug is a probiotic?", "choices": ["Lactobacillus", "Famotidine", "Omeprazole", "Sucralfate"], "a": "Lactobacillus"},
    {"q": "What is the brand name of magnesium hydroxide?", "choices": ["Milk of Magnesia", "Pepcid", "Prilosec", "Carafate"], "a": "Milk of Magnesia"},
    {"q": "Which drug has a boxed warning for tardive dyskinesia?", "choices": ["Metoclopramide", "Omeprazole", "Famotidine", "Sucralfate"], "a": "Metoclopramide"},
    {"q": "Which drug is a proton pump inhibitor?", "choices": ["Omeprazole", "Famotidine", "Sucralfate", "Metoclopramide"], "a": "Omeprazole"},
    {"q": "Which proton pump inhibitor has Protonix as a brand name?", "choices": ["Pantoprazole", "Omeprazole", "Famotidine", "Sucralfate"], "a": "Pantoprazole"},
    {"q": "Which drug is used for duodenal ulcer and should be taken on an empty stomach?", "choices": ["Sucralfate", "Famotidine", "Omeprazole", "Magnesium hydroxide"], "a": "Sucralfate"},
    {"q": "Which topical drug is used for hemorrhoidal pain, burning, or itching?", "choices": ["Phenylephrine topical", "Promethazine", "Pantoprazole", "Famotidine"], "a": "Phenylephrine topical"},
    {"q": "Which drug is a phenothiazine antihistamine used for nausea and vomiting?", "choices": ["Promethazine", "Diphenhydramine", "Hydroxyzine", "Cetirizine"], "a": "Promethazine"},
    {"q": "Which drug has Pepcid as a brand name?", "choices": ["Famotidine", "Omeprazole", "Pantoprazole", "Sucralfate"], "a": "Famotidine"},
    {"q": "Which drug should be taken 15 to 60 minutes before meals for heartburn prevention?", "choices": ["Famotidine", "Sucralfate", "Pantoprazole", "Magnesium hydroxide"], "a": "Famotidine"},
    {"q": "Which drug has a lack of strong efficacy data as a clinical pearl?", "choices": ["Lactobacillus", "Famotidine", "Omeprazole", "Promethazine"], "a": "Lactobacillus"},
    {"q": "Which drug should sometimes be kept in the fridge and may lose potency over time?", "choices": ["Lactobacillus", "Sucralfate", "Famotidine", "Pantoprazole"], "a": "Lactobacillus"},
    {"q": "Which drug can be used as both an antacid and a laxative?", "choices": ["Magnesium hydroxide", "Famotidine", "Omeprazole", "Promethazine"], "a": "Magnesium hydroxide"},
    {"q": "Which drug should be used cautiously in renal failure, heart failure, and advanced age?", "choices": ["Magnesium hydroxide", "Famotidine", "Pantoprazole", "Sucralfate"], "a": "Magnesium hydroxide"},
    {"q": "Which drug has Reglan as a brand name?", "choices": ["Metoclopramide", "Sucralfate", "Promethazine", "Famotidine"], "a": "Metoclopramide"},
    {"q": "Which drug is a dopamine antagonist used for diabetic gastroparesis?", "choices": ["Metoclopramide", "Pantoprazole", "Famotidine", "Lactobacillus"], "a": "Metoclopramide"},
    {"q": "Which drug has Prilosec as a brand name?", "choices": ["Omeprazole", "Pantoprazole", "Famotidine", "Sucralfate"], "a": "Omeprazole"},
    {"q": "Which drug has a contraindication with concurrent rilpivirine and is used OTC for 14 days?", "choices": ["Omeprazole", "Famotidine", "Promethazine", "Magnesium hydroxide"], "a": "Omeprazole"},
    {"q": "Which drug has Protonix as a brand name?", "choices": ["Pantoprazole", "Omeprazole", "Famotidine", "Sucralfate"], "a": "Pantoprazole"},
    {"q": "Which drug may cause headache and should ideally be taken before meals?", "choices": ["Pantoprazole", "Promethazine", "Famotidine", "Lactobacillus"], "a": "Pantoprazole"},
    {"q": "Which drug has Phenergan as a brand name?", "choices": ["Promethazine", "Famotidine", "Pantoprazole", "Sucralfate"], "a": "Promethazine"},
    {"q": "Which drug is contraindicated in children younger than 2 years and in comatose states?", "choices": ["Promethazine", "Famotidine", "Sucralfate", "Lactobacillus"], "a": "Promethazine"},
    {"q": "Which drug has Carafate as a brand name?", "choices": ["Sucralfate", "Famotidine", "Omeprazole", "Pantoprazole"], "a": "Sucralfate"},
    {"q": "Which drug should be separated 2 to 4 hours from other medications and shaken well if suspension?", "choices": ["Sucralfate", "Famotidine", "Magnesium hydroxide", "Promethazine"], "a": "Sucralfate"},
]

WEEK_3_QUESTIONS = [
    {"q": "What is the brand name of azelastine?", "choices": ["Astepro", "Zyrtec", "Afrin", "NasalCrom"], "a": "Astepro"},
    {"q": "Which drug is a mast cell stabilizer?", "choices": ["Cromolyn sodium", "Mometasone", "Oxymetazoline", "Azelastine"], "a": "Cromolyn sodium"},
    {"q": "Which drug is a cough suppressant that can cause euphoria or hallucinations when abused?", "choices": ["Dextromethorphan", "Guaifenesin", "Diphenhydramine", "Benzonatate"], "a": "Dextromethorphan"},
    {"q": "What is the brand name of diphenhydramine?", "choices": ["Benadryl", "Zyrtec", "Vistaril", "Mucinex"], "a": "Benadryl"},
    {"q": "Which drug is an expectorant?", "choices": ["Guaifenesin", "Dextromethorphan", "Diphenhydramine", "Hydroxyzine"], "a": "Guaifenesin"},
    {"q": "Which drug is a piperazine derivative antihistamine?", "choices": ["Hydroxyzine", "Diphenhydramine", "Cetirizine", "Azelastine"], "a": "Hydroxyzine"},
    {"q": "What is the brand name of ketotifen ophthalmic?", "choices": ["Zaditor", "Afrin", "Astepro", "Benadryl"], "a": "Zaditor"},
    {"q": "Which drug is an intranasal corticosteroid?", "choices": ["Mometasone", "Azelastine", "Cromolyn sodium", "Oxymetazoline"], "a": "Mometasone"},
    {"q": "Which nasal spray should not be used for more than 3 consecutive days?", "choices": ["Oxymetazoline", "Mometasone", "Cromolyn sodium", "Azelastine"], "a": "Oxymetazoline"},
    {"q": "Which drug should not be chewed because it can cause oral and pharyngeal numbness?", "choices": ["Benzonatate", "Dextromethorphan", "Guaifenesin", "Diphenhydramine"], "a": "Benzonatate"},
    {"q": "Which drug is a nasal antihistamine?", "choices": ["Azelastine", "Mometasone", "Oxymetazoline", "Cromolyn sodium"], "a": "Azelastine"},
    {"q": "Which drug should be primed on first use and avoided in the eyes?", "choices": ["Azelastine", "Cetirizine", "Diphenhydramine", "Guaifenesin"], "a": "Azelastine"},
    {"q": "What is the brand name of cetirizine?", "choices": ["Zyrtec", "Benadryl", "Astepro", "Vistaril"], "a": "Zyrtec"},
    {"q": "Which drug may cause excitability or insomnia in children and has onset within 60 minutes?", "choices": ["Cetirizine", "Diphenhydramine", "Hydroxyzine", "Azelastine"], "a": "Cetirizine"},
    {"q": "What is the brand name of cromolyn sodium nasal?", "choices": ["NasalCrom", "Afrin", "Astepro", "Zaditor"], "a": "NasalCrom"},
    {"q": "Which drug is not appropriate for acute symptom relief and should not be used for cold symptoms?", "choices": ["Cromolyn sodium", "Oxymetazoline", "Mometasone", "Azelastine"], "a": "Cromolyn sodium"},
    {"q": "Which drug has Delsym as a brand name?", "choices": ["Dextromethorphan", "Guaifenesin", "Benzonatate", "Diphenhydramine"], "a": "Dextromethorphan"},
    {"q": "Which drug is contraindicated with concurrent MAOI use and is a cough suppressant?", "choices": ["Dextromethorphan", "Guaifenesin", "Benzonatate", "Hydroxyzine"], "a": "Dextromethorphan"},
    {"q": "Which drug is used only occasionally for sleep and should not be used in children for sleep?", "choices": ["Diphenhydramine", "Cetirizine", "Hydroxyzine", "Guaifenesin"], "a": "Diphenhydramine"},
    {"q": "Which drug has Mucinex as a brand name?", "choices": ["Guaifenesin", "Dextromethorphan", "Diphenhydramine", "Benzonatate"], "a": "Guaifenesin"},
    {"q": "Which drug has little evidence supporting its use for cough?", "choices": ["Guaifenesin", "Dextromethorphan", "Benzonatate", "Azelastine"], "a": "Guaifenesin"},
    {"q": "What is the brand name of hydroxyzine?", "choices": ["Vistaril", "Zyrtec", "Benadryl", "Astepro"], "a": "Vistaril"},
    {"q": "Which drug is contraindicated in patients with hypersensitivity to cetirizine?", "choices": ["Hydroxyzine", "Diphenhydramine", "Azelastine", "Guaifenesin"], "a": "Hydroxyzine"},
    {"q": "Which ophthalmic drug is used for allergic conjunctivitis twice daily 8 to 12 hours apart?", "choices": ["Ketotifen", "Naphazoline", "Azelastine", "Mometasone"], "a": "Ketotifen"},
    {"q": "Which drug requires priming if not used for 1 week and is used for allergic rhinitis?", "choices": ["Mometasone", "Oxymetazoline", "Azelastine", "Cromolyn sodium"], "a": "Mometasone"},
]

WEEK_4_QUESTIONS = [
    {"q": "Which drug is used for emergency treatment of acute anaphylaxis?", "choices": ["Epinephrine auto-injector", "Diphenhydramine", "Hydroxyzine", "Cetirizine"], "a": "Epinephrine auto-injector"},
    {"q": "Which drug is contraindicated with concurrent or recent MAOI use and is used for nasal congestion?", "choices": ["Pseudoephedrine", "Oxymetazoline", "Azelastine", "Mometasone"], "a": "Pseudoephedrine"},
    {"q": "Which ophthalmic decongestant is contraindicated in narrow-angle glaucoma?", "choices": ["Naphazoline", "Ketotifen", "Azelastine", "Mometasone"], "a": "Naphazoline"},
    {"q": "Which drug is a sedative alpha-2 agonist used in ICU or procedural sedation?", "choices": ["Dexmedetomidine", "Guanfacine", "Atomoxetine", "Hydroxyzine"], "a": "Dexmedetomidine"},
    {"q": "What is the brand name of levothyroxine?", "choices": ["Synthroid", "Strattera", "Vyvanse", "Intuniv"], "a": "Synthroid"},
    {"q": "Which drug has a boxed warning that it is not for weight reduction?", "choices": ["Levothyroxine", "Lisdexamfetamine", "Atomoxetine", "Methylphenidate"], "a": "Levothyroxine"},
    {"q": "What is the brand name of atomoxetine?", "choices": ["Strattera", "Vyvanse", "Concerta", "Intuniv"], "a": "Strattera"},
    {"q": "Which drug has a boxed warning for suicidality in children and adolescents?", "choices": ["Atomoxetine", "Guanfacine", "Lisdexamfetamine", "Methylphenidate"], "a": "Atomoxetine"},
    {"q": "Which drug is an alpha-2 agonist with Intuniv as a brand name?", "choices": ["Guanfacine", "Atomoxetine", "Lisdexamfetamine", "Methylphenidate"], "a": "Guanfacine"},
    {"q": "What is the brand name of lisdexamfetamine?", "choices": ["Vyvanse", "Concerta", "Strattera", "Intuniv"], "a": "Vyvanse"},
    {"q": "Which stimulant has a boxed warning for risk of abuse, misuse, and diversion?", "choices": ["Lisdexamfetamine", "Atomoxetine", "Guanfacine", "Hydroxyzine"], "a": "Lisdexamfetamine"},
    {"q": "Which drug has Concerta and Ritalin as brand names?", "choices": ["Methylphenidate", "Lisdexamfetamine", "Atomoxetine", "Guanfacine"], "a": "Methylphenidate"},
    {"q": "Which stimulant is also used for narcolepsy?", "choices": ["Methylphenidate", "Atomoxetine", "Guanfacine", "Hydroxyzine"], "a": "Methylphenidate"},
    {"q": "Which antihistamine is contraindicated in patients with hypersensitivity to hydroxyzine?", "choices": ["Cetirizine", "Diphenhydramine", "Hydroxyzine", "Azelastine"], "a": "Cetirizine"},
    {"q": "What is the brand name of cetirizine?", "choices": ["Zyrtec", "Astepro", "Benadryl", "Vistaril"], "a": "Zyrtec"},
    {"q": "Which drug should be taken 1 hour before meals and may restart after 4 months for OTC use?", "choices": ["Omeprazole", "Famotidine", "Sucralfate", "Pantoprazole"], "a": "Omeprazole"},
    {"q": "Which drug may cause dyspnea or chest tightness with the first dose?", "choices": ["Lubiprostone", "Linaclotide", "Psyllium", "Loperamide"], "a": "Lubiprostone"},
    {"q": "Which drug should be avoided with mineral oil unless approved by a health care provider?", "choices": ["Docusate", "Senna", "Psyllium", "Rifaximin"], "a": "Docusate"},
    {"q": "Which drug should be separated 2 hours from other medications and dust inhalation should be avoided?", "choices": ["Psyllium", "Bisacodyl", "Docusate", "Loperamide"], "a": "Psyllium"},
    {"q": "Which epinephrine product should be injected into the anterolateral thigh?", "choices": ["Epinephrine auto-injector", "Pseudoephedrine", "Diphenhydramine", "Hydroxyzine"], "a": "Epinephrine auto-injector"},
    {"q": "What is the brand name of pseudoephedrine?", "choices": ["Sudafed", "Afrin", "Astepro", "Zyrtec"], "a": "Sudafed"},
    {"q": "Which drug is an alpha/beta agonist used for nasal congestion at 60 mg every 4 to 6 hours?", "choices": ["Pseudoephedrine", "Epinephrine auto-injector", "Naphazoline", "Dexmedetomidine"], "a": "Pseudoephedrine"},
    {"q": "What is the brand name of naphazoline ophthalmic?", "choices": ["Clear Eyes", "Zaditor", "Astepro", "Afrin"], "a": "Clear Eyes"},
    {"q": "Which drug may produce prolonged redness with overuse and is fatal if ingested?", "choices": ["Naphazoline", "Ketotifen", "Azelastine", "Mometasone"], "a": "Naphazoline"},
    {"q": "What is the brand name of dexmedetomidine?", "choices": ["Precedex", "Intuniv", "Strattera", "Vyvanse"], "a": "Precedex"},
    {"q": "Which drug is an alpha-2 agonist used for short-term sedation?", "choices": ["Dexmedetomidine", "Guanfacine", "Atomoxetine", "Hydroxyzine"], "a": "Dexmedetomidine"},
    {"q": "Which drug should be taken on an empty stomach with water at least 30 minutes before food?", "choices": ["Levothyroxine", "Atomoxetine", "Lisdexamfetamine", "Methylphenidate"], "a": "Levothyroxine"},
    {"q": "Which drug should not be abruptly discontinued and may require 6 to 8 weeks for symptomatic improvement?", "choices": ["Levothyroxine", "Guanfacine", "Atomoxetine", "Methylphenidate"], "a": "Levothyroxine"},
    {"q": "Which drug is a norepinephrine reuptake inhibitor used for ADHD?", "choices": ["Atomoxetine", "Guanfacine", "Lisdexamfetamine", "Methylphenidate"], "a": "Atomoxetine"},
    {"q": "Which drug should not have its capsules opened?", "choices": ["Atomoxetine", "Lisdexamfetamine", "Methylphenidate", "Guanfacine"], "a": "Atomoxetine"},
    {"q": "What is the brand name of guanfacine?", "choices": ["Intuniv", "Strattera", "Vyvanse", "Concerta"], "a": "Intuniv"},
    {"q": "Which drug should not be abruptly discontinued because of rebound hypertension?", "choices": ["Guanfacine", "Atomoxetine", "Methylphenidate", "Hydroxyzine"], "a": "Guanfacine"},
    {"q": "Which drug may be opened and dissolved in water, yogurt, or orange juice?", "choices": ["Lisdexamfetamine", "Atomoxetine", "Guanfacine", "Pseudoephedrine"], "a": "Lisdexamfetamine"},
    {"q": "Which stimulant should be taken in the morning and is used for binge eating disorder?", "choices": ["Lisdexamfetamine", "Methylphenidate", "Atomoxetine", "Guanfacine"], "a": "Lisdexamfetamine"},
    {"q": "Which drug should avoid late evening doses and can be opened into soft food?", "choices": ["Methylphenidate", "Atomoxetine", "Guanfacine", "Levothyroxine"], "a": "Methylphenidate"},
]

WEEK_5_QUESTIONS = [
    {"q": "Which drug is an anticholinergic used for parkinsonism and extrapyramidal symptoms?", "choices": ["Benztropine", "Donepezil", "Memantine", "Ropinirole"], "a": "Benztropine"},
    {"q": "Which drug has Sinemet as a brand name?", "choices": ["Carbidopa/Levodopa", "Ropinirole", "Benztropine", "Donepezil"], "a": "Carbidopa/Levodopa"},
    {"q": "Which drug is a central cholinesterase inhibitor used in Alzheimer disease?", "choices": ["Donepezil", "Memantine", "Melatonin", "Modafinil"], "a": "Donepezil"},
    {"q": "Which herbal product should be discontinued before surgery and dental procedures?", "choices": ["Ginkgo biloba", "Melatonin", "St. John's Wort", "Echinacea"], "a": "Ginkgo biloba"},
    {"q": "Which drug has Antivert as a brand name?", "choices": ["Meclizine", "Melatonin", "Modafinil", "Zolpidem"], "a": "Meclizine"},
    {"q": "Which supplement is commonly used 3 to 6 hours before sleep for insomnia?", "choices": ["Melatonin", "Meclizine", "Modafinil", "Memantine"], "a": "Melatonin"},
    {"q": "Which drug has Namenda as a brand name?", "choices": ["Memantine", "Donepezil", "Modafinil", "Benztropine"], "a": "Memantine"},
    {"q": "Which drug has Provigil as a brand name?", "choices": ["Modafinil", "Zolpidem", "Ropinirole", "Melatonin"], "a": "Modafinil"},
    {"q": "Which drug is a dopamine agonist used for Parkinson disease and restless leg syndrome?", "choices": ["Ropinirole", "Benztropine", "Donepezil", "Carbidopa/Levodopa"], "a": "Ropinirole"},
    {"q": "Which drug has Ambien as a brand name?", "choices": ["Zolpidem", "Modafinil", "Melatonin", "Meclizine"], "a": "Zolpidem"},
    {"q": "Which drug has a boxed warning for complex sleep behaviors?", "choices": ["Zolpidem", "Modafinil", "Melatonin", "Donepezil"], "a": "Zolpidem"},
    {"q": "Which drug should be taken on an empty stomach before bedtime and avoided with alcohol?", "choices": ["Zolpidem", "Melatonin", "Meclizine", "Ropinirole"], "a": "Zolpidem"},
]

WEEK_6_QUESTIONS = [
    {"q": "Which antidepressant is a tricyclic antidepressant?", "choices": ["Amitriptyline", "Duloxetine", "Escitalopram", "Sertraline"], "a": "Amitriptyline"},
    {"q": "Which drug has Abilify as a brand name?", "choices": ["Aripiprazole", "Olanzapine", "Risperidone", "Trazodone"], "a": "Aripiprazole"},
    {"q": "Which drug is an SNRI used for anxiety, depression, and diabetic neuropathy?", "choices": ["Duloxetine", "Escitalopram", "Fluoxetine", "Mirtazapine"], "a": "Duloxetine"},
    {"q": "Which drug has Lexapro as a brand name?", "choices": ["Escitalopram", "Fluoxetine", "Sertraline", "Trazodone"], "a": "Escitalopram"},
    {"q": "Which SSRI has Prozac as a brand name?", "choices": ["Fluoxetine", "Escitalopram", "Sertraline", "Vilazodone"], "a": "Fluoxetine"},
    {"q": "Which antidepressant commonly causes increased appetite and weight gain?", "choices": ["Mirtazapine", "Fluoxetine", "Escitalopram", "Sertraline"], "a": "Mirtazapine"},
    {"q": "Which drug has Zyprexa as a brand name?", "choices": ["Olanzapine", "Aripiprazole", "Risperidone", "Trazodone"], "a": "Olanzapine"},
    {"q": "Which antipsychotic is a benzisoxazole derivative?", "choices": ["Risperidone", "Olanzapine", "Aripiprazole", "Mirtazapine"], "a": "Risperidone"},
    {"q": "Which SSRI has Zoloft as a brand name?", "choices": ["Sertraline", "Fluoxetine", "Escitalopram", "Trazodone"], "a": "Sertraline"},
    {"q": "Which antidepressant is associated with priapism counseling?", "choices": ["Trazodone", "Mirtazapine", "Fluoxetine", "Duloxetine"], "a": "Trazodone"},
    {"q": "Which drug has a boxed warning for mortality in elderly patients with dementia-related psychosis?", "choices": ["Olanzapine", "Aripiprazole", "Risperidone", "All of the above"], "a": "All of the above"},
    {"q": "Which antidepressant should usually be taken in the morning?", "choices": ["Fluoxetine", "Mirtazapine", "Trazodone", "Amitriptyline"], "a": "Fluoxetine"},
]

WEEK_7_QUESTIONS = [
    {"q": "Which benzodiazepine has Xanax as a brand name?", "choices": ["Alprazolam", "Clonazepam", "Lorazepam", "Buspirone"], "a": "Alprazolam"},
    {"q": "Which drug is a serotonin 5-HT1A partial agonist used for anxiety?", "choices": ["Buspirone", "Alprazolam", "Clonazepam", "Lorazepam"], "a": "Buspirone"},
    {"q": "Which anticonvulsant has Tegretol as a brand name?", "choices": ["Carbamazepine", "Lamotrigine", "Levetiracetam", "Phenytoin"], "a": "Carbamazepine"},
    {"q": "Which anticonvulsant has a boxed warning for agranulocytosis and aplastic anemia?", "choices": ["Carbamazepine", "Lamotrigine", "Levetiracetam", "Oxcarbazepine"], "a": "Carbamazepine"},
    {"q": "Which benzodiazepine has Klonopin as a brand name?", "choices": ["Clonazepam", "Alprazolam", "Lorazepam", "Buspirone"], "a": "Clonazepam"},
    {"q": "Which anticonvulsant has a boxed warning for serious skin reactions?", "choices": ["Lamotrigine", "Carbamazepine", "Phenytoin", "Levetiracetam"], "a": "Lamotrigine"},
    {"q": "Which anticonvulsant has Keppra as a brand name?", "choices": ["Levetiracetam", "Lamotrigine", "Phenytoin", "Oxcarbazepine"], "a": "Levetiracetam"},
    {"q": "Which benzodiazepine has Ativan as a brand name?", "choices": ["Lorazepam", "Clonazepam", "Alprazolam", "Buspirone"], "a": "Lorazepam"},
    {"q": "Which anticonvulsant has Trileptal as a brand name?", "choices": ["Oxcarbazepine", "Phenytoin", "Lamotrigine", "Carbamazepine"], "a": "Oxcarbazepine"},
    {"q": "Which anticonvulsant has Dilantin as a brand name?", "choices": ["Phenytoin", "Levetiracetam", "Lamotrigine", "Oxcarbazepine"], "a": "Phenytoin"},
    {"q": "Which herbal product is associated with photosensitivity and many drug interactions?", "choices": ["St. John's Wort", "Ginkgo biloba", "Melatonin", "Echinacea"], "a": "St. John's Wort"},
    {"q": "Which antidepressant is an SSRI/5-HT1A partial agonist?", "choices": ["Vilazodone", "Sertraline", "Fluoxetine", "Escitalopram"], "a": "Vilazodone"},
]

WEEK_8_QUESTIONS = [
    {"q": "Which drug has Suboxone as a brand name?", "choices": ["Buprenorphine/Naloxone", "Naloxone", "Bupropion", "Varenicline"], "a": "Buprenorphine/Naloxone"},
    {"q": "Which drug is used for opioid use disorder and is a partial agonist/antagonist combination?", "choices": ["Buprenorphine/Naloxone", "Naloxone", "Gabapentin", "Lithium"], "a": "Buprenorphine/Naloxone"},
    {"q": "Which antidepressant also helps with smoking cessation?", "choices": ["Bupropion", "Duloxetine", "Sertraline", "Vilazodone"], "a": "Bupropion"},
    {"q": "Which drug has a boxed warning for hepatotoxicity, pancreatitis, and teratogenicity?", "choices": ["Divalproex", "Lithium", "Gabapentin", "Topiramate"], "a": "Divalproex"},
    {"q": "Which drug has Neurontin as a brand name?", "choices": ["Gabapentin", "Pregabalin", "Topiramate", "Naloxone"], "a": "Gabapentin"},
    {"q": "Which drug has Lithobid as a brand name?", "choices": ["Lithium", "Divalproex", "Bupropion", "Gabapentin"], "a": "Lithium"},
    {"q": "Which drug requires lithium level monitoring?", "choices": ["Lithium", "Topiramate", "Pregabalin", "Bupropion"], "a": "Lithium"},
    {"q": "Which drug has Narcan as a brand name?", "choices": ["Naloxone", "Nicotine", "Buprenorphine/Naloxone", "Sumatriptan"], "a": "Naloxone"},
    {"q": "Which drug immediately reverses opioid overdose?", "choices": ["Naloxone", "Buprenorphine/Naloxone", "Gabapentin", "Lithium"], "a": "Naloxone"},
    {"q": "Which smoking cessation aid includes Nicorette and Nicoderm CQ?", "choices": ["Nicotine", "Varenicline", "Bupropion", "Naloxone"], "a": "Nicotine"},
    {"q": "Which drug has Lyrica as a brand name?", "choices": ["Pregabalin", "Gabapentin", "Topiramate", "Divalproex"], "a": "Pregabalin"},
    {"q": "Which antimigraine serotonin receptor agonist has Imitrex as a brand name?", "choices": ["Sumatriptan", "Topiramate", "Divalproex", "Pregabalin"], "a": "Sumatriptan"},
    {"q": "Which anticonvulsant has Topamax as a brand name?", "choices": ["Topiramate", "Divalproex", "Gabapentin", "Pregabalin"], "a": "Topiramate"},
    {"q": "Which smoking cessation partial nicotine agonist has Chantix as a brand name?", "choices": ["Varenicline", "Nicotine", "Bupropion", "Naloxone"], "a": "Varenicline"},
]

QUESTION_BANK = {
    "All Weeks": (
        WEEK_1_QUESTIONS
        + WEEK_2_QUESTIONS
        + WEEK_3_QUESTIONS
        + WEEK_4_QUESTIONS
        + WEEK_5_QUESTIONS
        + WEEK_6_QUESTIONS
        + WEEK_7_QUESTIONS
        + WEEK_8_QUESTIONS
    ),
    "Week 1": WEEK_1_QUESTIONS,
    "Week 2": WEEK_2_QUESTIONS,
    "Week 3": WEEK_3_QUESTIONS,
    "Week 4": WEEK_4_QUESTIONS,
    "Week 5": WEEK_5_QUESTIONS,
    "Week 6": WEEK_6_QUESTIONS,
    "Week 7": WEEK_7_QUESTIONS,
    "Week 8": WEEK_8_QUESTIONS,
}

# ---------- Helpers ----------
def build_game_questions(selected_week="All Weeks", num_questions=15):
    pool = [dict(q) for q in QUESTION_BANK[selected_week]]
    random.shuffle(pool)
    selected = pool[:min(num_questions, len(pool))]

    for q in selected:
        random.shuffle(q["choices"])

    return selected

def reset_room_state(room_ref, selected_week, game_mode):
    room_ref.update({
        "score1": 0,
        "score2": 0,
        "current_question": 0,
        "buzzer": "",
        "steal_turn": "",
        "turn_deadline": 0,
        "winner_recorded": False,
        "feedback": "",
        "rope_position": 0,
        "selected_week": selected_week,
        "game_mode": game_mode,
        "questions": build_game_questions(selected_week)
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

def render_choice_grid(current_question, q_index, player_role, room_ref, room_data, name, is_steal=False, solo_mode=False):
    cols = st.columns(2)

    for i, choice in enumerate(current_question["choices"]):
        col = cols[i % 2]

        with col:
            button_key = f"{'solo' if solo_mode else ('steal' if is_steal else 'buzz')}_{q_index}_{i}"
            if st.button(choice, key=button_key, use_container_width=True):
                if choice.lower() == current_question["a"].lower():
                    if solo_mode:
                        room_ref.update({
                            "score1": room_data.get("score1", 0) + 1,
                            "current_question": q_index + 1,
                            "feedback": f"{name} got it correct! ✅"
                        })
                    else:
                        if player_role == "player1":
                            room_ref.update({
                                "score1": room_data.get("score1", 0) + 1,
                                "current_question": q_index + 1,
                                "buzzer": "",
                                "steal_turn": "",
                                "turn_deadline": 0,
                                "feedback": f"{name} got it correct! ✅",
                                "rope_position": room_data.get("rope_position", 0) - 1
                            })
                        else:
                            room_ref.update({
                                "score2": room_data.get("score2", 0) + 1,
                                "current_question": q_index + 1,
                                "buzzer": "",
                                "steal_turn": "",
                                "turn_deadline": 0,
                                "feedback": f"{name} got it correct! ✅",
                                "rope_position": room_data.get("rope_position", 0) + 1
                            })
                else:
                    if solo_mode:
                        room_ref.update({
                            "current_question": q_index + 1,
                            "feedback": random.choice(WRONG_MESSAGES)
                        })
                    elif is_steal:
                        room_ref.update({
                            "current_question": q_index + 1,
                            "buzzer": "",
                            "steal_turn": "",
                            "turn_deadline": 0,
                            "feedback": random.choice(WRONG_MESSAGES)
                        })
                    else:
                        room_ref.update({
                            "steal_turn": other_player(player_role),
                            "turn_deadline": time.time() + 7,
                            "feedback": random.choice(WRONG_MESSAGES)
                        })

                st.rerun()

# ---------- Pretty Leaderboard ----------
st.subheader("🏆 Leaderboard")
leaderboard = get_leaderboard()

if leaderboard:
    total_players = len(leaderboard)
    total_wins = sum(player["wins"] for player in leaderboard)

    col1, col2 = st.columns(2)
    col1.metric("Players", total_players)
    col2.metric("Total Wins", total_wins)

    medals = ["🥇", "🥈", "🥉"]

    for i, player in enumerate(leaderboard[:3]):
        st.markdown(
            f"""
            <div style="
                padding:12px 16px;
                margin-bottom:10px;
                border-radius:14px;
                background: linear-gradient(90deg, #111827, #1f2937);
                color:white;
                display:flex;
                justify-content:space-between;
                align-items:center;
            ">
                <div style="font-size:20px;">
                    {medals[i]} <b>{player['name']}</b>
                </div>
                <div style="font-size:18px;">
                    {player['wins']} wins
                </div>
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
selected_week_label = st.selectbox("Choose a week", list(WEEK_OPTIONS.keys()))
selected_week = WEEK_OPTIONS[selected_week_label]
game_mode = st.selectbox("Mode", ["Battle Mode", "Solo Practice"])
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
                "rope_position": 0,
                "selected_week": selected_week,
                "game_mode": game_mode,
                "questions": build_game_questions(selected_week)
            })
            st.success(f"{name} joined {room} as Player 1")
            st.rerun()

        else:
            player1 = room_data.get("player1", "")
            player2 = room_data.get("player2", "")

            if player1 == name or player2 == name:
                st.success(f"{name} rejoined {room}")
            elif room_data.get("game_mode") == "Solo Practice":
                st.error("Solo Practice is for one player only.")
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
    current_mode = room_data.get("game_mode", "Battle Mode")

    if current_mode == "Battle Mode":
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
                    "turn_deadline": time.time() + 7,
                    "feedback": "⚡ Steal opportunity!"
                })
                st.rerun()

    room_data = room_ref.get()
    buzzer = room_data.get("buzzer", "")
    steal_turn = room_data.get("steal_turn", "")
    deadline = room_data.get("turn_deadline", 0)
    current_mode = room_data.get("game_mode", "Battle Mode")

    st.subheader(f"Room: {room}")
    st.write("Mode:", current_mode)
    st.write("Week:", WEEK_DISPLAY.get(room_data.get("selected_week", "All Weeks"), "All Weeks — Mixed Review"))
    st.write("Player 1:", room_data.get("player1", ""))
    if current_mode == "Battle Mode":
        st.write("Player 2:", room_data.get("player2", ""))
    st.write("Score 1:", room_data.get("score1", 0))
    if current_mode == "Battle Mode":
        st.write("Score 2:", room_data.get("score2", 0))

    if current_mode == "Battle Mode":
        rope_position = room_data.get("rope_position", 0)
        rope_position = max(-5, min(5, rope_position))
        rope_percent = ((rope_position + 5) / 10) * 100

        st.write("### Tug of War")
        st.markdown(
            f"""
            <div style="display:flex; justify-content:space-between; font-weight:600; margin-bottom:6px;">
                <span>🟦 {room_data.get('player1', 'Player 1')}</span>
                <span>{room_data.get('player2', 'Player 2')} 🟥</span>
            </div>

            <div style="
                width:100%;
                height:28px;
                background:#e5e7eb;
                border-radius:14px;
                position:relative;
                overflow:hidden;
                margin-bottom:10px;
            ">
                <div style="
                    position:absolute;
                    left:{rope_percent}%;
                    top:0;
                    transform:translateX(-50%);
                    font-size:22px;
                    line-height:28px;
                ">🪢</div>
            </div>
            """,
            unsafe_allow_html=True
        )

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

        if current_mode == "Solo Practice":
            st.success(f"Practice complete. Final score: {p1}/{len(questions)}")
        else:
            rope_position = room_data.get("rope_position", 0)

            if rope_position <= -5:
                winner_name = room_data.get("player1", "Player 1")
                if not room_data.get("winner_recorded", False):
                    record_win(winner_name)
                    room_ref.update({"winner_recorded": True})
                st.balloons()
                st.success(f"🏆 {winner_name} wins the tug of war!")
                st.markdown("### 🟦🪢💥 🟥 dropped the rope!")
            elif rope_position >= 5:
                winner_name = room_data.get("player2", "Player 2")
                if not room_data.get("winner_recorded", False):
                    record_win(winner_name)
                    room_ref.update({"winner_recorded": True})
                st.balloons()
                st.success(f"🏆 {winner_name} wins the tug of war!")
                st.markdown("### 🟥🪢💥 🟦 dropped the rope!")
            elif p1 > p2:
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

    if current_mode == "Battle Mode":
        if buzzer:
            st.write(f"⚡ {get_player_name(room_data, buzzer)} buzzed!")
        else:
            st.write("Buzzer: None")

        if steal_turn:
            st.write("Steal Turn:", player_label(steal_turn))

        if deadline and current_question and (buzzer or steal_turn):
            time_left = max(0, deadline - time.time())
            seconds_left = max(0, int(time_left) + (1 if time_left > 0 else 0))
            progress_value = min(1.0, max(0.0, time_left / 7))
            st.caption(f"⏱️ {seconds_left}s remaining")
            st.progress(progress_value)

    if current_question:
        if current_mode == "Solo Practice":
            render_choice_grid(current_question, q_index, "player1", room_ref, room_data, name, solo_mode=True)

        else:
            if buzzer == "" and steal_turn == "":
                if st.button("🔴 Buzz"):
                    if player_role:
                        room_ref.update({
                            "buzzer": player_role,
                            "turn_deadline": time.time() + 7,
                            "feedback": ""
                        })
                        st.rerun()

            elif steal_turn:
                if player_role == steal_turn:
                    st.warning("Steal chance! Pick an answer in 7 seconds.")
                    render_choice_grid(current_question, q_index, player_role, room_ref, room_data, name, is_steal=True)
                else:
                    st.warning("Other player is attempting the steal.")

            else:
                if player_role == buzzer:
                    st.success("You buzzed first! Pick an answer in 7 seconds.")
                    render_choice_grid(current_question, q_index, player_role, room_ref, room_data, name, is_steal=False)
                else:
                    st.warning("Other player buzzed first.")

    col1, col2 = st.columns(2)

    with col1:
        if current_mode == "Battle Mode":
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
            reset_room_state(
                room_ref,
                room_data.get("selected_week", "All Weeks"),
                room_data.get("game_mode", "Battle Mode")
            )
            st.session_state.room_code = generate_room_code()
            st.rerun()

else:
    st.info("Join or create a room to start playing.")

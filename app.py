# print(flask.__version__)
# print(pickle.format_version)

from sklearn.linear_model import LogisticRegression
import pandas as pd
from statistics import mean
from sklearn.model_selection import cross_val_score
from bs4 import BeautifulSoup
from googlesearch import search
import re
import warnings

warnings.filterwarnings("ignore")
from flask import Flask, request, render_template, flash
import requests
from io import StringIO


output = StringIO

app = Flask(__name__)
app.secret_key = "it is a secret"

df = pd.read_csv("Dataset.csv")

Symptoms = []
output = []

features = [
    "itching",
    "skin_rash",
    "nodal_skin_eruptions",
    "continuous_sneezing",
    "shivering",
    "chills",
    "joint_pain",
    "stomach_pain",
    "acidity",
    "ulcers_on_tongue",
    "muscle_wasting",
    "vomiting",
    "burning_micturition",
    "spotting_ urination",
    "fatigue",
    "weight_gain",
    "anxiety",
    "cold_hands_and_feets",
    "mood_swings",
    "weight_loss",
    "restlessness",
    "lethargy",
    "patches_in_throat",
    "irregular_sugar_level",
    "cough",
    "high_fever",
    "sunken_eyes",
    "breathlessness",
    "sweating",
    "dehydration",
    "indigestion",
    "headache",
    "yellowish_skin",
    "dark_urine",
    "nausea",
    "loss_of_appetite",
    "pain_behind_the_eyes",
    "back_pain",
    "constipation",
    "abdominal_pain",
    "diarrhoea",
    "mild_fever",
    "yellow_urine",
    "yellowing_of_eyes",
    "acute_liver_failure",
    "fluid_overload",
    "swelling_of_stomach",
    "swelled_lymph_nodes",
    "malaise",
    "blurred_and_distorted_vision",
    "phlegm",
    "throat_irritation",
    "redness_of_eyes",
    "sinus_pressure",
    "runny_nose",
    "congestion",
    "chest_pain",
    "weakness_in_limbs",
    "fast_heart_rate",
    "pain_during_bowel_movements",
    "pain_in_anal_region",
    "bloody_stool",
    "irritation_in_anus",
    "neck_pain",
    "dizziness",
    "cramps",
    "bruising",
    "obesity",
    "swollen_legs",
    "swollen_blood_vessels",
    "puffy_face_and_eyes",
    "enlarged_thyroid",
    "brittle_nails",
    "swollen_extremeties",
    "excessive_hunger",
    "extra_marital_contacts",
    "drying_and_tingling_lips",
    "slurred_speech",
    "knee_pain",
    "hip_joint_pain",
    "muscle_weakness",
    "stiff_neck",
    "swelling_joints",
    "movement_stiffness",
    "spinning_movements",
    "loss_of_balance",
    "unsteadiness",
    "weakness_of_one_body_side",
    "loss_of_smell",
    "bladder_discomfort",
    "foul_smell_of urine",
    "continuous_feel_of_urine",
    "passage_of_gases",
    "internal_itching",
    "toxic_look_(typhos)",
    "depression",
    "irritability",
    "muscle_pain",
    "altered_sensorium",
    "red_spots_over_body",
    "belly_pain",
    "abnormal_menstruation",
    "dischromic _patches",
    "watering_from_eyes",
    "increased_appetite",
    "polyuria",
    "family_history",
    "mucoid_sputum",
    "rusty_sputum",
    "lack_of_concentration",
    "visual_disturbances",
    "receiving_blood_transfusion",
    "receiving_unsterile_injections",
    "coma",
    "stomach_bleeding",
    "distention_of_abdomen",
    "history_of_alcohol_consumption",
    "fluid_overload",
    "blood_in_sputum",
    "prominent_veins_on_calf",
    "palpitations",
    "painful_walking",
    "pus_filled_pimples",
    "blackheads",
    "scurring",
    "skin_peeling",
    "silver_like_dusting",
    "small_dents_in_nails",
    "inflammatory_nails",
    "blister",
    "red_sore_around_nose",
    "yellow_crust_ooze",
]

disease = [
    "Fungal infection",
    "Allergy",
    "GERD",
    "Chronic cholestasis",
    "Drug Reaction",
    "Peptic ulcer diseae",
    "AIDS",
    "Diabetes",
    "Gastroenteritis",
    "Bronchial Asthma",
    "Hypertension",
    " Migraine",
    "Cervical spondylosis",
    "Paralysis (brain hemorrhage)",
    "Jaundice",
    "Malaria",
    "Chicken pox",
    "Dengue",
    "Typhoid",
    "hepatitis A",
    "Hepatitis B",
    "Hepatitis C",
    "Hepatitis D",
    "Hepatitis E",
    "Alcoholic hepatitis",
    "Tuberculosis",
    "Common Cold",
    "Pneumonia",
    "Dimorphic hemmorhoids(piles)",
    "Heartattack",
    "Varicoseveins",
    "Hypothyroidism",
    "Hyperthyroidism",
    "Hypoglycemia",
    "Osteoarthristis",
    "Arthritis",
    "(vertigo) Paroymsal  Positional Vertigo",
    "Acne",
    "Urinary tract infection",
    "Psoriasis",
    "Impetigo",
]

sample_x = [0 for x in range(0, len(features))]

X = df[features]
Y = df[["prognosis"]]

lr = LogisticRegression()
lr = lr.fit(X, Y)
scores = cross_val_score(lr, X, Y, cv=5)


def diseaseDetail(term):
    diseases = [term]
    ret = term + "\n"
    for dis in diseases:
        # search "disease wilipedia" on google
        query = dis + " wikipedia"
        for sr in search(query, tld="co.in", stop=10, pause=0.5):
            # open wikipedia link
            match = re.search(r"wikipedia", sr)
            filled = 0
            if match:
                wiki = requests.get(sr, verify=False)
                soup = BeautifulSoup(wiki.content, "html5lib")
                # Fetch HTML code for 'infobox'
                info_table = soup.find("table", {"class": "infobox"})
                if info_table is not None:
                    # Preprocess contents of infobox
                    for row in info_table.find_all("tr"):
                        data = row.find("th", {"scope": "row"})
                        if data is not None:
                            symptom = str(row.find("td"))
                            symptom = symptom.replace(".", "")
                            symptom = symptom.replace(";", ",")
                            symptom = symptom.replace("<b>", "<b> \n")
                            symptom = re.sub(r"<a.*?>", "", symptom)  # Remove hyperlink
                            symptom = re.sub(r"</a>", "", symptom)  # Remove hyperlink
                            symptom = re.sub(r"<[^<]+?>", " ", symptom)  # All the tags
                            symptom = re.sub(
                                r"\[.*\]", "", symptom
                            )  # Remove citation text
                            symptom = symptom.replace("&gt", ">")
                            ret += data.get_text() + " - " + symptom + "\n"
                            #                            print(data.get_text(),"-",symptom)
                            filled = 1
                if filled:
                    break
    return ret


@app.route("/")
def home():
    redirect("redirect.html")
    return render_template("index.html")


@app.route("/number", methods=["POST"])
def number():
    Num = []
    Num = request.form["scc"]
    if Num == "1":
        return render_template("symp1.html")
    if Num == "2":
        return render_template("symp2.html")
    if Num == "3":
        return render_template("symp3.html")
    if Num == "4":
        return render_template("symp4.html")
    if Num == "5":
        return render_template("symp5.html")
    if Num == "6":
        return render_template("symp6.html")
    if Num == "7":
        return render_template("symp7.html")
    if Num == "8":
        return render_template("symp8.html")
    if Num == "9":
        return render_template("symp9.html")
    if Num == "10":
        return render_template("symp10.html")
    if request.form["scc"] != "secret":
        flash("Please Select A Number in Range (1-10)")
        return render_template("index.html")


@app.route("/treatment", methods=["POST"])
def treatment():
    selected = request.form["trt"]
    if selected != "-1":
        dis = diseases[topk_index_mapping[int(selected)]]
        out = diseaseDetail(dis)
        return render_template("treatment.html", text="{}".format(out))


@app.route("/symp1", methods=["POST"])
def symp1():
    global sample_x
    value1 = request.form["symptom-1"]
    Symptoms.append(value1)
    s1 = Symptoms[0]
    a = "\n list of Symptoms Selected:"

    if ("None") in Symptoms:
        Symptoms.remove(value1)
        return render_template("symp1.html", alert="Please Enter A Valid Symptoms")

    X = df[features]
    Y = df[["prognosis"]]

    lr = LogisticRegression()
    lr = lr.fit(X, Y)

    for k in range(0, len(features)):
        for val in Symptoms:
            if val == features[k]:
                sample_x[k] = 1
    print(Symptoms)
    print(sample_x)
    del k
    del val

    prediction = lr.predict_proba([sample_x])

    k = 10
    global diseases
    diseases = list(set(Y["prognosis"]))
    diseases.sort()
    topk = prediction[0].argsort()[-k:][::-1]

    tt = f"\nTop {k} diseases predicted based on symptoms"
    topk_dict = {}
    # Show top 10 highly probable disease to the user.
    for idx, t in enumerate(topk):
        match_sym = set()
        row = df.loc[df["prognosis"] == diseases[t]].values.tolist()
        row[0].pop(0)

        for idx, val in enumerate(row[0]):
            if val != 0:
                match_sym.add(features[idx])
        prob = (len(match_sym.intersection(set(Symptoms))) + 1) / (
            len(set(Symptoms)) + 1
        )
        prob *= mean(scores)
        topk_dict[t] = prob
    j = 0
    global topk_index_mapping
    topk_index_mapping = {}
    topk_sorted = dict(sorted(topk_dict.items(), key=lambda kv: kv[1], reverse=True))
    for key in topk_sorted:
        prob = topk_sorted[key] * 100
        print(
            str(j) + " Disease name:",
            diseases[key],
            "\tProbability:",
            str(round(prob, 2)) + "%",
        )
        out = (
            str(j) + " : Disease name:",
            diseases[key],
            "Probability:",
            str(round(prob, 2)) + "%",
        )
        output.append(out)
        topk_index_mapping[j] = key
        j += 1

    Symptoms.remove(value1)
    d0 = output[0]
    d1 = output[1]
    d2 = output[2]
    d3 = output[3]
    d4 = output[4]
    d5 = output[5]
    d6 = output[6]
    d7 = output[7]
    d8 = output[8]
    d9 = output[9]
    output.clear()
    sample_x = [0 for x in range(0, len(features))]
    return render_template(
        "result.html",
        text="{}".format(a),
        texts1="1.{}".format(s1),
        text2="{}".format(tt),
        text3="{}".format(d0),
        text4="{}".format(d1),
        text5="{}".format(d2),
        text6="{}".format(d3),
        text7="{}".format(d4),
        text8="{}".format(d5),
        text9="{}".format(d6),
        text10="{}".format(d7),
        text11="{}".format(d8),
        text12="{}".format(d9),
    )


@app.route("/symp2", methods=["POST"])
def symp2():
    global sample_x
    value1 = request.form["symptom-1"]
    Symptoms.append(value1)
    value2 = request.form["symptom-2"]
    Symptoms.append(value2)
    s1 = Symptoms[0]
    s2 = Symptoms[1]
    a = "\n list of Symptoms Selected :"

    if ("None") in Symptoms:
        Symptoms.remove(value1)
        Symptoms.remove(value2)
        return render_template("symp2.html", alert="Please Enter All Valid 3 Symptoms")

    X = df[features]
    Y = df[["prognosis"]]

    lr = LogisticRegression()
    lr = lr.fit(X, Y)

    for k in range(0, len(features)):
        for val in Symptoms:
            if val == features[k]:
                sample_x[k] = 1
    print(Symptoms)
    print(sample_x)
    del k
    del val

    prediction = lr.predict_proba([sample_x])

    k = 10
    global diseases
    diseases = list(set(Y["prognosis"]))
    diseases.sort()
    topk = prediction[0].argsort()[-k:][::-1]

    tt = f"\nTop {k} diseases predicted based on symptoms"
    topk_dict = {}
    # Show top 10 highly probable disease to the user.
    for idx, t in enumerate(topk):
        match_sym = set()
        row = df.loc[df["prognosis"] == diseases[t]].values.tolist()
        row[0].pop(0)

        for idx, val in enumerate(row[0]):
            if val != 0:
                match_sym.add(features[idx])
        prob = (len(match_sym.intersection(set(Symptoms))) + 1) / (
            len(set(Symptoms)) + 1
        )
        prob *= mean(scores)
        topk_dict[t] = prob
    j = 0
    global topk_index_mapping
    topk_index_mapping = {}
    topk_sorted = dict(sorted(topk_dict.items(), key=lambda kv: kv[1], reverse=True))
    for key in topk_sorted:
        prob = topk_sorted[key] * 100
        print(
            str(j) + " Disease name:",
            diseases[key],
            "\tProbability:",
            str(round(prob, 2)) + "%",
        )
        out = (
            str(j) + " : Disease name:",
            diseases[key],
            "Probability:",
            str(round(prob, 2)) + "%",
        )
        output.append(out)
        topk_index_mapping[j] = key
        j += 1

    Symptoms.remove(value1)
    Symptoms.remove(value2)
    d0 = output[0]
    d1 = output[1]
    d2 = output[2]
    d3 = output[3]
    d4 = output[4]
    d5 = output[5]
    d6 = output[6]
    d7 = output[7]
    d8 = output[8]
    d9 = output[9]
    output.clear()
    sample_x = [0 for x in range(0, len(features))]
    return render_template(
        "result.html",
        text="{}".format(a),
        texts1="1.{}".format(s1),
        texts2="2.{}".format(s2),
        text2="{}".format(tt),
        text3="{}".format(d0),
        text4="{}".format(d1),
        text5="{}".format(d2),
        text6="{}".format(d3),
        text7="{}".format(d4),
        text8="{}".format(d5),
        text9="{}".format(d6),
        text10="{}".format(d7),
        text11="{}".format(d8),
        text12="{}".format(d9),
    )


@app.route("/symp3", methods=["POST"])
def symp3():
    global sample_x
    value1 = request.form["symptom-1"]
    Symptoms.append(value1)
    value2 = request.form["symptom-2"]
    Symptoms.append(value2)
    value3 = request.form["symptom-3"]
    Symptoms.append(value3)
    s1 = Symptoms[0]
    s2 = Symptoms[1]
    s3 = Symptoms[2]
    a = "\n list of Symptoms Selected :"

    if ("None") in Symptoms:
        Symptoms.remove(value1)
        Symptoms.remove(value2)
        Symptoms.remove(value3)
        return render_template("symp3.html", alert="Please Enter All Valid 3 Symptoms")

    X = df[features]
    Y = df[["prognosis"]]

    lr = LogisticRegression()
    lr = lr.fit(X, Y)

    for k in range(0, len(features)):
        for val in Symptoms:
            if val == features[k]:
                sample_x[k] = 1
    print(Symptoms)
    print(sample_x)
    del k
    del val

    prediction = lr.predict_proba([sample_x])

    k = 10
    global diseases
    diseases = list(set(Y["prognosis"]))
    diseases.sort()
    topk = prediction[0].argsort()[-k:][::-1]

    tt = f"\nTop {k} diseases predicted based on symptoms"
    topk_dict = {}
    # Show top 10 highly probable disease to the user.
    for idx, t in enumerate(topk):
        match_sym = set()
        row = df.loc[df["prognosis"] == diseases[t]].values.tolist()
        row[0].pop(0)

        for idx, val in enumerate(row[0]):
            if val != 0:
                match_sym.add(features[idx])
        prob = (len(match_sym.intersection(set(Symptoms))) + 1) / (
            len(set(Symptoms)) + 1
        )
        prob *= mean(scores)
        topk_dict[t] = prob
    j = 0
    global topk_index_mapping
    topk_index_mapping = {}
    topk_sorted = dict(sorted(topk_dict.items(), key=lambda kv: kv[1], reverse=True))
    for key in topk_sorted:
        prob = topk_sorted[key] * 100
        print(
            str(j) + " Disease name:",
            diseases[key],
            "\tProbability:",
            str(round(prob, 2)) + "%",
        )
        out = (
            str(j) + " : Disease name:",
            diseases[key],
            "Probability:",
            str(round(prob, 2)) + "%",
        )
        output.append(out)
        topk_index_mapping[j] = key
        j += 1

    Symptoms.remove(value1)
    Symptoms.remove(value2)
    Symptoms.remove(value3)
    d0 = output[0]
    d1 = output[1]
    d2 = output[2]
    d3 = output[3]
    d4 = output[4]
    d5 = output[5]
    d6 = output[6]
    d7 = output[7]
    d8 = output[8]
    d9 = output[9]
    output.clear()
    sample_x = [0 for x in range(0, len(features))]
    return render_template(
        "result.html",
        text="{}".format(a),
        texts1="1.{}".format(s1),
        texts2="2.{}".format(s2),
        texts3="3.{}".format(s3),
        text2="{}".format(tt),
        text3="{}".format(d0),
        text4="{}".format(d1),
        text5="{}".format(d2),
        text6="{}".format(d3),
        text7="{}".format(d4),
        text8="{}".format(d5),
        text9="{}".format(d6),
        text10="{}".format(d7),
        text11="{}".format(d8),
        text12="{}".format(d9),
    )


@app.route("/symp4", methods=["POST"])
def symp4():
    global sample_x
    value1 = request.form["symptom-1"]
    Symptoms.append(value1)
    value2 = request.form["symptom-2"]
    Symptoms.append(value2)
    value3 = request.form["symptom-3"]
    Symptoms.append(value3)
    value4 = request.form["symptom-4"]
    Symptoms.append(value4)
    s1 = Symptoms[0]
    s2 = Symptoms[1]
    s3 = Symptoms[2]
    s4 = Symptoms[3]
    a = "\n list of Symptoms Selected :"

    if ("None") in Symptoms:
        Symptoms.remove(value1)
        Symptoms.remove(value2)
        Symptoms.remove(value3)
        Symptoms.remove(value4)
        return render_template("symp4.html", alert="Please Enter All Valid 4 Symptoms")

    X = df[features]
    Y = df[["prognosis"]]

    lr = LogisticRegression()
    lr = lr.fit(X, Y)

    for k in range(0, len(features)):
        for val in Symptoms:
            if val == features[k]:
                sample_x[k] = 1
    print(Symptoms)
    print(sample_x)
    del k
    del val

    prediction = lr.predict_proba([sample_x])

    k = 10
    global diseases
    diseases = list(set(Y["prognosis"]))
    diseases.sort()
    topk = prediction[0].argsort()[-k:][::-1]

    tt = f"\nTop {k} diseases predicted based on symptoms"
    topk_dict = {}
    # Show top 10 highly probable disease to the user.
    for idx, t in enumerate(topk):
        match_sym = set()
        row = df.loc[df["prognosis"] == diseases[t]].values.tolist()
        row[0].pop(0)

        for idx, val in enumerate(row[0]):
            if val != 0:
                match_sym.add(features[idx])
        prob = (len(match_sym.intersection(set(Symptoms))) + 1) / (
            len(set(Symptoms)) + 1
        )
        prob *= mean(scores)
        topk_dict[t] = prob
    j = 0
    global topk_index_mapping
    topk_index_mapping = {}
    topk_sorted = dict(sorted(topk_dict.items(), key=lambda kv: kv[1], reverse=True))
    for key in topk_sorted:
        prob = topk_sorted[key] * 100
        print(
            str(j) + " Disease name:",
            diseases[key],
            "\tProbability:",
            str(round(prob, 2)) + "%",
        )
        out = (
            str(j) + " : Disease name:",
            diseases[key],
            "Probability:",
            str(round(prob, 2)) + "%",
        )
        output.append(out)
        topk_index_mapping[j] = key
        j += 1

    Symptoms.remove(value1)
    Symptoms.remove(value2)
    Symptoms.remove(value3)
    Symptoms.remove(value4)
    d0 = output[0]
    d1 = output[1]
    d2 = output[2]
    d3 = output[3]
    d4 = output[4]
    d5 = output[5]
    d6 = output[6]
    d7 = output[7]
    d8 = output[8]
    d9 = output[9]
    output.clear()
    sample_x = [0 for x in range(0, len(features))]
    return render_template(
        "result.html",
        text="{}".format(a),
        texts1="1.{}".format(s1),
        texts2="2.{}".format(s2),
        texts3="3.{}".format(s3),
        texts4="4.{}".format(s4),
        text2="{}".format(tt),
        text3="{}".format(d0),
        text4="{}".format(d1),
        text5="{}".format(d2),
        text6="{}".format(d3),
        text7="{}".format(d4),
        text8="{}".format(d5),
        text9="{}".format(d6),
        text10="{}".format(d7),
        text11="{}".format(d8),
        text12="{}".format(d9),
    )


@app.route("/symp5", methods=["POST"])
def symp5():
    global sample_x
    value1 = request.form["symptom-1"]
    Symptoms.append(value1)
    value2 = request.form["symptom-2"]
    Symptoms.append(value2)
    value3 = request.form["symptom-3"]
    Symptoms.append(value3)
    value4 = request.form["symptom-4"]
    Symptoms.append(value4)
    value5 = request.form["symptom-5"]
    Symptoms.append(value5)
    s1 = Symptoms[0]
    s2 = Symptoms[1]
    s3 = Symptoms[2]
    s4 = Symptoms[3]
    s5 = Symptoms[4]
    a = "\n list of Symptoms Selected :"

    if ("None") in Symptoms:
        Symptoms.remove(value1)
        Symptoms.remove(value2)
        Symptoms.remove(value3)
        Symptoms.remove(value4)
        Symptoms.remove(value5)
        return render_template("symp5.html", alert="Please Enter All Valid 5 Symptoms")

    X = df[features]
    Y = df[["prognosis"]]

    lr = LogisticRegression()
    lr = lr.fit(X, Y)

    for k in range(0, len(features)):
        for val in Symptoms:
            if val == features[k]:
                sample_x[k] = 1
    print(Symptoms)
    print(sample_x)
    del k
    del val

    prediction = lr.predict_proba([sample_x])

    k = 10
    global diseases
    diseases = list(set(Y["prognosis"]))
    diseases.sort()
    topk = prediction[0].argsort()[-k:][::-1]

    tt = f"\nTop {k} diseases predicted based on symptoms"
    topk_dict = {}
    # Show top 10 highly probable disease to the user.
    for idx, t in enumerate(topk):
        match_sym = set()
        row = df.loc[df["prognosis"] == diseases[t]].values.tolist()
        row[0].pop(0)

        for idx, val in enumerate(row[0]):
            if val != 0:
                match_sym.add(features[idx])
        prob = (len(match_sym.intersection(set(Symptoms))) + 1) / (
            len(set(Symptoms)) + 1
        )
        prob *= mean(scores)
        topk_dict[t] = prob
    j = 0
    global topk_index_mapping
    topk_index_mapping = {}
    topk_sorted = dict(sorted(topk_dict.items(), key=lambda kv: kv[1], reverse=True))
    for key in topk_sorted:
        prob = topk_sorted[key] * 100
        print(
            str(j) + " Disease name:",
            diseases[key],
            "\tProbability:",
            str(round(prob, 2)) + "%",
        )
        out = (
            str(j) + " : Disease name:",
            diseases[key],
            "Probability:",
            str(round(prob, 2)) + "%",
        )
        output.append(out)
        topk_index_mapping[j] = key
        j += 1

    Symptoms.remove(value1)
    Symptoms.remove(value2)
    Symptoms.remove(value3)
    Symptoms.remove(value4)
    Symptoms.remove(value5)
    d0 = output[0]
    d1 = output[1]
    d2 = output[2]
    d3 = output[3]
    d4 = output[4]
    d5 = output[5]
    d6 = output[6]
    d7 = output[7]
    d8 = output[8]
    d9 = output[9]
    output.clear()
    sample_x = [0 for x in range(0, len(features))]
    return render_template(
        "result.html",
        text="{}".format(a),
        texts1="1.{}".format(s1),
        texts2="2.{}".format(s2),
        texts3="3.{}".format(s3),
        texts4="4.{}".format(s4),
        texts5="5.{}".format(s5),
        text2="{}".format(tt),
        text3="{}".format(d0),
        text4="{}".format(d1),
        text5="{}".format(d2),
        text6="{}".format(d3),
        text7="{}".format(d4),
        text8="{}".format(d5),
        text9="{}".format(d6),
        text10="{}".format(d7),
        text11="{}".format(d8),
        text12="{}".format(d9),
    )


@app.route("/symp6", methods=["POST"])
def symp6():
    global sample_x
    value1 = request.form["symptom-1"]
    Symptoms.append(value1)
    value2 = request.form["symptom-2"]
    Symptoms.append(value2)
    value3 = request.form["symptom-3"]
    Symptoms.append(value3)
    value4 = request.form["symptom-4"]
    Symptoms.append(value4)
    value5 = request.form["symptom-5"]
    Symptoms.append(value5)
    value6 = request.form["symptom-6"]
    Symptoms.append(value6)
    s1 = Symptoms[0]
    s2 = Symptoms[1]
    s3 = Symptoms[2]
    s4 = Symptoms[3]
    s5 = Symptoms[4]
    s6 = Symptoms[5]
    a = "\n list of Symptoms Selected :"

    if ("None") in Symptoms:
        Symptoms.remove(value1)
        Symptoms.remove(value2)
        Symptoms.remove(value3)
        Symptoms.remove(value4)
        Symptoms.remove(value5)
        Symptoms.remove(value6)
        return render_template("symp6.html", alert="Please Enter All Valid 5 Symptoms")

    X = df[features]
    Y = df[["prognosis"]]

    lr = LogisticRegression()
    lr = lr.fit(X, Y)

    for k in range(0, len(features)):
        for val in Symptoms:
            if val == features[k]:
                sample_x[k] = 1
    print(Symptoms)
    print(sample_x)
    del k
    del val

    prediction = lr.predict_proba([sample_x])

    k = 10
    global diseases
    diseases = list(set(Y["prognosis"]))
    diseases.sort()
    topk = prediction[0].argsort()[-k:][::-1]

    tt = f"\nTop {k} diseases predicted based on symptoms"
    topk_dict = {}
    # Show top 10 highly probable disease to the user.
    for idx, t in enumerate(topk):
        match_sym = set()
        row = df.loc[df["prognosis"] == diseases[t]].values.tolist()
        row[0].pop(0)

        for idx, val in enumerate(row[0]):
            if val != 0:
                match_sym.add(features[idx])
        prob = (len(match_sym.intersection(set(Symptoms))) + 1) / (
            len(set(Symptoms)) + 1
        )
        prob *= mean(scores)
        topk_dict[t] = prob
    j = 0
    global topk_index_mapping
    topk_index_mapping = {}
    topk_sorted = dict(sorted(topk_dict.items(), key=lambda kv: kv[1], reverse=True))
    for key in topk_sorted:
        prob = topk_sorted[key] * 100
        print(
            str(j) + " Disease name:",
            diseases[key],
            "\tProbability:",
            str(round(prob, 2)) + "%",
        )
        out = (
            str(j) + " : Disease name:",
            diseases[key],
            "Probability:",
            str(round(prob, 2)) + "%",
        )
        output.append(out)
        topk_index_mapping[j] = key
        j += 1

    Symptoms.remove(value1)
    Symptoms.remove(value2)
    Symptoms.remove(value3)
    Symptoms.remove(value4)
    Symptoms.remove(value5)
    Symptoms.remove(value6)

    d0 = output[0]
    d1 = output[1]
    d2 = output[2]
    d3 = output[3]
    d4 = output[4]
    d5 = output[5]
    d6 = output[6]
    d7 = output[7]
    d8 = output[8]
    d9 = output[9]
    output.clear()
    sample_x = [0 for x in range(0, len(features))]
    return render_template(
        "result.html",
        text="{}".format(a),
        texts1="1.{}".format(s1),
        texts2="2.{}".format(s2),
        texts3="3.{}".format(s3),
        texts4="4.{}".format(s4),
        texts5="5.{}".format(s5),
        texts6="6.{}".format(s6),
        text2="{}".format(tt),
        text3="{}".format(d0),
        text4="{}".format(d1),
        text5="{}".format(d2),
        text6="{}".format(d3),
        text7="{}".format(d4),
        text8="{}".format(d5),
        text9="{}".format(d6),
        text10="{}".format(d7),
        text11="{}".format(d8),
        text12="{}".format(d9),
    )


@app.route("/symp7", methods=["POST"])
def symp7():
    global sample_x
    value1 = request.form["symptom-1"]
    Symptoms.append(value1)
    value2 = request.form["symptom-2"]
    Symptoms.append(value2)
    value3 = request.form["symptom-3"]
    Symptoms.append(value3)
    value4 = request.form["symptom-4"]
    Symptoms.append(value4)
    value5 = request.form["symptom-5"]
    Symptoms.append(value5)
    value6 = request.form["symptom-6"]
    Symptoms.append(value6)
    value7 = request.form["symptom-7"]
    Symptoms.append(value7)
    s1 = Symptoms[0]
    s2 = Symptoms[1]
    s3 = Symptoms[2]
    s4 = Symptoms[3]
    s5 = Symptoms[4]
    s6 = Symptoms[5]
    s7 = Symptoms[6]
    a = "\n list of Symptoms Selected :"

    if ("None") in Symptoms:
        Symptoms.remove(value1)
        Symptoms.remove(value2)
        Symptoms.remove(value3)
        Symptoms.remove(value4)
        Symptoms.remove(value5)
        Symptoms.remove(value6)
        Symptoms.remove(value7)
        return render_template("symp7.html", alert="Please Enter All Valid 5 Symptoms")

    X = df[features]
    Y = df[["prognosis"]]

    lr = LogisticRegression()
    lr = lr.fit(X, Y)

    for k in range(0, len(features)):
        for val in Symptoms:
            if val == features[k]:
                sample_x[k] = 1
    print(Symptoms)
    print(sample_x)
    del k
    del val

    prediction = lr.predict_proba([sample_x])

    k = 10
    global diseases
    diseases = list(set(Y["prognosis"]))
    diseases.sort()
    topk = prediction[0].argsort()[-k:][::-1]

    tt = f"\nTop {k} diseases predicted based on symptoms"
    topk_dict = {}
    # Show top 10 highly probable disease to the user.
    for idx, t in enumerate(topk):
        match_sym = set()
        row = df.loc[df["prognosis"] == diseases[t]].values.tolist()
        row[0].pop(0)

        for idx, val in enumerate(row[0]):
            if val != 0:
                match_sym.add(features[idx])
        prob = (len(match_sym.intersection(set(Symptoms))) + 1) / (
            len(set(Symptoms)) + 1
        )
        prob *= mean(scores)
        topk_dict[t] = prob
    j = 0
    global topk_index_mapping
    topk_index_mapping = {}
    topk_sorted = dict(sorted(topk_dict.items(), key=lambda kv: kv[1], reverse=True))
    for key in topk_sorted:
        prob = topk_sorted[key] * 100
        print(
            str(j) + " Disease name:",
            diseases[key],
            "\tProbability:",
            str(round(prob, 2)) + "%",
        )
        out = (
            str(j) + " : Disease name:",
            diseases[key],
            "Probability:",
            str(round(prob, 2)) + "%",
        )
        output.append(out)
        topk_index_mapping[j] = key
        j += 1

    Symptoms.remove(value1)
    Symptoms.remove(value2)
    Symptoms.remove(value3)
    Symptoms.remove(value4)
    Symptoms.remove(value5)
    Symptoms.remove(value6)
    Symptoms.remove(value7)

    d0 = output[0]
    d1 = output[1]
    d2 = output[2]
    d3 = output[3]
    d4 = output[4]
    d5 = output[5]
    d6 = output[6]
    d7 = output[7]
    d8 = output[8]
    d9 = output[9]
    output.clear()
    sample_x = [0 for x in range(0, len(features))]
    return render_template(
        "result.html",
        text="{}".format(a),
        texts1="1.{}".format(s1),
        texts2="2.{}".format(s2),
        texts3="3.{}".format(s3),
        texts4="4.{}".format(s4),
        texts5="5.{}".format(s5),
        texts6="6.{}".format(s6),
        texts7="7.{}".format(s7),
        text2="{}".format(tt),
        text3="{}".format(d0),
        text4="{}".format(d1),
        text5="{}".format(d2),
        text6="{}".format(d3),
        text7="{}".format(d4),
        text8="{}".format(d5),
        text9="{}".format(d6),
        text10="{}".format(d7),
        text11="{}".format(d8),
        text12="{}".format(d9),
    )


@app.route("/symp8", methods=["POST"])
def symp8():
    global sample_x
    value1 = request.form["symptom-1"]
    Symptoms.append(value1)
    value2 = request.form["symptom-2"]
    Symptoms.append(value2)
    value3 = request.form["symptom-3"]
    Symptoms.append(value3)
    value4 = request.form["symptom-4"]
    Symptoms.append(value4)
    value5 = request.form["symptom-5"]
    Symptoms.append(value5)
    value6 = request.form["symptom-6"]
    Symptoms.append(value6)
    value7 = request.form["symptom-7"]
    Symptoms.append(value7)
    value8 = request.form["symptom-8"]
    Symptoms.append(value8)
    s1 = Symptoms[0]
    s2 = Symptoms[1]
    s3 = Symptoms[2]
    s4 = Symptoms[3]
    s5 = Symptoms[4]
    s6 = Symptoms[5]
    s7 = Symptoms[6]
    s8 = Symptoms[7]
    a = "\n list of Symptoms Selected :"

    if ("None") in Symptoms:
        Symptoms.remove(value1)
        Symptoms.remove(value2)
        Symptoms.remove(value3)
        Symptoms.remove(value4)
        Symptoms.remove(value5)
        Symptoms.remove(value6)
        Symptoms.remove(value7)
        Symptoms.remove(value8)
        return render_template("symp8.html", alert="Please Enter All Valid 5 Symptoms")

    X = df[features]
    Y = df[["prognosis"]]

    lr = LogisticRegression()
    lr = lr.fit(X, Y)

    for k in range(0, len(features)):
        for val in Symptoms:
            if val == features[k]:
                sample_x[k] = 1
    print(Symptoms)
    print(sample_x)
    del k
    del val

    prediction = lr.predict_proba([sample_x])

    k = 10
    global diseases
    diseases = list(set(Y["prognosis"]))
    diseases.sort()
    topk = prediction[0].argsort()[-k:][::-1]

    tt = f"\nTop {k} diseases predicted based on symptoms"
    topk_dict = {}
    # Show top 10 highly probable disease to the user.
    for idx, t in enumerate(topk):
        match_sym = set()
        row = df.loc[df["prognosis"] == diseases[t]].values.tolist()
        row[0].pop(0)

        for idx, val in enumerate(row[0]):
            if val != 0:
                match_sym.add(features[idx])
        prob = (len(match_sym.intersection(set(Symptoms))) + 1) / (
            len(set(Symptoms)) + 1
        )
        prob *= mean(scores)
        topk_dict[t] = prob
    j = 0
    global topk_index_mapping
    topk_index_mapping = {}
    topk_sorted = dict(sorted(topk_dict.items(), key=lambda kv: kv[1], reverse=True))
    for key in topk_sorted:
        prob = topk_sorted[key] * 100
        print(
            str(j) + " Disease name:",
            diseases[key],
            "\tProbability:",
            str(round(prob, 2)) + "%",
        )
        out = (
            str(j) + " : Disease name:",
            diseases[key],
            "Probability:",
            str(round(prob, 2)) + "%",
        )
        output.append(out)
        topk_index_mapping[j] = key
        j += 1

    Symptoms.remove(value1)
    Symptoms.remove(value2)
    Symptoms.remove(value3)
    Symptoms.remove(value4)
    Symptoms.remove(value5)
    Symptoms.remove(value6)
    Symptoms.remove(value7)
    Symptoms.remove(value8)

    d0 = output[0]
    d1 = output[1]
    d2 = output[2]
    d3 = output[3]
    d4 = output[4]
    d5 = output[5]
    d6 = output[6]
    d7 = output[7]
    d8 = output[8]
    d9 = output[9]
    output.clear()
    sample_x = [0 for x in range(0, len(features))]
    return render_template(
        "result.html",
        text="{}".format(a),
        texts1="1.{}".format(s1),
        texts2="2.{}".format(s2),
        texts3="3.{}".format(s3),
        texts4="4.{}".format(s4),
        texts5="5.{}".format(s5),
        texts6="6.{}".format(s6),
        texts7="7.{}".format(s7),
        texts8="8.{}".format(s8),
        text2="{}".format(tt),
        text3="{}".format(d0),
        text4="{}".format(d1),
        text5="{}".format(d2),
        text6="{}".format(d3),
        text7="{}".format(d4),
        text8="{}".format(d5),
        text9="{}".format(d6),
        text10="{}".format(d7),
        text11="{}".format(d8),
        text12="{}".format(d9),
    )


@app.route("/symp9", methods=["POST"])
def symp9():
    global sample_x
    value1 = request.form["symptom-1"]
    Symptoms.append(value1)
    value2 = request.form["symptom-2"]
    Symptoms.append(value2)
    value3 = request.form["symptom-3"]
    Symptoms.append(value3)
    value4 = request.form["symptom-4"]
    Symptoms.append(value4)
    value5 = request.form["symptom-5"]
    Symptoms.append(value5)
    value6 = request.form["symptom-6"]
    Symptoms.append(value6)
    value7 = request.form["symptom-7"]
    Symptoms.append(value7)
    value8 = request.form["symptom-8"]
    Symptoms.append(value8)
    value9 = request.form["symptom-9"]
    Symptoms.append(value9)
    s1 = Symptoms[0]
    s2 = Symptoms[1]
    s3 = Symptoms[2]
    s4 = Symptoms[3]
    s5 = Symptoms[4]
    s6 = Symptoms[5]
    s7 = Symptoms[6]
    s8 = Symptoms[7]
    s9 = Symptoms[8]
    a = "\n list of Symptoms Selected :"

    if ("None") in Symptoms:
        Symptoms.remove(value1)
        Symptoms.remove(value2)
        Symptoms.remove(value3)
        Symptoms.remove(value4)
        Symptoms.remove(value5)
        Symptoms.remove(value6)
        Symptoms.remove(value7)
        Symptoms.remove(value8)
        Symptoms.remove(value9)
        return render_template("symp9.html", alert="Please Enter All Valid 5 Symptoms")

    X = df[features]
    Y = df[["prognosis"]]

    lr = LogisticRegression()
    lr = lr.fit(X, Y)

    for k in range(0, len(features)):
        for val in Symptoms:
            if val == features[k]:
                sample_x[k] = 1
    print(Symptoms)
    print(sample_x)
    del k
    del val

    prediction = lr.predict_proba([sample_x])

    k = 10
    global diseases
    diseases = list(set(Y["prognosis"]))
    diseases.sort()
    topk = prediction[0].argsort()[-k:][::-1]

    tt = f"\nTop {k} diseases predicted based on symptoms"
    topk_dict = {}
    # Show top 10 highly probable disease to the user.
    for idx, t in enumerate(topk):
        match_sym = set()
        row = df.loc[df["prognosis"] == diseases[t]].values.tolist()
        row[0].pop(0)

        for idx, val in enumerate(row[0]):
            if val != 0:
                match_sym.add(features[idx])
        prob = (len(match_sym.intersection(set(Symptoms))) + 1) / (
            len(set(Symptoms)) + 1
        )
        prob *= mean(scores)
        topk_dict[t] = prob
    j = 0
    global topk_index_mapping
    topk_index_mapping = {}
    topk_sorted = dict(sorted(topk_dict.items(), key=lambda kv: kv[1], reverse=True))
    for key in topk_sorted:
        prob = topk_sorted[key] * 100
        print(
            str(j) + " Disease name:",
            diseases[key],
            "\tProbability:",
            str(round(prob, 2)) + "%",
        )
        out = (
            str(j) + " : Disease name:",
            diseases[key],
            "Probability:",
            str(round(prob, 2)) + "%",
        )
        output.append(out)
        topk_index_mapping[j] = key
        j += 1

    Symptoms.remove(value1)
    Symptoms.remove(value2)
    Symptoms.remove(value3)
    Symptoms.remove(value4)
    Symptoms.remove(value5)
    Symptoms.remove(value6)
    Symptoms.remove(value7)
    Symptoms.remove(value8)
    Symptoms.remove(value9)

    d0 = output[0]
    d1 = output[1]
    d2 = output[2]
    d3 = output[3]
    d4 = output[4]
    d5 = output[5]
    d6 = output[6]
    d7 = output[7]
    d8 = output[8]
    d9 = output[9]
    output.clear()
    sample_x = [0 for x in range(0, len(features))]
    return render_template(
        "result.html",
        text="{}".format(a),
        texts1="1.{}".format(s1),
        texts2="2.{}".format(s2),
        texts3="3.{}".format(s3),
        texts4="4.{}".format(s4),
        texts5="5.{}".format(s5),
        texts6="6.{}".format(s6),
        texts7="7.{}".format(s7),
        texts8="8.{}".format(s8),
        texts9="9.{}".format(s9),
        text2="{}".format(tt),
        text3="{}".format(d0),
        text4="{}".format(d1),
        text5="{}".format(d2),
        text6="{}".format(d3),
        text7="{}".format(d4),
        text8="{}".format(d5),
        text9="{}".format(d6),
        text10="{}".format(d7),
        text11="{}".format(d8),
        text12="{}".format(d9),
    )


@app.route("/symp10", methods=["POST"])
def symp10():
    global sample_x
    value1 = request.form["symptom-1"]
    Symptoms.append(value1)
    value2 = request.form["symptom-2"]
    Symptoms.append(value2)
    value3 = request.form["symptom-3"]
    Symptoms.append(value3)
    value4 = request.form["symptom-4"]
    Symptoms.append(value4)
    value5 = request.form["symptom-5"]
    Symptoms.append(value5)
    value6 = request.form["symptom-6"]
    Symptoms.append(value6)
    value7 = request.form["symptom-7"]
    Symptoms.append(value7)
    value8 = request.form["symptom-8"]
    Symptoms.append(value8)
    value9 = request.form["symptom-9"]
    Symptoms.append(value9)
    value10 = request.form["symptom-10"]
    Symptoms.append(value10)

    s1 = Symptoms[0]
    s2 = Symptoms[1]
    s3 = Symptoms[2]
    s4 = Symptoms[3]
    s5 = Symptoms[4]
    s6 = Symptoms[5]
    s7 = Symptoms[6]
    s8 = Symptoms[7]
    s9 = Symptoms[8]
    s10 = Symptoms[9]
    a = "\n list of Symptoms Selected :"

    if ("None") in Symptoms:
        Symptoms.remove(value1)
        Symptoms.remove(value2)
        Symptoms.remove(value3)
        Symptoms.remove(value4)
        Symptoms.remove(value5)
        Symptoms.remove(value6)
        Symptoms.remove(value7)
        Symptoms.remove(value8)
        Symptoms.remove(value9)
        Symptoms.remove(value10)
        return render_template("symp10.html", alert="Please Enter All Valid 5 Symptoms")

    X = df[features]
    Y = df[["prognosis"]]

    lr = LogisticRegression()
    lr = lr.fit(X, Y)

    for k in range(0, len(features)):
        for val in Symptoms:
            if val == features[k]:
                sample_x[k] = 1
    print(Symptoms)
    print(sample_x)

    prediction = lr.predict_proba([sample_x])

    k = 10
    global diseases
    diseases = list(set(Y["prognosis"]))
    diseases.sort()
    topk = prediction[0].argsort()[-k:][::-1]

    tt = f"\nTop {k} diseases predicted based on symptoms"
    topk_dict = {}
    # Show top 10 highly probable disease to the user.
    for idx, t in enumerate(topk):
        match_sym = set()
        row = df.loc[df["prognosis"] == diseases[t]].values.tolist()
        row[0].pop(0)

        for idx, val in enumerate(row[0]):
            if val != 0:
                match_sym.add(features[idx])
        prob = (len(match_sym.intersection(set(Symptoms))) + 1) / (
            len(set(Symptoms)) + 1
        )
        prob *= mean(scores)
        topk_dict[t] = prob
    j = 0
    global topk_index_mapping
    topk_index_mapping = {}
    topk_sorted = dict(sorted(topk_dict.items(), key=lambda kv: kv[1], reverse=True))
    for key in topk_sorted:
        prob = topk_sorted[key] * 100
        print(
            str(j) + " Disease name:",
            diseases[key],
            "\tProbability:",
            str(round(prob, 2)) + "%",
        )
        out = (
            str(j) + " : Disease name:",
            diseases[key],
            "Probability:",
            str(round(prob, 2)) + "%",
        )
        output.append(out)
        topk_index_mapping[j] = key
        j += 1

    Symptoms.remove(value1)
    Symptoms.remove(value2)
    Symptoms.remove(value3)
    Symptoms.remove(value4)
    Symptoms.remove(value5)
    Symptoms.remove(value6)
    Symptoms.remove(value7)
    Symptoms.remove(value8)
    Symptoms.remove(value9)
    Symptoms.remove(value10)

    d0 = output[0]
    d1 = output[1]
    d2 = output[2]
    d3 = output[3]
    d4 = output[4]
    d5 = output[5]
    d6 = output[6]
    d7 = output[7]
    d8 = output[8]
    d9 = output[9]
    output.clear()
    sample_x = [0 for x in range(0, len(features))]
    return render_template(
        "result.html",
        text="{}".format(a),
        texts1="1.{}".format(s1),
        texts2="2.{}".format(s2),
        texts3="3.{}".format(s3),
        texts4="4.{}".format(s4),
        texts5="5.{}".format(s5),
        texts6="6.{}".format(s6),
        texts7="7.{}".format(s7),
        texts8="8.{}".format(s8),
        texts9="9.{}".format(s9),
        texts10="10.{}".format(s10),
        text2="{}".format(tt),
        text3="{}".format(d0),
        text4="{}".format(d1),
        text5="{}".format(d2),
        text6="{}".format(d3),
        text7="{}".format(d4),
        text8="{}".format(d5),
        text9="{}".format(d6),
        text10="{}".format(d7),
        text11="{}".format(d8),
        text12="{}".format(d9),
    )


if __name__ == "__main__":
    app.run(debug=True)

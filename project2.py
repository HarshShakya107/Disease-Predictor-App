import streamlit as st
import joblib
import numpy as np
import pandas as pd
from rapidfuzz  import process
import math

model=joblib.load("C:\\Users\\HP\\Downloads\\model.pkl")
df=pd.read_csv(r"C:\\Users\\HP\\Downloads\\disease_treatment_data.csv")

if "accepted" not in st.session_state:
    st.session_state.accepted = False

if not st.session_state.accepted:
    st.title("⚠️ Disclaimer")
    st.error("This model is approximately 85% accurate. Use at your own risk.")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ I Accept"):
            st.session_state.accepted = True
    with col2:
        if st.button("❌ Exit"):
            st.stop() 
else:
    st.success("Welcome! You have accepted the disclaimer.")

def get_treatment_info(disease_name):
    row = df[df['Disease'].str.lower() == disease_name.lower()]
    if not row.empty:
        treatment = row['Treatment'].values[0]
        medicines = row['Medicines'].values[0]
        specialist = row['Specialist'].values[0]
        home_remedy = row['Home Remedies'].values[0]
        return {
            'Treatment': treatment,
            'Medicines': medicines,
            'Specialist': specialist,
            'Home Remedies': home_remedy
        }
    else:
        return None

st.title("DISEASES PREDICTOR APP")
st.write("SELECT YOUR SYMPTOMS:")

symptoms=[ 
'itching',
 'skin_rash',
 'nodal_skin_eruptions',
 'continuous_sneezing',
 'shivering',
 'chills',
 'joint_pain',
 'stomach_pain',
 'acidity',
 'ulcers_on_tongue',
 'muscle_wasting',
'vomiting',
 'burning_micturition',
 'spotting_ urination',
 'fatigue',
 'weight_gain',
 'anxiety',
 'cold_hands_and_feets',
 'mood_swings',
 'weight_loss',
 'restlessness',
 'lethargy',
 'patches_in_throat',
 'irregular_sugar_level',
 'cough',
 'high_fever',
 'sunken_eyes',
 'breathlessness',
 'sweating',
 'dehydration',
 'indigestion',
 'headache',
 'yellowish_skin',
 'dark_urine',
 'nausea',
 'loss_of_appetite',
 'pain_behind_the_eyes',
 'back_pain',
 'constipation',
 'abdominal_pain',
 'diarrhoea',
 'mild_fever',
 'yellow_urine',
 'yellowing_of_eyes',
 'acute_liver_failure',
 'fluid_overload',
 'swelling_of_stomach',
 'swelled_lymph_nodes',
 'malaise',
 'blurred_and_distorted_vision',
 'phlegm',
 'throat_irritation',
 'redness_of_eyes',
 'sinus_pressure',
 'runny_nose',
 'congestion',
 'chest_pain',
 'weakness_in_limbs',
 'fast_heart_rate',
 'pain_during_bowel_movements',
 'pain_in_anal_region',
 'bloody_stool',
 'irritation_in_anus',
 'neck_pain',
 'dizziness',
 'cramps',
 'bruising',
 'obesity',
 'swollen_legs',
 'swollen_blood_vessels',
 'puffy_face_and_eyes',
 'enlarged_thyroid',
 'brittle_nails',
 'swollen_extremeties',
 'excessive_hunger',
 'extra_marital_contacts',
 'drying_and_tingling_lips',
 'slurred_speech',
 'knee_pain',
 'hip_joint_pain',
 'muscle_weakness',
 'stiff_neck',
 'swelling_joints',
 'movement_stiffness',
 'spinning_movements',
 'loss_of_balance',
 'unsteadiness',
 'weakness_of_one_body_side',
 'loss_of_smell',
 'bladder_discomfort',
 'foul_smell_of urine',
 'continuous_feel_of_urine',
 'passage_of_gases',
 'internal_itching',
 'toxic_look_(typhos)',
 'depression',
 'irritability',
 'muscle_pain',
 'altered_sensorium',
 'red_spots_over_body',
 'belly_pain',
 'abnormal_menstruation',
 'dischromic _patches',
 'watering_from_eyes',
 'increased_appetite',
 'polyuria',
 'family_history',
 'mucoid_sputum',
 'rusty_sputum',
 'lack_of_concentration',
 'visual_disturbances',
 'receiving_blood_transfusion',
 'receiving_unsterile_injections',
 'coma',
 'stomach_bleeding',
 'distention_of_abdomen',
 'history_of_alcohol_consumption',
 'fluid_overload.1',
 'blood_in_sputum',
 'prominent_veins_on_calf',
 'palpitations',
 'painful_walking',
 'pus_filled_pimples',
 'blackheads',
 'scurring',
 'skin_peeling',
 'silver_like_dusting',
 'small_dents_in_nails',
 'inflammatory_nails',
 'blister',
 'red_sore_around_nose',
 'yellow_crust_ooze']

num_cols = 5
checkboxes_per_row = num_cols
user_input = {}

for i in range(0, len(symptoms), checkboxes_per_row):
    cols = st.columns(num_cols)
    for j, col in enumerate(cols):
        if i + j < len(symptoms):
            symptom = symptoms[i + j]
            user_input[symptom] = col.checkbox(symptom)

input_df=pd.DataFrame([user_input])
if st.button("PREDICT DISEASE"):
    prediction=model.predict(input_df)[0]

    st.success(f"PRIDICTED DISEASE: {prediction}")

st.title("DISEASE TREATMENT RECOMENDATION")
disease_input = st.text_input("Enter Disease Name:")


if disease_input:
    info = get_treatment_info(disease_input)
    if info:
        st.subheader(f"Treatment Details for {disease_input}")
        st.write(f"**Treatment:** {info['Treatment']}")
        st.write(f"**Medicines:** {info['Medicines']}")
        st.write(f"**Specialist:** {info['Specialist']}")
        st.write(f"**Home Remedies:** {info['Home Remedies']}")
    else:
        st.error("Disease not found in database. Please check spelling or try another.")


df1 = pd.read_csv(r"C:\\Users\\HP\\Downloads\\daily_food_nutrition_dataset2.csv")


food_items = df1['Food_Item'].tolist()

def get_nutrition(food_name):
    match, score, _ = process.extractOne(food_name, food_items)
    if score < 60:
        return f"No close match found for '{food_name}'."
    nutrition = df1[df1['Food_Item'] == match].iloc[0]
    return nutrition

# Streamlit UI
st.title("Food Nutrition Lookup")

user_input = st.text_input("Enter food item name:")

if user_input:
    result = get_nutrition(user_input)
    if isinstance(result, str):
        st.error(result)
    else:
        st.write(result)




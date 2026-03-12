"""
Precautionary Advice Module
===========================
Comprehensive disease-specific precautionary advice including:
- General precautions
- Do's and Don'ts
- When to consult a doctor

Contains advice for all 50 diseases in the dataset.
"""

from typing import List, Optional

# ============================================
# Complete Disease Precautions Mapping
# All 50 diseases from the dataset
# ============================================

DISEASE_PRECAUTIONS = {
    
    # ==========================================
    # RESPIRATORY CONDITIONS
    # ==========================================
    
    "Common Cold": {
        "general": [
            "Rest and get adequate sleep to help your body recover",
            "Stay hydrated by drinking plenty of water, herbal tea, and warm fluids",
            "Use a humidifier to ease congestion and soothe irritated nasal passages",
            "Gargle with warm salt water to relieve sore throat"
        ],
        "dos": [
            "Wash hands frequently to prevent spreading",
            "Cover mouth and nose when sneezing or coughing",
            "Take over-the-counter medications for symptom relief",
            "Eat nutritious foods rich in vitamins C and zinc"
        ],
        "donts": [
            "Don't go to work or school while symptomatic",
            "Avoid close contact with others",
            "Don't smoke or be around secondhand smoke",
            "Avoid alcohol as it can dehydrate you"
        ],
        "consult_doctor": [
            "Symptoms persist beyond 10 days",
            "Fever above 103°F (39.4°C)",
            "Difficulty breathing or shortness of breath",
            "Severe headache or sinus pain"
        ]
    },
    
    "Influenza (Flu)": {
        "general": [
            "Rest at home and avoid strenuous activities",
            "Stay well-hydrated with water, clear broths, and electrolyte drinks",
            "Use fever-reducing medications as directed",
            "Keep warm and comfortable"
        ],
        "dos": [
            "Monitor your temperature regularly",
            "Take antiviral medications if prescribed within 48 hours",
            "Use tissues and dispose of them properly",
            "Isolate yourself from family members if possible"
        ],
        "donts": [
            "Don't take antibiotics (flu is viral, not bacterial)",
            "Avoid going to public places",
            "Don't ignore worsening symptoms",
            "Avoid giving aspirin to children (risk of Reye's syndrome)"
        ],
        "consult_doctor": [
            "Difficulty breathing or chest pain",
            "Persistent vomiting",
            "Symptoms that improve then return with fever and worse cough",
            "Confusion or sudden dizziness"
        ]
    },
    
    "Bronchitis": {
        "general": [
            "Get plenty of rest to help your body fight the infection",
            "Drink lots of fluids to thin mucus and prevent dehydration",
            "Use a humidifier or steam to loosen chest congestion",
            "Avoid irritants like smoke, dust, and strong fumes"
        ],
        "dos": [
            "Take prescribed medications as directed",
            "Use honey in warm water to soothe cough (adults only)",
            "Sleep with your head elevated to ease breathing",
            "Practice deep breathing exercises"
        ],
        "donts": [
            "Don't smoke or vape",
            "Avoid cold, dry air which irritates airways",
            "Don't suppress a productive cough completely",
            "Avoid dairy if it increases mucus production for you"
        ],
        "consult_doctor": [
            "Cough lasts more than 3 weeks",
            "You're coughing up blood or rust-colored mucus",
            "Fever higher than 100.4°F (38°C) for more than 3 days",
            "You have difficulty breathing or wheezing"
        ]
    },
    
    "Pneumonia": {
        "general": [
            "Get plenty of rest - your body needs energy to fight infection",
            "Drink plenty of fluids to stay hydrated and loosen mucus",
            "Take all prescribed medications exactly as directed",
            "Use a cool-mist humidifier to ease breathing"
        ],
        "dos": [
            "Complete the full course of antibiotics if prescribed",
            "Monitor your temperature and oxygen levels if possible",
            "Practice deep breathing and coughing exercises",
            "Get a follow-up chest X-ray as recommended"
        ],
        "donts": [
            "Don't smoke or be around smokers",
            "Avoid alcohol as it weakens immune response",
            "Don't skip doses of prescribed medications",
            "Avoid crowded places until fully recovered"
        ],
        "consult_doctor": [
            "Difficulty breathing or rapid breathing",
            "Chest pain that worsens when breathing",
            "High fever that doesn't respond to medication",
            "Confusion or altered mental state"
        ]
    },
    
    "Asthma": {
        "general": [
            "Keep your rescue inhaler with you at all times",
            "Identify and avoid your asthma triggers",
            "Follow your asthma action plan consistently",
            "Monitor your peak flow readings regularly"
        ],
        "dos": [
            "Take controller medications daily as prescribed",
            "Use spacer devices with inhalers for better delivery",
            "Get annual flu vaccinations",
            "Exercise regularly with proper warm-up"
        ],
        "donts": [
            "Don't ignore early warning signs of an attack",
            "Avoid smoking and secondhand smoke",
            "Don't exercise outdoors when air quality is poor",
            "Never stop controller medications without doctor's advice"
        ],
        "consult_doctor": [
            "Rescue inhaler doesn't provide relief",
            "Symptoms worsen rapidly or frequently",
            "You need rescue inhaler more than twice a week",
            "Lips or fingernails turn blue"
        ]
    },
    
    "Tuberculosis": {
        "general": [
            "Take all medications exactly as prescribed for the full duration",
            "Cover mouth when coughing and dispose of tissues properly",
            "Ensure good ventilation in living spaces",
            "Wear a mask when around others during infectious period"
        ],
        "dos": [
            "Attend all follow-up appointments for monitoring",
            "Eat a nutritious diet to support recovery",
            "Inform close contacts so they can get tested",
            "Get adequate rest during treatment"
        ],
        "donts": [
            "Never skip doses or stop treatment early",
            "Avoid alcohol as it affects liver during TB treatment",
            "Don't go to work/school until cleared by doctor",
            "Avoid sharing personal items with others"
        ],
        "consult_doctor": [
            "You experience side effects from medications",
            "Symptoms worsen or don't improve after 2-3 weeks",
            "You develop new symptoms like vision changes",
            "You have difficulty taking medications regularly"
        ]
    },
    
    "Sinusitis": {
        "general": [
            "Use saline nasal spray or irrigation to clear sinuses",
            "Apply warm compresses to face for pain relief",
            "Stay hydrated to thin mucus secretions",
            "Sleep with head elevated to help drainage"
        ],
        "dos": [
            "Use a humidifier to keep nasal passages moist",
            "Inhale steam from a bowl of hot water",
            "Take over-the-counter decongestants as directed",
            "Blow nose gently, one nostril at a time"
        ],
        "donts": [
            "Don't use decongestant sprays for more than 3 days",
            "Avoid flying or diving with sinus congestion",
            "Don't smoke or be exposed to smoke",
            "Avoid very dry environments"
        ],
        "consult_doctor": [
            "Symptoms last more than 10 days",
            "Severe facial pain or headache",
            "Fever higher than 102°F (39°C)",
            "Symptoms return after initial improvement"
        ]
    },
    
    "Allergic Rhinitis": {
        "general": [
            "Identify and avoid your allergy triggers",
            "Keep windows closed during high pollen seasons",
            "Use air purifiers with HEPA filters indoors",
            "Shower after being outdoors to remove allergens"
        ],
        "dos": [
            "Take antihistamines as recommended",
            "Wear sunglasses outdoors to protect eyes",
            "Wash bedding weekly in hot water",
            "Check pollen forecasts before outdoor activities"
        ],
        "donts": [
            "Don't dry clothes outdoors during allergy season",
            "Avoid rubbing your eyes",
            "Don't keep windows open at night",
            "Avoid mowing grass or raking leaves"
        ],
        "consult_doctor": [
            "Over-the-counter medications don't provide relief",
            "Symptoms significantly affect daily life or sleep",
            "You experience wheezing or difficulty breathing",
            "You want to discuss allergy testing or immunotherapy"
        ]
    },
    
    # ==========================================
    # GASTROINTESTINAL CONDITIONS
    # ==========================================
    
    "Food Poisoning": {
        "general": [
            "Let your stomach settle - avoid eating for a few hours",
            "Sip small amounts of water or clear fluids frequently",
            "Gradually introduce bland foods (BRAT diet: bananas, rice, applesauce, toast)",
            "Rest and allow your body to recover"
        ],
        "dos": [
            "Stay hydrated with oral rehydration solutions",
            "Wash hands thoroughly before handling food",
            "Monitor for signs of dehydration",
            "Keep track of what you ate to identify the source"
        ],
        "donts": [
            "Don't eat dairy, fatty, or spicy foods until recovered",
            "Avoid caffeine and alcohol",
            "Don't take anti-diarrheal medications initially",
            "Don't prepare food for others while symptomatic"
        ],
        "consult_doctor": [
            "Symptoms last more than 3 days",
            "Blood in stool or vomit",
            "Signs of severe dehydration (dizziness, dark urine)",
            "High fever above 101.5°F (38.6°C)"
        ]
    },
    
    "Gastroenteritis": {
        "general": [
            "Focus on staying hydrated - small, frequent sips",
            "Rest as much as possible",
            "Gradually reintroduce bland foods when able",
            "Practice good hygiene to prevent spreading"
        ],
        "dos": [
            "Drink oral rehydration solutions or electrolyte drinks",
            "Eat small portions of easy-to-digest foods",
            "Wash hands frequently, especially after bathroom",
            "Disinfect commonly touched surfaces"
        ],
        "donts": [
            "Don't drink fruit juices or sugary drinks",
            "Avoid dairy products temporarily",
            "Don't share towels or utensils",
            "Don't return to work for 48 hours after symptoms stop"
        ],
        "consult_doctor": [
            "Unable to keep any fluids down for 24 hours",
            "Diarrhea lasts more than 3 days",
            "Signs of severe dehydration",
            "Blood in stool or severe abdominal pain"
        ]
    },
    
    "Acid Reflux (GERD)": {
        "general": [
            "Eat smaller, more frequent meals",
            "Avoid lying down for 3 hours after eating",
            "Elevate the head of your bed by 6-8 inches",
            "Maintain a healthy weight"
        ],
        "dos": [
            "Chew food thoroughly and eat slowly",
            "Wear loose-fitting clothes",
            "Keep a food diary to identify triggers",
            "Take prescribed medications as directed"
        ],
        "donts": [
            "Don't eat spicy, acidic, or fatty foods",
            "Avoid alcohol and caffeine",
            "Don't smoke - it weakens the lower esophageal sphincter",
            "Avoid eating late at night"
        ],
        "consult_doctor": [
            "Symptoms occur more than twice a week",
            "Difficulty swallowing or painful swallowing",
            "Unexplained weight loss",
            "Chest pain (to rule out heart issues)"
        ]
    },
    
    "Peptic Ulcer": {
        "general": [
            "Take prescribed medications exactly as directed",
            "Eat regular meals at consistent times",
            "Manage stress through relaxation techniques",
            "Avoid foods that worsen your symptoms"
        ],
        "dos": [
            "Complete the full course of antibiotics if prescribed",
            "Eat a balanced diet with adequate fiber",
            "Stay well-hydrated with water",
            "Get adequate sleep"
        ],
        "donts": [
            "Don't take NSAIDs like aspirin or ibuprofen",
            "Avoid alcohol completely during healing",
            "Don't smoke - it delays healing",
            "Don't skip meals or overeat"
        ],
        "consult_doctor": [
            "Sharp, sudden abdominal pain",
            "Vomiting blood or dark, tarry stools",
            "Unexplained weight loss",
            "Symptoms don't improve with treatment"
        ]
    },
    
    "Irritable Bowel Syndrome": {
        "general": [
            "Identify and avoid your trigger foods",
            "Eat regular meals and don't skip meals",
            "Manage stress through relaxation techniques",
            "Exercise regularly to improve bowel function"
        ],
        "dos": [
            "Keep a food and symptom diary",
            "Eat slowly and chew food thoroughly",
            "Drink plenty of water",
            "Consider probiotics after consulting doctor"
        ],
        "donts": [
            "Don't eat large meals",
            "Avoid carbonated drinks and artificial sweeteners",
            "Don't eat too much fiber too quickly",
            "Avoid caffeine and alcohol if they trigger symptoms"
        ],
        "consult_doctor": [
            "Symptoms significantly impact quality of life",
            "Unexplained weight loss",
            "Blood in stool",
            "Symptoms started after age 50"
        ]
    },
    
    "Appendicitis": {
        "general": [
            "Seek immediate medical attention - this is a medical emergency",
            "Do not eat or drink anything",
            "Lie still and avoid moving around",
            "Do not take pain medications until evaluated"
        ],
        "dos": [
            "Call emergency services or go to ER immediately",
            "Note when pain started and its progression",
            "Stay calm and breathe normally",
            "Have someone drive you to the hospital"
        ],
        "donts": [
            "Don't apply heat to the abdomen",
            "Don't take laxatives or enemas",
            "Don't ignore the pain hoping it will pass",
            "Don't eat or drink anything"
        ],
        "consult_doctor": [
            "Any sudden severe abdominal pain",
            "Pain that starts near navel and moves to lower right",
            "Pain worsens with movement, coughing, or walking",
            "Fever, nausea, and loss of appetite with pain"
        ]
    },
    
    # ==========================================
    # INFECTIOUS DISEASES
    # ==========================================
    
    "Malaria": {
        "general": [
            "Take all antimalarial medications exactly as prescribed",
            "Rest and stay well-hydrated",
            "Monitor temperature regularly",
            "Use mosquito nets while recovering"
        ],
        "dos": [
            "Complete the full course of treatment",
            "Eat light, nutritious meals",
            "Take fever-reducing medications as directed",
            "Report any side effects to your doctor"
        ],
        "donts": [
            "Don't skip doses of antimalarial medication",
            "Avoid mosquito bites to prevent reinfection",
            "Don't donate blood for at least 3 years after infection",
            "Don't take any additional medications without doctor's approval"
        ],
        "consult_doctor": [
            "High fever that doesn't respond to treatment",
            "Severe headache or confusion",
            "Difficulty breathing",
            "Dark or decreased urine output"
        ]
    },
    
    "Dengue": {
        "general": [
            "Rest completely and avoid physical exertion",
            "Stay well-hydrated with water, ORS, and coconut water",
            "Monitor platelet count regularly",
            "Take only acetaminophen/paracetamol for fever"
        ],
        "dos": [
            "Drink at least 3 liters of fluids daily",
            "Eat nutritious, easily digestible foods",
            "Use mosquito repellent to prevent spreading",
            "Watch for warning signs of severe dengue"
        ],
        "donts": [
            "Don't take aspirin or ibuprofen (increases bleeding risk)",
            "Avoid dark-colored drinks to monitor vomiting",
            "Don't ignore warning signs like severe abdominal pain",
            "Avoid getting bitten by mosquitoes"
        ],
        "consult_doctor": [
            "Severe abdominal pain or persistent vomiting",
            "Bleeding gums or blood in vomit/stool",
            "Difficulty breathing or fatigue",
            "Platelet count drops significantly"
        ]
    },
    
    "Typhoid": {
        "general": [
            "Take antibiotics exactly as prescribed for full duration",
            "Rest and avoid strenuous activities",
            "Drink plenty of safe, clean water",
            "Eat small, frequent meals"
        ],
        "dos": [
            "Practice strict hand hygiene",
            "Eat freshly cooked, hot foods",
            "Get follow-up stool cultures as recommended",
            "Inform close contacts to get tested"
        ],
        "donts": [
            "Don't handle food for others until cleared",
            "Avoid raw fruits and vegetables unless self-peeled",
            "Don't stop antibiotics early even if feeling better",
            "Avoid ice and drinks that may be contaminated"
        ],
        "consult_doctor": [
            "High fever persists despite treatment",
            "Severe abdominal pain or distension",
            "Blood in stool",
            "Confusion or altered consciousness"
        ]
    },
    
    "Chickenpox": {
        "general": [
            "Stay home and isolate until all blisters have crusted over",
            "Keep skin clean and dry",
            "Keep fingernails short to prevent scratching damage",
            "Take lukewarm baths with colloidal oatmeal"
        ],
        "dos": [
            "Apply calamine lotion to relieve itching",
            "Take antihistamines for itch relief",
            "Wear loose, soft clothing",
            "Stay hydrated and eat soft foods"
        ],
        "donts": [
            "Don't scratch the blisters (causes scarring and infection)",
            "Don't give aspirin to children (Reye's syndrome risk)",
            "Don't go to school/work until fully crusted",
            "Avoid contact with pregnant women and immunocompromised people"
        ],
        "consult_doctor": [
            "High fever lasting more than 4 days",
            "Rash spreads to eyes",
            "Rash becomes very red, warm, or tender",
            "Difficulty breathing or confusion"
        ]
    },
    
    "Measles": {
        "general": [
            "Isolate completely until 4 days after rash appears",
            "Rest and stay in a dimly lit room (light sensitivity)",
            "Stay well-hydrated with fluids",
            "Take fever-reducing medications as directed"
        ],
        "dos": [
            "Take vitamin A supplements if recommended",
            "Use a humidifier for cough relief",
            "Gently clean eyes with warm water",
            "Eat soft, nutritious foods"
        ],
        "donts": [
            "Don't go to public places while infectious",
            "Avoid contact with unvaccinated individuals",
            "Don't rub eyes",
            "Don't ignore high fever or breathing difficulties"
        ],
        "consult_doctor": [
            "Fever returns after initially improving",
            "Difficulty breathing or rapid breathing",
            "Earache or hearing problems",
            "Seizures or altered consciousness"
        ]
    },
    
    "Mumps": {
        "general": [
            "Rest and stay home until swelling subsides",
            "Apply warm or cold compresses to swollen glands",
            "Stay well-hydrated with non-acidic fluids",
            "Eat soft foods that don't require much chewing"
        ],
        "dos": [
            "Take pain relievers as directed for discomfort",
            "Gargle with warm salt water",
            "Get plenty of sleep",
            "Apply ice packs to swollen areas"
        ],
        "donts": [
            "Don't eat sour or acidic foods (increases saliva and pain)",
            "Avoid contact with others for 5 days after swelling begins",
            "Don't share eating utensils",
            "Don't return to school/work until fully recovered"
        ],
        "consult_doctor": [
            "Severe headache or neck stiffness",
            "Testicular pain and swelling in males",
            "Abdominal pain (possible pancreatic involvement)",
            "Hearing loss"
        ]
    },
    
    "Hepatitis": {
        "general": [
            "Rest and avoid strenuous activities",
            "Eat a balanced, nutritious diet",
            "Avoid alcohol completely",
            "Take prescribed medications as directed"
        ],
        "dos": [
            "Stay well-hydrated",
            "Eat small, frequent meals if nauseous",
            "Practice good hygiene to prevent spread",
            "Get adequate sleep"
        ],
        "donts": [
            "Don't drink alcohol - it damages the liver further",
            "Don't take over-the-counter medications without asking doctor",
            "Don't share personal items like razors or toothbrushes",
            "Avoid fatty and processed foods"
        ],
        "consult_doctor": [
            "Severe abdominal pain",
            "Yellowing of skin or eyes increases",
            "Dark urine or pale stools",
            "Confusion or drowsiness"
        ]
    },
    
    "Conjunctivitis": {
        "general": [
            "Practice strict hand hygiene",
            "Clean eyes gently with warm water",
            "Use separate towels and pillowcases",
            "Avoid touching or rubbing eyes"
        ],
        "dos": [
            "Apply prescribed eye drops as directed",
            "Use clean, warm compresses for comfort",
            "Remove contact lenses and use glasses",
            "Wash hands before and after touching eyes"
        ],
        "donts": [
            "Don't share eye makeup, towels, or pillows",
            "Don't wear contact lenses until fully healed",
            "Don't touch eyes with unwashed hands",
            "Avoid swimming pools until infection clears"
        ],
        "consult_doctor": [
            "Vision changes or severe eye pain",
            "Sensitivity to light",
            "Symptoms worsen or don't improve in 24-48 hours",
            "Thick discharge that keeps eyes from opening"
        ]
    },
    
    # ==========================================
    # SKIN CONDITIONS
    # ==========================================
    
    "Eczema": {
        "general": [
            "Keep skin moisturized with thick creams or ointments",
            "Take lukewarm (not hot) baths or showers",
            "Identify and avoid your triggers",
            "Wear soft, breathable fabrics like cotton"
        ],
        "dos": [
            "Apply moisturizer within 3 minutes of bathing",
            "Use fragrance-free products",
            "Keep fingernails short to minimize scratching damage",
            "Use a humidifier in dry environments"
        ],
        "donts": [
            "Don't take hot showers or baths",
            "Avoid harsh soaps and detergents",
            "Don't scratch - it worsens the condition",
            "Avoid wool and synthetic fabrics"
        ],
        "consult_doctor": [
            "Skin becomes very red, hot, or painful",
            "Signs of infection (oozing, crusting, fever)",
            "Eczema doesn't respond to treatment",
            "Sleep is significantly affected"
        ]
    },
    
    "Psoriasis": {
        "general": [
            "Keep skin moisturized regularly",
            "Get moderate sun exposure (but don't burn)",
            "Manage stress through relaxation techniques",
            "Avoid skin injuries (cuts, scrapes, sunburns)"
        ],
        "dos": [
            "Take prescribed medications consistently",
            "Use medicated shampoos for scalp psoriasis",
            "Keep a symptom diary to identify triggers",
            "Soak in lukewarm baths with bath oils"
        ],
        "donts": [
            "Don't pick or scratch plaques",
            "Avoid alcohol - it can trigger flares",
            "Don't smoke - it worsens symptoms",
            "Avoid very hot water"
        ],
        "consult_doctor": [
            "Psoriasis covers large areas of body",
            "Joint pain or stiffness develops",
            "Current treatment isn't working",
            "Significant impact on quality of life"
        ]
    },
    
    "Acne": {
        "general": [
            "Wash face twice daily with gentle cleanser",
            "Keep hands off your face",
            "Use non-comedogenic skincare products",
            "Stay hydrated and eat a balanced diet"
        ],
        "dos": [
            "Use prescribed topical treatments consistently",
            "Change pillowcases frequently",
            "Remove makeup before bed",
            "Be patient - treatments take 6-8 weeks to work"
        ],
        "donts": [
            "Don't pop or squeeze pimples (causes scarring)",
            "Avoid heavy, oil-based makeup",
            "Don't over-wash or scrub face harshly",
            "Don't touch your face frequently"
        ],
        "consult_doctor": [
            "Acne is severe or widespread",
            "Over-the-counter treatments don't help",
            "Acne is leaving scars",
            "Acne is affecting self-esteem significantly"
        ]
    },
    
    "Dermatitis": {
        "general": [
            "Identify and avoid irritants or allergens",
            "Keep affected areas moisturized",
            "Avoid scratching the affected areas",
            "Wear protective gloves when using chemicals"
        ],
        "dos": [
            "Apply prescribed creams or ointments",
            "Use fragrance-free, hypoallergenic products",
            "Pat skin dry instead of rubbing",
            "Wear loose, cotton clothing"
        ],
        "donts": [
            "Don't use harsh soaps or detergents",
            "Avoid very hot water",
            "Don't wear jewelry that irritates skin",
            "Avoid prolonged exposure to water"
        ],
        "consult_doctor": [
            "Rash spreads or becomes severely infected",
            "Pain, swelling, or fever develops",
            "Home treatments aren't effective",
            "You can't identify the cause"
        ]
    },
    
    "Fungal Infection": {
        "general": [
            "Keep affected areas clean and dry",
            "Apply antifungal medications as directed",
            "Avoid sharing personal items",
            "Wear loose, breathable clothing"
        ],
        "dos": [
            "Complete full course of antifungal treatment",
            "Change socks and underwear daily",
            "Dry thoroughly after bathing, especially between toes",
            "Wash clothes and towels in hot water"
        ],
        "donts": [
            "Don't walk barefoot in public areas",
            "Avoid tight, non-breathable shoes",
            "Don't share towels, razors, or combs",
            "Don't stop treatment when symptoms improve"
        ],
        "consult_doctor": [
            "Infection doesn't improve after 2 weeks of treatment",
            "Infection spreads or returns",
            "You have diabetes or weakened immune system",
            "Redness, swelling, or pus develops"
        ]
    },
    
    # ==========================================
    # CARDIOVASCULAR CONDITIONS
    # ==========================================
    
    "Hypertension": {
        "general": [
            "Monitor blood pressure regularly at home",
            "Reduce sodium intake in your diet",
            "Engage in regular moderate exercise",
            "Manage stress through relaxation techniques"
        ],
        "dos": [
            "Take prescribed medications as directed",
            "Eat a DASH diet (fruits, vegetables, whole grains)",
            "Maintain a healthy weight",
            "Limit alcohol consumption"
        ],
        "donts": [
            "Don't skip medications without doctor's advice",
            "Avoid processed and high-sodium foods",
            "Don't smoke or use tobacco products",
            "Don't ignore symptoms like severe headaches"
        ],
        "consult_doctor": [
            "Blood pressure consistently above 140/90 mmHg",
            "Severe headache, chest pain, or vision changes",
            "Numbness or weakness in limbs",
            "Difficulty breathing"
        ]
    },
    
    "Heart Disease": {
        "general": [
            "Follow your cardiologist's treatment plan exactly",
            "Take all medications as prescribed",
            "Monitor symptoms and report changes",
            "Make heart-healthy lifestyle changes"
        ],
        "dos": [
            "Exercise as recommended by your doctor",
            "Eat a heart-healthy diet low in saturated fats",
            "Maintain a healthy weight",
            "Manage stress and get adequate sleep"
        ],
        "donts": [
            "Don't smoke or use tobacco in any form",
            "Avoid excessive alcohol consumption",
            "Don't ignore warning signs",
            "Don't engage in strenuous activity without guidance"
        ],
        "consult_doctor": [
            "Chest pain or discomfort",
            "Shortness of breath, especially during rest",
            "Swelling in legs, ankles, or feet",
            "Rapid or irregular heartbeat"
        ]
    },
    
    "Anemia": {
        "general": [
            "Eat iron-rich foods like spinach, red meat, and beans",
            "Take iron supplements if prescribed (with vitamin C)",
            "Get adequate rest as your body builds blood cells",
            "Stay hydrated"
        ],
        "dos": [
            "Pair iron-rich foods with vitamin C for better absorption",
            "Cook in cast iron pans to increase iron content",
            "Eat fortified cereals and breads",
            "Get regular blood tests to monitor levels"
        ],
        "donts": [
            "Don't drink tea or coffee with iron-rich meals",
            "Avoid calcium supplements with iron tablets",
            "Don't ignore symptoms of fatigue",
            "Avoid excessive consumption of dairy with iron-rich foods"
        ],
        "consult_doctor": [
            "Extreme fatigue or weakness",
            "Shortness of breath with minimal activity",
            "Rapid heartbeat or chest pain",
            "Pale skin, dizziness, or cold hands/feet"
        ]
    },
    
    # ==========================================
    # METABOLIC & ENDOCRINE CONDITIONS
    # ==========================================
    
    "Diabetes": {
        "general": [
            "Monitor blood sugar levels as recommended",
            "Follow a balanced, low-glycemic diet",
            "Stay physically active with regular exercise",
            "Take medications or insulin as prescribed"
        ],
        "dos": [
            "Check feet daily for cuts, blisters, or sores",
            "Carry fast-acting glucose for low blood sugar",
            "Wear medical identification",
            "Attend all medical appointments"
        ],
        "donts": [
            "Don't skip meals or medications",
            "Avoid sugary drinks and excessive carbohydrates",
            "Don't walk barefoot to prevent foot injuries",
            "Don't ignore symptoms of high or low blood sugar"
        ],
        "consult_doctor": [
            "Blood sugar frequently out of target range",
            "Signs of hypoglycemia or hyperglycemia",
            "Slow-healing wounds or frequent infections",
            "Numbness or tingling in hands or feet"
        ]
    },
    
    "Hyperthyroidism": {
        "general": [
            "Take prescribed medications consistently",
            "Get adequate rest despite feeling energetic",
            "Protect eyes if experiencing thyroid eye disease",
            "Manage stress as it can worsen symptoms"
        ],
        "dos": [
            "Eat a well-balanced diet with adequate calcium",
            "Attend all follow-up appointments",
            "Exercise moderately as tolerated",
            "Keep regular meal and sleep schedules"
        ],
        "donts": [
            "Don't consume excessive iodine or kelp",
            "Avoid caffeine and stimulants",
            "Don't skip medications",
            "Avoid smoking - worsens eye complications"
        ],
        "consult_doctor": [
            "Rapid or irregular heartbeat",
            "Unexplained weight loss despite eating well",
            "Eye problems (bulging, irritation, vision changes)",
            "Severe anxiety or tremors"
        ]
    },
    
    "Hypothyroidism": {
        "general": [
            "Take thyroid medication on empty stomach, same time daily",
            "Get regular thyroid function tests",
            "Eat a balanced diet with adequate iodine",
            "Exercise regularly to boost metabolism"
        ],
        "dos": [
            "Take medication 30-60 minutes before breakfast",
            "Wait 4 hours before taking calcium or iron supplements",
            "Stay consistent with medication timing",
            "Monitor for symptom changes"
        ],
        "donts": [
            "Don't skip doses of thyroid medication",
            "Avoid soy products near medication time",
            "Don't take with coffee - wait 30 minutes",
            "Don't stop medication even if feeling better"
        ],
        "consult_doctor": [
            "Symptoms worsen despite treatment",
            "Heart palpitations or chest pain",
            "Severe fatigue or depression",
            "Significant weight changes"
        ]
    },
    
    # ==========================================
    # NEUROLOGICAL CONDITIONS
    # ==========================================
    
    "Migraine": {
        "general": [
            "Rest in a quiet, dark room during episodes",
            "Apply cold or warm compresses to head/neck",
            "Stay hydrated and maintain regular meals",
            "Practice stress-reduction techniques"
        ],
        "dos": [
            "Keep a headache diary to identify triggers",
            "Take medications at first sign of migraine",
            "Maintain regular sleep schedule",
            "Practice relaxation exercises daily"
        ],
        "donts": [
            "Don't skip meals or fast",
            "Avoid excessive caffeine or sudden withdrawal",
            "Don't overuse pain medications",
            "Avoid bright lights and loud noises during episodes"
        ],
        "consult_doctor": [
            "Migraines occur more than 15 days per month",
            "Pain medications don't provide relief",
            "New or different headache patterns",
            "Headache with fever, stiff neck, or confusion"
        ]
    },
    
    "Tension Headache": {
        "general": [
            "Apply heat or cold to head and neck muscles",
            "Practice good posture throughout the day",
            "Take regular breaks from screens",
            "Manage stress through relaxation techniques"
        ],
        "dos": [
            "Massage tense muscles in shoulders and neck",
            "Get regular sleep on a consistent schedule",
            "Stay hydrated throughout the day",
            "Exercise regularly to reduce tension"
        ],
        "donts": [
            "Don't clench jaw or grind teeth",
            "Avoid overuse of pain medications",
            "Don't skip meals",
            "Avoid excessive screen time without breaks"
        ],
        "consult_doctor": [
            "Headaches occur more than 15 days per month",
            "Over-the-counter medications don't help",
            "Headache pattern changes suddenly",
            "Headaches affect daily activities"
        ]
    },
    
    "Vertigo": {
        "general": [
            "Move slowly and carefully to prevent falls",
            "Sit or lie down immediately when symptoms start",
            "Keep your head still during episodes",
            "Focus on a fixed point to help with balance"
        ],
        "dos": [
            "Use good lighting to help with balance",
            "Use handrails on stairs",
            "Do prescribed vestibular exercises",
            "Sleep with head slightly elevated"
        ],
        "donts": [
            "Don't make sudden head movements",
            "Avoid driving during episodes",
            "Don't climb ladders or work at heights",
            "Avoid alcohol and caffeine"
        ],
        "consult_doctor": [
            "Vertigo is accompanied by hearing loss",
            "Symptoms are severe or frequent",
            "You experience numbness, weakness, or vision changes",
            "Vertigo doesn't improve with treatment"
        ]
    },
    
    "Epilepsy": {
        "general": [
            "Take anti-seizure medications consistently",
            "Get adequate, regular sleep",
            "Avoid known seizure triggers",
            "Wear medical identification"
        ],
        "dos": [
            "Keep a seizure diary",
            "Inform family and friends about first aid",
            "Take medications at the same time daily",
            "Stay well-hydrated"
        ],
        "donts": [
            "Don't stop medications without doctor's guidance",
            "Avoid excessive alcohol consumption",
            "Don't drive until cleared by doctor",
            "Avoid swimming or bathing alone"
        ],
        "consult_doctor": [
            "Seizure frequency increases",
            "New types of seizures occur",
            "Medication side effects are troublesome",
            "Seizure lasts more than 5 minutes (emergency)"
        ]
    },
    
    # ==========================================
    # MENTAL HEALTH CONDITIONS
    # ==========================================
    
    "Anxiety Disorder": {
        "general": [
            "Practice deep breathing and mindfulness",
            "Maintain a regular sleep schedule",
            "Engage in regular physical activity",
            "Limit caffeine and alcohol"
        ],
        "dos": [
            "Talk to trusted friends or family",
            "Practice progressive muscle relaxation",
            "Keep a journal to track triggers",
            "Consider professional therapy"
        ],
        "donts": [
            "Don't isolate yourself from support",
            "Avoid excessive caffeine and stimulants",
            "Don't rely on alcohol or substances to cope",
            "Don't dismiss your feelings"
        ],
        "consult_doctor": [
            "Anxiety significantly interferes with daily life",
            "You experience panic attacks",
            "Physical symptoms persist",
            "You have thoughts of self-harm"
        ]
    },
    
    "Depression": {
        "general": [
            "Maintain a daily routine as much as possible",
            "Get regular physical activity, even brief walks",
            "Stay connected with supportive people",
            "Practice good sleep hygiene"
        ],
        "dos": [
            "Set small, achievable daily goals",
            "Eat regular, nutritious meals",
            "Consider therapy or counseling",
            "Take prescribed medications as directed"
        ],
        "donts": [
            "Don't isolate yourself",
            "Avoid alcohol and recreational drugs",
            "Don't make major life decisions while depressed",
            "Don't be too hard on yourself"
        ],
        "consult_doctor": [
            "Symptoms last more than two weeks",
            "Daily functioning is significantly impaired",
            "You have thoughts of suicide or self-harm",
            "Symptoms worsen despite treatment"
        ]
    },
    
    "Insomnia": {
        "general": [
            "Maintain a consistent sleep schedule",
            "Create a relaxing bedtime routine",
            "Make your bedroom dark, quiet, and cool",
            "Limit screen time before bed"
        ],
        "dos": [
            "Exercise regularly, but not close to bedtime",
            "Use bed only for sleep and intimacy",
            "Practice relaxation techniques before bed",
            "Get exposure to natural light during the day"
        ],
        "donts": [
            "Don't consume caffeine after noon",
            "Avoid long daytime naps",
            "Don't watch TV or use phones in bed",
            "Don't lie in bed awake for long periods"
        ],
        "consult_doctor": [
            "Insomnia persists for more than 3 weeks",
            "Sleep problems affect daytime functioning",
            "You suspect a sleep disorder like sleep apnea",
            "Other health conditions may be contributing"
        ]
    },
    
    # ==========================================
    # MUSCULOSKELETAL CONDITIONS
    # ==========================================
    
    "Arthritis": {
        "general": [
            "Stay active with gentle, low-impact exercises",
            "Apply heat or cold therapy for pain relief",
            "Maintain a healthy weight to reduce joint stress",
            "Protect joints during daily activities"
        ],
        "dos": [
            "Take medications as prescribed",
            "Do stretching exercises daily",
            "Use assistive devices if needed",
            "Balance activity with rest"
        ],
        "donts": [
            "Don't remain sedentary for too long",
            "Avoid repetitive stress on affected joints",
            "Don't ignore increasing pain",
            "Avoid high-impact activities"
        ],
        "consult_doctor": [
            "Joint pain or swelling is severe",
            "You develop a fever with joint symptoms",
            "Joint becomes suddenly red and hot",
            "Current medications aren't controlling symptoms"
        ]
    },
    
    "Osteoporosis": {
        "general": [
            "Get adequate calcium and vitamin D",
            "Engage in weight-bearing exercises",
            "Prevent falls with home safety measures",
            "Take prescribed medications as directed"
        ],
        "dos": [
            "Eat calcium-rich foods like dairy and leafy greens",
            "Get regular bone density tests",
            "Do strength training exercises",
            "Get safe sun exposure for vitamin D"
        ],
        "donts": [
            "Don't smoke - it weakens bones",
            "Avoid excessive alcohol",
            "Don't engage in high-risk activities",
            "Avoid bending and twisting spine"
        ],
        "consult_doctor": [
            "You experience a fracture from minor injury",
            "Severe back pain develops suddenly",
            "Height loss is noticeable",
            "You have risk factors for osteoporosis"
        ]
    },
    
    "Muscle Strain": {
        "general": [
            "Rest the injured muscle",
            "Apply ice for first 48-72 hours",
            "Use compression to reduce swelling",
            "Elevate the injured area"
        ],
        "dos": [
            "Take over-the-counter pain relievers",
            "Gradually return to activity as pain allows",
            "Do gentle stretching once acute pain subsides",
            "Use heat therapy after initial swelling goes down"
        ],
        "donts": [
            "Don't continue activities that cause pain",
            "Avoid heat application in first 48 hours",
            "Don't return to full activity too quickly",
            "Avoid massage during acute phase"
        ],
        "consult_doctor": [
            "Severe pain or swelling",
            "Inability to use the affected muscle",
            "Pain doesn't improve after a week",
            "You heard a 'pop' at time of injury"
        ]
    },
    
    # ==========================================
    # URINARY CONDITIONS
    # ==========================================
    
    "Urinary Tract Infection": {
        "general": [
            "Drink plenty of water to flush bacteria",
            "Urinate frequently - don't hold it",
            "Use a heating pad on abdomen for comfort",
            "Complete prescribed antibiotic course"
        ],
        "dos": [
            "Wipe front to back after using bathroom",
            "Urinate before and after sexual activity",
            "Wear breathable cotton underwear",
            "Take cranberry supplements if helpful"
        ],
        "donts": [
            "Don't use scented products in genital area",
            "Avoid caffeine and alcohol until recovered",
            "Don't hold urine for long periods",
            "Don't stop antibiotics early"
        ],
        "consult_doctor": [
            "Symptoms don't improve within 2 days",
            "Fever, chills, or back pain develop",
            "Blood in urine",
            "You get frequent UTIs (3+ per year)"
        ]
    },
    
    "Kidney Stones": {
        "general": [
            "Drink plenty of water (2-3 liters daily)",
            "Take prescribed pain medications",
            "Use heat therapy for pain relief",
            "Strain urine to catch the stone for analysis"
        ],
        "dos": [
            "Stay as active as possible to help pass stone",
            "Follow dietary recommendations for your stone type",
            "Take prescribed medications to help pass stone",
            "Drink citrus juices (lemon, orange)"
        ],
        "donts": [
            "Don't limit fluids",
            "Avoid excessive sodium intake",
            "Don't ignore severe pain or fever",
            "Avoid foods high in oxalates if applicable"
        ],
        "consult_doctor": [
            "Severe pain that doesn't respond to medication",
            "Unable to urinate",
            "Fever, chills, or vomiting",
            "Blood in urine is heavy"
        ]
    },
    
    "Kidney Disease": {
        "general": [
            "Control blood pressure and blood sugar",
            "Follow kidney-friendly diet as prescribed",
            "Take all medications as directed",
            "Attend all medical appointments"
        ],
        "dos": [
            "Monitor blood pressure at home",
            "Limit sodium, phosphorus, and potassium as advised",
            "Stay physically active as tolerated",
            "Maintain a healthy weight"
        ],
        "donts": [
            "Don't take NSAIDs without doctor's approval",
            "Avoid excessive protein intake",
            "Don't smoke",
            "Avoid herbal supplements without consulting doctor"
        ],
        "consult_doctor": [
            "Swelling in feet, ankles, or around eyes",
            "Changes in urination (frequency or color)",
            "Severe fatigue or weakness",
            "Nausea, vomiting, or loss of appetite"
        ]
    },
    
    # ==========================================
    # OTHER CONDITIONS
    # ==========================================
    
    "Food Allergy": {
        "general": [
            "Strictly avoid known allergens",
            "Read all food labels carefully",
            "Carry emergency epinephrine at all times",
            "Wear medical alert identification"
        ],
        "dos": [
            "Inform restaurants about your allergies",
            "Create an allergy action plan",
            "Train family/friends to use epinephrine",
            "Keep antihistamines available"
        ],
        "donts": [
            "Don't eat foods with unknown ingredients",
            "Never share food or utensils",
            "Don't delay using epinephrine if needed",
            "Avoid cross-contamination in kitchen"
        ],
        "consult_doctor": [
            "Any allergic reaction occurs",
            "Symptoms are becoming more severe over time",
            "You want allergy testing",
            "Emergency epinephrine was used"
        ]
    },
    
    "Dehydration": {
        "general": [
            "Drink fluids immediately - water or ORS",
            "Sip small amounts frequently if nauseous",
            "Rest in a cool environment",
            "Monitor for worsening symptoms"
        ],
        "dos": [
            "Drink oral rehydration solutions",
            "Eat water-rich foods (watermelon, cucumber)",
            "Replace electrolytes with sports drinks",
            "Check urine color - aim for pale yellow"
        ],
        "donts": [
            "Don't drink alcohol or caffeine",
            "Avoid very hot or strenuous activities",
            "Don't ignore symptoms of severe dehydration",
            "Avoid sugary drinks that can worsen dehydration"
        ],
        "consult_doctor": [
            "Unable to keep fluids down",
            "Dizziness, confusion, or fainting",
            "No urination for 8+ hours",
            "Rapid heartbeat or breathing"
        ]
    },
    
    "Heat Stroke": {
        "general": [
            "This is a medical emergency - call for help immediately",
            "Move to a cool, shaded area immediately",
            "Remove excess clothing",
            "Apply cool water to skin and fan"
        ],
        "dos": [
            "Call emergency services immediately",
            "Apply ice packs to neck, armpits, and groin",
            "Immerse in cool water if possible",
            "Monitor breathing and consciousness"
        ],
        "donts": [
            "Don't give fluids if person is unconscious",
            "Don't delay seeking emergency care",
            "Avoid ice-cold water immersion",
            "Don't leave person alone"
        ],
        "consult_doctor": [
            "Any suspected heat stroke is a medical emergency",
            "Body temperature above 104°F (40°C)",
            "Confusion or loss of consciousness",
            "Hot, dry skin without sweating"
        ]
    },
    
    "Glaucoma": {
        "general": [
            "Take eye drops exactly as prescribed",
            "Attend all eye appointments",
            "Protect eyes from injury",
            "Monitor peripheral vision changes"
        ],
        "dos": [
            "Use eye drops at the same time daily",
            "Keep head elevated when sleeping",
            "Inform all doctors about your glaucoma",
            "Exercise regularly (with doctor's approval)"
        ],
        "donts": [
            "Don't skip eye drop doses",
            "Avoid rubbing your eyes",
            "Don't lift heavy weights without guidance",
            "Avoid certain yoga positions that increase eye pressure"
        ],
        "consult_doctor": [
            "Sudden vision changes",
            "Severe eye pain or headache",
            "Halos around lights",
            "Nausea or vomiting with eye pain"
        ]
    }
}

# Default precautions for any disease not specifically listed
DEFAULT_PRECAUTIONS = {
    "general": [
        "Rest and allow your body time to recover",
        "Stay hydrated by drinking plenty of fluids",
        "Monitor your symptoms and note any changes",
        "Maintain good hygiene practices"
    ],
    "dos": [
        "Get adequate sleep",
        "Eat nutritious, balanced meals",
        "Take note of your symptoms for your doctor",
        "Follow any medical advice you've received"
    ],
    "donts": [
        "Don't ignore worsening symptoms",
        "Avoid self-medicating without proper guidance",
        "Don't delay seeking medical attention if concerned",
        "Avoid strenuous activities until you feel better"
    ],
    "consult_doctor": [
        "Symptoms persist or worsen over time",
        "You develop new or concerning symptoms",
        "You have underlying health conditions",
        "You're unsure about your condition"
    ]
}


# ============================================
# Advice Level Determination
# ============================================

def determine_advice_level(confidence: float, risk_level: str) -> str:
    """
    Determine the urgency level of advice based on confidence and risk.
    
    Returns: 'low', 'medium', or 'high'
    """
    if risk_level == "HIGH" or confidence < 0.3:
        return "high"
    elif risk_level == "MEDIUM" or confidence < 0.5:
        return "medium"
    else:
        return "low"


# ============================================
# Precaution Generation
# ============================================

def generate_precautions(
    disease: str,
    confidence: float,
    risk_level: str,
    user_name: str,
    previous_predictions: Optional[List] = None
) -> dict:
    """
    Generate personalized precautionary advice.
    
    Args:
        disease: Predicted disease name
        confidence: Model confidence (0-1)
        risk_level: Risk level (LOW/MEDIUM/HIGH)
        user_name: User's name for personalization
        previous_predictions: List of user's previous predictions (optional)
        
    Returns:
        Dictionary containing precautions and advice metadata
    """
    # Get disease-specific precautions or defaults
    precautions_data = DISEASE_PRECAUTIONS.get(disease, DEFAULT_PRECAUTIONS)
    
    # Determine advice level
    advice_level = determine_advice_level(confidence, risk_level)
    
    # Build personalized precautions list
    precautions_list = []
    
    # Add confidence-based opening advice
    confidence_percent = int(confidence * 100)
    
    if confidence < 0.3:
        precautions_list.append(
            f"⚠️ {user_name}, the prediction confidence is low ({confidence_percent}%). "
            "These suggestions are general guidelines. Please consult a healthcare professional "
            "for an accurate assessment."
        )
    elif confidence < 0.5:
        precautions_list.append(
            f"📋 {user_name}, based on your symptoms, here are some helpful suggestions. "
            f"The prediction confidence is moderate ({confidence_percent}%), so professional "
            "consultation is recommended."
        )
    else:
        precautions_list.append(
            f"💡 {user_name}, based on your symptoms analysis, here are personalized suggestions "
            "to help you feel better."
        )
    
    # Add general precautions
    precautions_list.extend(precautions_data["general"][:4])
    
    # Add risk-level specific advice
    if risk_level == "HIGH":
        precautions_list.append(
            "🏥 Given the risk assessment, we strongly recommend consulting a healthcare "
            "provider as soon as possible."
        )
    elif risk_level == "MEDIUM":
        precautions_list.append(
            "📞 If symptoms persist or worsen, consider scheduling a consultation with "
            "a healthcare provider."
        )
    
    # Check for recurring conditions in history
    if previous_predictions:
        same_disease_count = sum(
            1 for p in previous_predictions 
            if p.predicted_disease == disease
        )
        if same_disease_count >= 2:
            precautions_list.append(
                f"📊 We noticed you've had similar symptoms before. If this is a recurring "
                "issue, discussing it with a doctor may help identify underlying causes."
            )
    
    # Build structured response
    return {
        "advice_level": advice_level,
        "precautions": precautions_list,
        "dos": precautions_data["dos"][:4],
        "donts": precautions_data["donts"][:4],
        "consult_when": precautions_data["consult_doctor"][:4],
        "disclaimer": (
            "⚠️ DISCLAIMER: This advice is NOT a substitute for professional medical "
            "diagnosis, advice, or treatment. Always consult a qualified healthcare "
            "provider for medical concerns."
        )
    }


def format_precautions_for_storage(precautions_dict: dict) -> str:
    """
    Format precautions dictionary as a string for database storage.
    """
    lines = []
    lines.append(f"Advice Level: {precautions_dict['advice_level'].upper()}")
    lines.append("\nKey Recommendations:")
    for p in precautions_dict['precautions']:
        lines.append(f"• {p}")
    return "\n".join(lines)

disease_symptoms = {
    'Cold': {
        'symptoms': ['cough', 'sneezing', 'runny nose'],
        'doctor': 'General Practitioner'
    },
    'Flu': {
        'symptoms': ['fever', 'body aches', 'fatigue', 'cough'],
        'doctor': 'General Practitioner'
    },
    'Allergies': {
        'symptoms': ['itchy eyes', 'sneezing', 'nasal congestion'],
        'doctor': 'Allergist'
    },
    'COVID-19': {
        'symptoms': ['fever', 'cough', 'shortness of breath', 'loss of taste or smell'],
        'doctor': 'Infectious Disease Specialist'
    },
    'Migraine': {
        'symptoms': ['headache', 'nausea', 'sensitivity to light'],
        'doctor': 'Neurologist'
    },
    'Stomach Flu': {
        'symptoms': ['vomiting', 'diarrhea', 'abdominal pain', 'fatigue'],
        'doctor': 'Gastroenterologist'
    },
    'Sinusitis': {
        'symptoms': ['facial pain', 'sinus pressure', 'congestion'],
        'doctor': 'Otolaryngologist'
    }
}

def get_possible_diseases(symptoms):
    possible_diseases = []
    doctors = []
    for disease, data in disease_symptoms.items():
        disease_symptoms_list = data['symptoms']
        if any(symptom in symptoms for symptom in disease_symptoms_list):
            possible_diseases.append(disease)
            doctors.append(data['doctor'])
    return possible_diseases, doctors

def diagnose(symptoms):
    possible_diseases, doctors = get_possible_diseases(symptoms)
    if possible_diseases:
        diagnosis_results = []
        max_len = max(len(disease) for disease in possible_diseases)
        count = 1
        for disease, doctor in zip(possible_diseases, doctors):
            if count == 1:
                diagnosis_results.append(f"{disease:<{max_len}}\n         Doctor: {doctor}")
            else:
                diagnosis_results.append(f"         {disease:<{max_len}}\n         Doctor: {doctor}")
            count+=1
        return diagnosis_results
    else:
        return "No matching diseases found, try consulting a professional.\n         Do you want to book an appointment."

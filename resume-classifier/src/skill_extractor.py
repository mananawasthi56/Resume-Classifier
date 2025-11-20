
COMMON_SKILLS = ['python','pandas','numpy','scikit-learn','sql','power bi','excel',
                'tensorflow','pytorch','react','javascript','node','selenium','mongodb']

def extract_skills(text):
    text_low = text.lower()
    found = [s for s in COMMON_SKILLS if s in text_low]
    return found

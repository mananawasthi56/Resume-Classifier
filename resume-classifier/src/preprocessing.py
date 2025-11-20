
import re
def clean_text(s):
    s = s.lower()
    s = re.sub(r'[^a-z0-9\s]', ' ', s)
    s = ' '.join(s.split())
    return s

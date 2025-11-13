NCERT_BASE = "https://ncert.nic.in/textbook/pdf/"

def ncert_url(class_num, subject_code, chapter_num):
    code = f"{subject_code.lower()}{class_num:02d}{chapter_num:02d}"
    return f"{NCERT_BASE}{code}.pdf"
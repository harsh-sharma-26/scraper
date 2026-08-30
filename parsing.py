# Har field ke liye keywords ka SET banaya - set isliye kyunki
# "in" check set me list se bhi fast hota hai
GENDER_MALE = {"male", "man", "boy"}
GENDER_FEMALE = {"female", "woman", "girl"}
GENDER_OTHER = {"transgender", "other"}

URBAN_WORDS = {"urban", "city", "town"}
RURAL_WORDS = {"rural", "village", "gaon"}

# Sabhi states ek hi jagah rakho - dono single-word aur multi-word
INDIAN_STATES = [
    "andhra pradesh", "arunachal pradesh", "assam", "bihar", "chhattisgarh",
    "goa", "gujarat", "haryana", "himachal pradesh", "jharkhand", "karnataka",
    "kerala", "madhya pradesh", "maharashtra", "manipur", "meghalaya", "mizoram",
    "nagaland", "odisha", "punjab", "rajasthan", "sikkim", "tamil nadu",
    "telangana", "tripura", "uttar pradesh", "uttarakhand", "west bengal",
    "delhi", "jammu and kashmir", "ladakh"
]

CATEGORIES = {"general", "obc", "sc", "st", "ews"}

BPL_YES_WORDS = {"bpl"}
DISABLED_WORDS = {"disabled", "handicapped", "differently-abled", "differently"}
SENIOR_WORDS = {"senior"}


def process_words(words_list):
    # sab words ko lowercase kar diya, taaki "Male"/"MALE"/"male" sab match ho
    words = set(word.lower() for word in words_list)
    sentence = " ".join(words_list).lower()

    data = {
        "gender": None,
        "age": None,
        "area_of_residence": None,
        "state": None,
        "category": None,
        "bpl": None,
        "differently_abled": None,
        "senior_citizen": None
    }

    # ---- GENDER ----
    # set ka "&" operator intersection nikalta hai - dono me common elements
    if words & GENDER_MALE:          # agar koi bhi common word mila (empty set False hota hai)
        data["gender"] = "Male"
    elif words & GENDER_FEMALE:
        data["gender"] = "Female"
    elif words & GENDER_OTHER:
        data["gender"] = "Other"

    # ---- AGE ----
    # list me se ek-ek word check karenge - jo bhi pure number ho wo age hai
    for word in words_list:
        if word.isdigit():
            data["age"] = int(word)
            break

    # ---- AREA ----
    if words & URBAN_WORDS:
        data["area_of_residence"] = "Urban"
    elif words & RURAL_WORDS:
        data["area_of_residence"] = "Rural"

    # ---- STATE ----
    for state in INDIAN_STATES:
        if state in sentence:
            data["state"] = state.title()
            break

    # ---- CATEGORY ----
    common_cat = words & CATEGORIES
    if common_cat:
        data["category"] = common_cat.pop().upper()

    # ---- BPL ----
    if words & BPL_YES_WORDS:
        data["bpl"] = "Yes"

    # ---- DIFFERENTLY ABLED ----
    if words & DISABLED_WORDS:
        data["differently_abled"] = "Yes"

    # ---- SENIOR CITIZEN ----
    if words & SENIOR_WORDS:
        data["senior_citizen"] = "Yes"
    elif data["age"] is not None and data["age"] >= 60:
        data["senior_citizen"] = "Yes"

    return data

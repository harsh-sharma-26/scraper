import requests
import json
import os

# Config - agar key change ho to bas yaha update karo (ya .env file me daalo)
MYSCHEME_API_URL = "https://api.myscheme.gov.in/search/v6/schemes"
MYSCHEME_API_KEY = os.getenv("MYSCHEME_API_KEY", "tYTy5eEhlu9rFjyxuCr7ra7ACp4dv1RH8gWuHTDc")

# Hamare extracted fields ko myScheme ke expected identifiers/values se map karna padega
# kyunki hamara "OBC" myScheme ka poora naam expect kar sakta hai jaise "Other Backward Class (OBC)"
CATEGORY_MAP = {
    "GENERAL": "General",
    "OBC": "Other Backward Class (OBC)",
    "SC": "Scheduled Caste (SC)",
    "ST": "Scheduled Tribe (ST)",
    "EWS": "Economically Weaker Section (EWS)"
}

GENDER_MAP = {
    "Male": "Male",
    "Female": "Female",
    "Other": "Transgender"
}


def build_query_filters(user_data):
    """
    user_data (jo parsing.py se extract hua tha) ko myScheme ke expected
    filter format [{"identifier": ..., "value": ...}, ...] me convert karta hai
    """
    filters = []

    if user_data.get("gender"):
        mapped_gender = GENDER_MAP.get(user_data["gender"])
        if mapped_gender:
            filters.append({"identifier": "gender", "value": mapped_gender})

    if user_data.get("category"):
        mapped_category = CATEGORY_MAP.get(user_data["category"])
        if mapped_category:
            filters.append({"identifier": "caste", "value": mapped_category})

    if user_data.get("area_of_residence"):
        filters.append({"identifier": "residence", "value": user_data["area_of_residence"]})

    if user_data.get("state"):
        filters.append({"identifier": "beneficiaryState", "value": user_data["state"]})

    if user_data.get("differently_abled"):
        filters.append({"identifier": "disability", "value": user_data["differently_abled"]})

    if user_data.get("age"):
        age_str = str(user_data["age"])
        filters.append({"identifier": "age-st", "min": age_str, "max": age_str})

    return filters


def extract_scheme_summary(api_response):
    """
    Poore myScheme response me se schemes nikalta hai, "fields" wrapper ke
    andar hi rakhta hai - kyunki frontend template (templates/index.html)
    scheme.fields.schemeName, scheme.fields.briefDescription,
    scheme.fields.schemeCategory, scheme.fields.tags, scheme.fields.slug
    isi nested shape ko expect karti hai.
    """
    if not api_response:
        return []

    items = api_response.get("data", {}).get("hits", {}).get("items", [])

    summaries = []
    for item in items:
        fields = item.get("fields", {})

        summaries.append({
            "fields": {
                "schemeName": fields.get("schemeName", "Naam uplabdh nahi"),
                "briefDescription": fields.get("briefDescription", "Description uplabdh nahi"),
                "schemeCategory": fields.get("schemeCategory", []),
                "tags": fields.get("tags", []),
                "slug": fields.get("slug", "")
            }
        })

    return summaries


def fetch_matching_schemes(user_data, page_size=20):
    """
    Saare matching schemes fetch karta hai, pagination handle karte hue -
    ek-ek page maangta hai jab tak sab results mil na jayen.

    Return: list of {"fields": {...}} dictionaries (already processed,
    ready to pass directly to render_template).
    """
    filters = build_query_filters(user_data)
    query_json = json.dumps(filters)

    headers = {
        "accept": "application/json, text/plain, */*",
        "origin": "https://www.myscheme.gov.in",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "x-api-key": MYSCHEME_API_KEY
    }

    all_schemes = []
    current_from = 0

    while True:
        params = {
            "lang": "en",
            "q": query_json,
            "keyword": "",
            "sort": "",
            "from": current_from,
            "size": page_size
        }

        try:
            response = requests.get(MYSCHEME_API_URL, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            raw_data = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching page from={current_from}: {e}")
            break   # error aaye to jo abhi tak mila hai wahi return karo, poori list crash na ho

        page_schemes = extract_scheme_summary(raw_data)

        if not page_schemes:
            break   # is page pe kuch nahi mila, matlab sab schemes mil chuke

        all_schemes.extend(page_schemes)   # naye results ko list me jodo

        # total count nikalo response se, taaki pata chale kab rukna hai
        total_available = raw_data.get("data", {}).get("hits", {}).get("total", {}).get("value", 0)

        current_from += page_size

        if current_from >= total_available:
            break   # sab results mil chuke, loop band karo

    return all_schemes

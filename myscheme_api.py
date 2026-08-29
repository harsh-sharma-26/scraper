import requests
import json
import urllib.parse

import parsing

# Config - agar key change ho to bas yaha update karo
MYSCHEME_API_URL = "https://api.myscheme.gov.in/search/v6/schemes"
MYSCHEME_API_KEY = "tYTy5eEhlu9rFjyxuCr7ra7ACp4dv1RH8gWuHTDc"

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
    user_data (jo tumne extract kiya tha) ko myScheme ke expected
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

   # if user_data.get("area_of_residence"):
    #    filters.append({"identifier": "residence", "value": user_data["area_of_residence"]})

    if user_data.get("state"):
        filters.append({"identifier": "beneficiaryState", "value": user_data["state"]})

    if user_data.get("differently_abled"):
        filters.append({"identifier": "disability", "value": user_data["differently_abled"]})

   # if user_data.get("age"):
     #   age_str = str(user_data["age"])
      #  filters.append({"identifier": "age-st", "min": age_str, "max": age_str})

    return filters


def fetch_matching_schemes(user_data, page_size=10, page_from=0):
    """
    User ke data ke basis par MyScheme API se matching schemes laata hai.
    """

    filters = build_query_filters(user_data)
    print("\nFILTERS:")
    print(filters)

    query_json = json.dumps(filters)

    params = {
        "lang": "en",
        "q": query_json,
        "keyword": "",
        "sort": "",
        "from": page_from,
        "size": page_size
    }

    headers = {
        "accept": "application/json, text/plain, */*",
        "origin": "https://www.myscheme.gov.in",
        "user-agent": "Mozilla/5.0",
        "x-api-key": MYSCHEME_API_KEY
    }

    try:
        response = requests.get(
            MYSCHEME_API_URL,
            headers=headers,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        print("\n========== API RESPONSE ==========")
        print(json.dumps(data, indent=2))
        print("==================================")

        return data

    except requests.exceptions.HTTPError as e:
        print(f"API ne error diya: {e}")
        return None

    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
        return None
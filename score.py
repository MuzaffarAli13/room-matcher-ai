# import json
# from agents import function_tool

# @function_tool
# def get_match_data_with_score(
#     city: str,
#     area: str,
#     budget_PKR: int,
#     cleanliness: str,
#     noise_tolerance: str,
#     study_habits: str,
#     food_pref: str,
#     sleep_schedule
# ):
#     """
#     User ke preferences aur profiles.json ke data ko score system ke sath match karega.
#     Score = % match of fields. Profiles ko descending order me return karega.
#     """
#     try:
#         with open("profiles.json", "r", encoding="utf-8") as file:
#             profiles = json.load(file)
#     except FileNotFoundError:
#         return {"error": "profiles.json file nahi mili."}
#     except json.JSONDecodeError:
#         return {"error": "profiles.json valid JSON nahi hai."}

#     user_input = {
#         "city": city,
#         "area": area,
#         "budget_PKR": budget_PKR,
#         "cleanliness": cleanliness,
#         "noise_tolerance": noise_tolerance,
#         "study_habits": study_habits,
#         "food_pref": food_pref,
#         "sleep_schedule": sleep_schedule,
#     }

#     matched_profiles = []

#     for profile in profiles:
#         total_fields = 0
#         matched_fields = 0

#         for key, value in user_input.items():
#             if value is not None:  # sirf wahi field check karni jo user ne di hai
#                 total_fields += 1
#                 if str(profile.get(key)).lower() == str(value).lower():
#                     matched_fields += 1

#         if total_fields > 0:
#             score = int((matched_fields / total_fields) * 100)
#             matched_profiles.append({
#                 "profile": profile,
#                 "score": score
#             })

#     # Profiles ko score ke hisaab se sort karna
#     matched_profiles.sort(key=lambda x: x["score"], reverse=True)

#     return matched_profiles if matched_profiles else {"message": "Koi matching profile nahi mili."}


import json
from agents import function_tool

@function_tool
def get_match_data_with_score(
    city: str,
    area: str,
    budget_PKR: int,
    cleanliness: str,
    noise_tolerance: str,
    study_habits: str,
    food_pref: str,
    sleep_schedule: str
):
    """
    User ke preferences aur profiles.json ke data ko score system ke sath match karega.
    Score = % match of fields. Profiles ko descending order me return karega.
    Sirf Top 3 matches return honge.
    """
    try:
        with open("profiles.json", "r", encoding="utf-8") as file:
            profiles = json.load(file)
    except FileNotFoundError:
        return {"error": "profiles.json file nahi mili."}
    except json.JSONDecodeError:
        return {"error": "profiles.json valid JSON nahi hai."}

    user_input = {
        "city": city,
        "area": area,
        "budget_PKR": budget_PKR,
        "cleanliness": cleanliness,
        "noise_tolerance": noise_tolerance,
        "study_habits": study_habits,
        "food_pref": food_pref,
        "sleep_schedule": sleep_schedule,
    }

    matched_profiles = []

    for profile in profiles:
        total_fields = 0
        matched_fields = 0

        for key, value in user_input.items():
            if value is not None:  # sirf wahi field check karni jo user ne di hai
                total_fields += 1
                if str(profile.get(key)).lower() == str(value).lower():
                    matched_fields += 1

        if total_fields > 0:
            score = int((matched_fields / total_fields) * 100)
            matched_profiles.append({
                "profile": profile,
                "score": score
            })

    # Profiles ko score ke hisaab se sort karna
    matched_profiles.sort(key=lambda x: x["score"], reverse=True)

    # Sirf top 3 results return karna
    top_matches = matched_profiles[:3]

    return top_matches if top_matches else {"message": "Koi matching profile nahi mili."}

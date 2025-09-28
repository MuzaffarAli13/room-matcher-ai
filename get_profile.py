# import json
# from agents import function_tool

# @function_tool
# def load_json_data():
#     """
#     JSON file se data read karke Python list/dict return karega.
    
#     """
#     try:
#         with open("profiles.json", "r", encoding="utf-8") as file:
#             data = json.load(file)
#             return data
#     except FileNotFoundError:
#         print(f"Error: File  nahi mili.")
#         return None
#     except json.JSONDecodeError:
#         print(f"Error: File valid JSON nahi hai.")
#         return None

# load_json_data()

# correct
# tool start
 
import json
from agents import function_tool

@function_tool
def get_match_profiles(
    city: str,
    area: str,
    budget_PKR: int,
    cleanliness: str,
    noise_tolerance: str,
    study_habits: str,
    food_pref: str
):
    """
    User ke diye gaye preferences ko profiles.json ke against match karega.
    Jo profiles match hongi unhe return karega.
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
    }

    # Filter profiles based on input
    matched_profiles = []
    for profile in profiles:
        is_match = True
        for key, value in user_input.items():
            if value is not None:  # sirf wahi fields check karo jo user ne bheji hain
                if str(profile.get(key)).lower() != str(value).lower():
                    is_match = False
                    break
        if is_match:
            matched_profiles.append(profile)

    return matched_profiles if matched_profiles else {"message": "Koi matching profile nahi mili."}

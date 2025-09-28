import json
from agents import function_tool

@function_tool
def get_red_flags_only(
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
    Sirf Red Flags detect karega between user input aur profiles.json.
    - Har profile ke liye red_flags list return karega.
    - Score ya sorting include nahi hogi.
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

    # Red Flag Rules
    def detect_red_flags(user, profile):
        red_flags = []

        # Cleanliness conflict
        if user["cleanliness"].lower() != profile.get("cleanliness", "").lower():
            red_flags.append("Cleanliness mismatch")

        # Sleep schedule conflict
        if user["sleep_schedule"].lower() != profile.get("sleep_schedule", "").lower():
            red_flags.append("Sleep schedule conflict")

        # Noise tolerance conflict
        if (
            user["noise_tolerance"].lower() == "quiet"
            and profile.get("noise_tolerance", "").lower() != "quiet"
        ):
            red_flags.append("Noise tolerance mismatch")

        # Study habit conflict
        if (
            user["study_habits"].lower().startswith("late-night")
            and user["sleep_schedule"].lower() == "early bird"
        ):
            red_flags.append("Study habit conflict")

        return red_flags

    results = []

    for profile in profiles:
        red_flags = detect_red_flags(user_input, profile)
        results.append({
            "profile": profile,
            "red_flags": red_flags
        })

    return results if results else {"message": "Koi red flags detect nahi hue."}

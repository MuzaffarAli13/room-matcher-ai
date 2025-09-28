import json
from agents import function_tool


@function_tool
def get_room_matches(
    city: str,
    area: str,
    monthly_rent_PKR: int,
    rooms_available: int,
    amenities: list,
):
    """
    Will match the user-provided room preferences against profiles.json.
    Returns the rooms that match.
    If no exact match is found → returns the top 3 closest matches along with their scores.
    """

    try:
        with open("rooms.json", "r", encoding="utf-8") as file:
            rooms = json.load(file)
    except FileNotFoundError:
        return {"error": "profiles.json file nahi mili."}
    except json.JSONDecodeError:
        return {"error": "profiles.json valid JSON nahi hai."}

    user_input = {
        "city": city.lower(),
        "area": area.lower(),
        "monthly_rent_PKR": monthly_rent_PKR,
        "rooms_available": rooms_available,
        "amenities": [a.lower() for a in amenities],
        
    }

    exact_matches = []
    near_matches = []

    for room in rooms:
        room_city = room.get("city", "").lower()
        room_area = room.get("area", "").lower()
        room_rent = room.get("monthly_rent_PKR", 0)
        room_rooms = room.get("rooms_available", 0)
        room_avail = room.get("availability", "").lower()
        room_amenities = [a.lower() for a in room.get("amenities", [])]

        match_score = 0
        total_fields = 5 + len(user_input["amenities"])  # city, area, rent, rooms, availability + amenities

        # Exact field checks
        if room_city == user_input["city"]:
            match_score += 1
        if room_area == user_input["area"]:
            match_score += 1
        if room_rent == user_input["monthly_rent_PKR"]:
            match_score += 1
        if room_rooms == user_input["rooms_available"]:
            match_score += 1
        

        # Amenities check
        amenity_matches = sum([1 for a in user_input["amenities"] if a in room_amenities])
        match_score += amenity_matches

        score_percent = int((match_score / total_fields) * 100)

        if score_percent == 100:
            exact_matches.append(room)
        else:
            near_matches.append({"room": room, "score": score_percent})

    # Sort near matches by score descending
    near_matches.sort(key=lambda x: x["score"], reverse=True)

    if exact_matches:
        return exact_matches
    elif near_matches:
        return near_matches[:3]  # top 3 near matches
    else:
        return {"message": "Koi matching room nahi mila."}


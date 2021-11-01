attribute_mapping = {
    "email": "email address",
    "address": "location",
    "contactNumber": "phone number",
    "fbProfileLink": "Facebook profile",
    "instaProfileLink": "Instagram Profile",
    "twitterHandle": "Twitter Account",
    "youtubeAccount": "Youtube Account",
    "roomNumber": "room number",
    "designation": "designation",
    "ServiceType": "service type",
    "entryTime": "entry time",
    "exitTime": "exit time",
    "openingTime": "opening time",
    "closingTime": "closing time",
    "blockName": "block name",
    "servicesOffered": "offered services",
    "offeredPrograms": "programs offered",
    "academicBlocks": "academic blocks",
    "studentClubs": "student clubs",
    "name": "name",
    "contactEmail": "email address",
    "description": "description",
}


def resolve_message(results=None, intent=None, attribute=None, name=None):
    if intent is None or results is None:
        text = "Sorry I could not find what you are looking for. I  can only answer the questions \
                        provided to me. Maybe you should ask them. Sorry that I couldn't help you."
    if intent == "school_info":
        if attribute == "offeredPrograms":
            text = f"The {attribute_mapping[attribute]} are : \n"
            for p in results:
                text = text + p + "\n"
        else:
            text = f"Your school {attribute_mapping[attribute]} is {results}."
    if intent == "teacher_info":
        text = f"The {attribute_mapping[attribute]} of the {name} sir is {results}"

    return text


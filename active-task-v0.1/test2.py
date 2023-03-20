import requests
import json

token = 'secret_Rs800ockGMwCwW6w7SY34v9m2QXtFCkeuqleS77U8Pb'

# databaseId = '614f2195f4ee4c9b8db9b232b8d53948'

# headers = {
#     "Authorization": "Bearer " + token,
#     "Content-Type": "application/json",
#     "Notion-Version": "2021-05-13"
# }

# Read a Database - prints Name and Note.
selectedLog = {"no log item selected."}


def readDatabase():
    query_url = f"https://api.notion.com/v1/databases/614f2195f4ee4c9b8db9b232b8d53948/query"
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": "2021-08-16",
        "Content-Type": "application/json",
    }
    query_params = {
        "sorts": [
            {
                "property": "Created time",
                "direction": "descending"
            }
        ],
        "page_size": 1
    }

    response = requests.post(query_url, headers=headers, json=query_params)
    data = response.json()

    if response.status_code == 200:
        if data.get("results"):
            latest_entry = data["results"][0]
            name = latest_entry["properties"]["Name"]["title"][0]["text"]["content"]
            note = latest_entry["properties"]["Note"]["rich_text"][0]["text"]["content"]
            selectedLog = name
            print(f"Name: {name}")
            print(f"Note: {note}")
        else:
            print("No results found")
    else:
        print(f"Request failed with {response.status_code} - {response.text}")

    with open('./db.json', 'w', encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False)


readDatabase()

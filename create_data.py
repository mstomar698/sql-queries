import requests
import json

url = "https://bp-production.up.railway.app/api/books/addbook"
book_json = [
    {
        "name": "Where the Crawdads Sing",
        "author": "Delia Owens",
        "yearRelease": 2018,
        "genre": "Fiction",
        "description": "A coming-of-age story of a young girl who lives alone in the marshes of North Carolina and becomes a murder suspect.",
        "coverImage": "https://th.bing.com/th/id/OIP.VGzMpW9v5zHmbogJkez2NgHaLL?pid=ImgDet&rs=1",
        "price": 11.00
    },
    {
        "name": "The Midnight Library",
        "author": "Matt Haig",
        "yearRelease": 2020,
        "genre": "Fantasy",
        "description": "A novel about a woman who finds herself in a library where she can explore the lives she could have lived if she had made different choices.",
        "coverImage": "https://upload.wikimedia.org/wikipedia/en/8/87/The_Midnight_Library.jpg",
        "price": 13.29
    },
    {
        "name": "The Vanishing Half",
        "author": "Brit Bennett",
        "yearRelease": 2020,
        "genre": "History",
        "description": "A saga of twin sisters who grow up in a black community in the South and choose to live very different lives, one as white and one as black.",
        "coverImage": "https://upload.wikimedia.org/wikipedia/en/e/ed/The_Vanishing_Half_%28Brit_Bennett%29.png",
        "price": 16.20
    },
    {
        "name": "The Silent Patient",
        "author": "Alex Michaelides",
        "yearRelease": 2019,
        "genre": "Thriller",
        "description": "A debut novel about a famous painter who shoots her husband and never speaks again, and the psychotherapist who tries to unravel her mystery.",
        "coverImage": "https://upload.wikimedia.org/wikipedia/en/d/df/The_Silent_Patient_early_2019_UK_edition.png",
        "price": 13.48
    },
    {
        "name": "Educated",
        "author": "Tara Westover",
        "yearRelease": 2018,
        "genre": "Memoir",
        "description": "A memoir of a young woman who grew up in a survivalist family in Idaho and went on to earn a PhD from Cambridge University.",
        "coverImage": "https://th.bing.com/th/id/OIP.hgnz4THaWJNiml-YG0DXFQHaLX?pid=ImgDet&rs=1",
        "price": 12.99
    },
]
headers = {
    'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2NTFmMGI1ZmI0NDUyMzU0MzBlNjIwODYiLCJuYW1lIjoiYWRtaW4iLCJlbWFpbCI6ImFkbWluQGFkbWluLmNvbSIsImlzQWRtaW4iOnRydWUsImlhdCI6MTY5NjUzMzQyMywiZXhwIjoxNjk3MTM4MjIzfQ.h5nASdPZaoaHIFCKdM2RRHBYhean5xOaYbLNgoAgkx4',
    'Content-Type': 'application/json'
}
for book_data in book_json:
    payload = json.dumps(book_data)
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)

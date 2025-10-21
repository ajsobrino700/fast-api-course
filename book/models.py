class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating


BOOKS = [
    Book(
        id=1,
        title="The selfish gene",
        author="Richard Dawkins",
        description="Holy shit",
        rating=7,
    ),
    Book(
        id=2,
        title="Fast API",
        author="Colombian Guy",
        description="Good framework",
        rating=5,
    ),
    Book(
        id=3,
        title="Introduction to Algorithms",
        author="Four guys",
        description="The best book, it is the bible",
        rating=10,
    ),
    Book(
        id=4,
        title="Crafting Interpreters",
        author="Robert Nystrom",
        description="A little practical introduction to interpreters",
        rating=8,
    ),
]

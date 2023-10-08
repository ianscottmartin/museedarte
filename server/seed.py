from faker import Faker
from models import User, Artist, Museum, Review
from config import db, app, bcrypt

faker = Faker()

# Seeding Users
with app.app_context():
    User.query.delete()

    for _ in range(20):
        username = faker.profile(fields=["username"])["username"]
        password = faker.password()
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        user = User(
            username=username,
            password_hash=hashed_password
        )

        db.session.add(user)

    db.session.commit()

# Seeding Artists, Museums, and Reviews
with app.app_context():
    # Create artists with specific names
    artists = [
        Artist(name="Vincent van Gogh"),
        Artist(name="Leonardo da Vinci"),
        Artist(name="Rembrandt van Rijn"),
        Artist(name="Pablo Picasso"),
        Artist(name="Claude Monet"),
        Artist(name="Mary Cassatt")
    ]

    # Create museums with specific names
    museums = [
        Museum(name="Musee D'Orsay"),
        Museum(name="Louvre"),
        Museum(name="National Gallery"),
        Museum(name="Denver Art Museum"),
        Museum(name="Art Institute"),
        Museum(name="Rijksmuseum")
    ]

    # Create reviews associated with artists and museums
    reviews = [
        Review(text="A masterpiece by Vincent van Gogh at Musee D'Orsay", artist=artists[0], museum=museums[0]),
        Review(text="Leonardo da Vinci's artwork is unparalleled at the Louvre", artist=artists[1], museum=museums[1]),
        Review(text="Rembrandt van Rijn's collection at the National Gallery is impressive", artist=artists[2], museum=museums[2]),
        Review(text="Pablo Picasso's unique style at Denver Art Museum is captivating", artist=artists[3], museum=museums[3]),
        Review(text="Claude Monet's impressionism at Art Institute is a must-see", artist=artists[4], museum=museums[4]),
        Review(text="Mary Cassatt's works at Rijksmuseum are delightful", artist=artists[5], museum=museums[5])
    ]

    # Add objects to the session and commit to the database
    db.session.add_all(artists)
    db.session.add_all(museums)
    db.session.add_all(reviews)
    db.session.commit()

print("Database seeded successfully with users, artists, museums, and reviews.")

from flask import Flask, request, session
import random
import collections

app = Flask(__name__)
app.secret_key = "your_secret_key_here"



def Auto_num():
    return random.randint(100, 999)


def bulls_cows(secret, user_input):
    secret = str(secret)
    guess = str(user_input)

    bulls = sum(x == y for x, y in zip(secret, guess))

    secret_counts = collections.Counter(secret)
    guess_counts = collections.Counter(guess)

    overlaps = 0
    for digit in secret_counts:
        if digit in guess_counts:
            overlaps += min(secret_counts[digit], guess_counts[digit])

    cows = overlaps - bulls
    return bulls, cows


@app.route("/", methods=["GET", "POST"])
def play_game():
    # Start new game if not already started
    if "secret" not in session:
        session["secret"] = Auto_num()
        session["attempts"] = 0

    secret = session["secret"]
    attempts = session["attempts"]
    message = ""

    if request.method == "POST":
        
        user_input = request.form.get("guess", "")

        if not user_input.isdigit() or len(user_input) != 3:
            message = "Enter a valid 3-digit number!"
        else:
            attempts += 1
            session["attempts"] = attempts

            bulls, cows = bulls_cows(secret, user_input)
            message = f"Bulls: {bulls}, Cows: {cows}"

            if bulls == 3:
                message += f"<br><br>🎉 You WON! The number was {secret}. Restarting..."
                session.clear()

            elif attempts >= 3:
                message += f"<br><br>❌ Attempts over! The number was {secret}. Restarting..."
                session.clear()

    # Simple inline HTML form
    return f"""
        <h2>Bulls & Cows Game</h2>
        
        <p>Attempt: {attempts}/3</p>
        <p> secret number {secret}</p>
        <form method="POST">
            
            <label>Enter a 3-digit number:</label><br>
            <input type="text" name="guess" maxlength="3" required>
            <button type="submit">Submit</button>
        </form>

        <p>{message}</p>
    """


if __name__ == "__main__":
    app.run(debug=True)
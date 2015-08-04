from flask import Flask, request, redirect
import twilio.twiml

app = Flask(__name__)

# Try adding your own number to this list!
callers = {
    "+16503841769": "Jesica",
    "+12672502802": "Viola",
}


@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
    """Say a caller's name, and play an MP3 for them."""
    from_number = request.values.get('From', None)
    if from_number in callers:
        caller = callers[from_number]
    else:
        caller = "Monkey"

    resp = twilio.twiml.Response()
    # Greet the caller by name
    resp.say("Hello " + caller)
    # Play an MP3
    resp.play("http://demo.twilio.com/hellomonkey/monkey.mp3")

    with resp.gather(numDigits=1, action="/handle-key", method="POST") as g:
        g.say("""To speak to a real monkey, press 1.
                 Press 2 to record your own monkey howl.
                 Press any other key to start over.""")

    # Say a command, and listen for the caller to press a key. When they press
    # a key, redirect them to /handle-key.
    with resp.gather(numDigits=1, action="/handle-key", method="POST") as g:
        g.say("To speak to the creator of this app, press 1. Press any other key to start over.")

    return str(resp)


@app.route("/handle-key", methods=['GET', 'POST'])
def handle_key():
    """Handle key press from a user."""

    # Get the digit pressed by the user
    digit_pressed = request.values.get('Digits', None)
    if digit_pressed == "1":
        resp = twilio.twiml.Response()
        # Dial (310) 555-1212 - connect that number to the incoming caller.
        resp.dial("+12672502802")
        # If the dial fails:
        resp.say("The call failed, or the remote party hung up. Goodbye.")

        return str(resp)

    elif digit_pressed == "2":
        resp = twilio.twiml.Response()
        resp.say("Record your monkey howl after the tone.")
        resp.record(maxLength="30", action="/handle-recording")
        return str(resp)

    # If the caller pressed anything but 1, redirect them to the homepage.
    else:
        return redirect("/")


@app.route("/handle-recording", methods=['GET', 'POST'])
def handle_recording():
    """Play back the caller's recording."""

    recording_url = request.values.get("RecordingUrl", None)

    resp = twilio.twiml.Response()
    resp.say("Thanks for howling... take a listen to what you howled.")
    resp.play(recording_url)
    resp.say("Goodbye.")
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)

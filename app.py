from flask import Flask, render_template, request
from analyzer import analyze_ssh_log

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 1 * 1024 * 1024  # max 1 MB upload


@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    error = None

    if request.method == "POST":
        if request.form.get("use_sample"):
            with open("sample_logs/auth.log", encoding="utf-8") as f:
                text = f.read()
            result = analyze_ssh_log(text)
        else:
            file = request.files.get("logfile")
            if not file or file.filename == "":
                error = "Please select a log file first."
            else:
                text = file.read().decode("utf-8", errors="ignore")
                result = analyze_ssh_log(text)

    return render_template("index.html", result=result, error=error)


if __name__ == "__main__":
    app.run(debug=True)
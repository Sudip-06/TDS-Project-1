from flask import Flask, request, jsonify
import os
import subprocess

app = Flask(__name__)
DATA_DIR = "/data"

# Security: Ensure we only access files within /data
def is_safe_path(path):
    abs_path = os.path.abspath(path)
    return abs_path.startswith(os.path.abspath(DATA_DIR))

@app.route("/run", methods=["POST"])
def run_task():
    task = request.args.get("task", "").strip()
    if not task:
        return jsonify({"error": "Task description is required"}), 400
    
    try:
        result = execute_task(task)
        return jsonify({"message": "Task executed successfully", "result": result}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

@app.route("/read", methods=["GET"])
def read_file():
    file_path = request.args.get("path", "").strip()
    if not file_path or not is_safe_path(file_path):
        return jsonify({"error": "Invalid or unsafe file path"}), 400
    
    if not os.path.exists(file_path):
        return "", 404
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    return content, 200, {"Content-Type": "text/plain"}

# Task execution logic
def execute_task(task):
    if "count the number of Wednesdays" in task.lower():
        return count_wednesdays("/data/dates.txt", "/data/dates-wednesdays.txt")
    elif "sort contacts" in task.lower():
        return sort_contacts("/data/contacts.json", "/data/contacts-sorted.json")
    elif "extract email sender" in task.lower():
        return extract_email_sender("/data/email.txt", "/data/email-sender.txt")
    else:
        raise ValueError("Unsupported task")

# Example task functions
def count_wednesdays(input_file, output_file):
    import datetime
    if not os.path.exists(input_file):
        raise ValueError("Input file does not exist")
    
    with open(input_file, "r", encoding="utf-8") as f:
        dates = [line.strip() for line in f.readlines()]
    
    wednesdays = sum(1 for date in dates if datetime.datetime.strptime(date, "%Y-%m-%d").weekday() == 2)
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(str(wednesdays))
    return f"Wednesdays counted: {wednesdays}"

def sort_contacts(input_file, output_file):
    import json
    if not os.path.exists(input_file):
        raise ValueError("Input file does not exist")
    
    with open(input_file, "r", encoding="utf-8") as f:
        contacts = json.load(f)
    
    sorted_contacts = sorted(contacts, key=lambda c: (c.get("last_name", ""), c.get("first_name", "")))
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(sorted_contacts, f, indent=2)
    return "Contacts sorted successfully"

def extract_email_sender(input_file, output_file):
    from openai import OpenAI
    if not os.path.exists(input_file):
        raise ValueError("Input file does not exist")
    
    with open(input_file, "r", encoding="utf-8") as f:
        email_content = f.read()
    
    client = OpenAI(api_key=os.environ.get("AIPROXY_TOKEN"))
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "Extract only the sender's email address from this email:"},
                  {"role": "user", "content": email_content}]
    )
    sender_email = response.choices[0].message.content.strip()
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(sender_email)
    return f"Sender email extracted: {sender_email}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

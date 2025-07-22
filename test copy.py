import subprocess

def ask_gemini(prompt: str) -> str:
    process = subprocess.Popen(
        [r"C:\Users\user\AppData\Roaming\npm\gemini.cmd"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8"
    )

    stdout, stderr = process.communicate(prompt)

    if stderr:
        print("エラー:", stderr)
    return stdout

# 日常会話プロンプトに変更
user_prompt = "明日の神奈川県川崎市の天気を教えてください。"
response = ask_gemini(user_prompt)

print("Geminiの回答:\n", response)
from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from fastapi.responses import HTMLResponse

app = FastAPI()

VERIFY_TOKEN = "my_instagram_verify_123"


@app.get("/webhook")
async def verify_webhook(request: Request):
    params = request.query_params

    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return PlainTextResponse(challenge)

    return PlainTextResponse("Verification failed", status_code=403)


@app.post("/webhook")
async def receive_webhook(request: Request):
    data = await request.json()

    print("WEBHOOK:", data)

    for entry in data.get("entry", []):
        for change in entry.get("changes", []):
            if change.get("field") == "comments":
                value = change.get("value", {})
                comment_text = value.get("text", "")
                username = value.get("from", {}).get("username", "")

                print("================================")
                print("USERNAME:", username)
                print("COMMENT:", comment_text)
                print("================================")

                if comment_text.strip() == "+":
                    print(">>> PLUS COMMENT TOPILDI!")

    return {"status": "ok"}


@app.get("/oauth/callback", response_class=HTMLResponse)
async def oauth_callback():
    return """
    <!DOCTYPE html>
    <html>
    <body>
        <h2>Instagram ulanishi yakunlandi</h2>
        <p id="status">Token tekshirilmoqda...</p>

        <script>
            const params = new URLSearchParams(
                window.location.hash.substring(1)
            );

            const token = params.get("access_token");

            if (token) {
                document.getElementById("status").innerText =
                    "Access Token olindi! Tokenni hech kimga yubormang.";
                console.log("Access Token:", token);
            } else {
                document.getElementById("status").innerText =
                    "Access Token topilmadi.";
            }
        </script>
    </body>
    </html>
    """
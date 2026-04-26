import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def page1():
    return """
    <html>
        <body>
            <h1>Page 1: Personal Info</h1>
            <form action="/page2" method="get">
                <input type="text" name="full_name" placeholder="Full Name"><br>
                <input type="email" name="email" placeholder="Email"><br>
                <button type="submit">Next</button>
            </form>
        </body>
    </html>
    """

@app.get("/page2", response_class=HTMLResponse)
async def page2():
    return """
    <html>
        <body>
            <h1>Page 2: Final Step</h1>
            <form action="/success" method="get">
                <input type="text" name="phone" placeholder="Phone"><br>
                <button type="submit">Submit Application</button>
            </form>
        </body>
    </html>
    """

@app.get("/success", response_class=HTMLResponse)
async def success():
    return """
    <html>
        <body>
            <h1>Thank you!</h1>
            <p>Your application has been submitted successfully.</p>
        </body>
    </html>
    """

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)

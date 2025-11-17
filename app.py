import asyncio
from flask import Flask, request, send_file, render_template
from pyppeteer import launch
import io

app = Flask(__name__)

browser = None

async def launch_browser():
    global browser
    browser = await launch(handleSIGINT=False, handleSIGTERM=False, handleSIGHUP=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/screenshot')
async def screenshot():
    url = request.args.get('url')
    if not url:
        return 'Missing url query parameter', 400

    try:
        page = await browser.newPage()
        await page.goto(url)
        screenshot_bytes = await page.screenshot({'type': 'png'})
        await page.close()
    except Exception as e:
        return f"Error taking screenshot: {e}", 500

    return send_file(
        io.BytesIO(screenshot_bytes),
        mimetype='image/png'
    )

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(launch_browser())
    app.run(debug=True)

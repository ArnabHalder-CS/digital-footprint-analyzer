import webview

APP_URL = "https://digital-footprint-analyzer-2e3w.onrender.com"

webview.create_window(
    "Digital Footprint Analyzer",
    APP_URL,
    width=1400,
    height=900,
    resizable=True
)

webview.start()
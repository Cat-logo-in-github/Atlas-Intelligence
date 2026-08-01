import subprocess
import time
import win32con

import requests
from playwright.sync_api import sync_playwright


EDGE_PATH = (
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
)

PROFILE_PATH = (
    r"D:\Projects\Active\atlas-intelligence\edge-profile"
)

PORT = 9222

_edge_process = None
_playwright = None
_browser = None


# ============================================================
# Edge startup
# ============================================================

def start_edge():

    # Already running?
    try:

        response = requests.get(
            f"http://localhost:{PORT}/json/version",
            timeout=1
        )

        if response.status_code == 200:
            return

    except requests.ConnectionError:
        pass


    global _edge_process

    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = win32con.SW_MINIMIZE


    _edge_process = subprocess.Popen(
        [
            EDGE_PATH,
            "--no-first-run",
            "--no-default-browser-check",
            "--disable-session-crashed-bubble",
            f"--remote-debugging-port={PORT}",
            f"--user-data-dir={PROFILE_PATH}",
        ],
        startupinfo=startupinfo,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


    for _ in range(30):

        try:

            response = requests.get(
                f"http://localhost:{PORT}/json/version"
            )

            if response.status_code == 200:
                return

        except requests.ConnectionError:
            pass

        time.sleep(1)


    raise RuntimeError(
        "Edge did not start."
    )


# ============================================================
# Browser connection
# ============================================================

def get_browser():

    global _playwright
    global _browser


    if _browser:

        return _browser


    start_edge()


    _playwright = sync_playwright().start()

    _browser = _playwright.chromium.connect_over_cdp(
        f"http://localhost:{PORT}"
    )


    return _browser


# ============================================================
# Pages
# ============================================================

def get_edge_page(reuse=True):
    browser = get_browser()
    context = browser.contexts[0]

    if reuse:
        for page in context.pages:
            if not page.is_closed():
                return page

    return context.new_page()

def stabilize_page(page):

    page.bring_to_front()

    page.wait_for_timeout(
        3000
    )

    page.mouse.move(
        500,
        300
    )

    page.wait_for_timeout(
        1000
    )

import win32gui
import win32con
def minimize_edge():

    def callback(hwnd, _):

        title = win32gui.GetWindowText(hwnd)

        if "Edge" in title:
            win32gui.ShowWindow(
                hwnd,
                win32con.SW_MINIMIZE
            )

    win32gui.EnumWindows(
        callback,
        None
    )

def close_edge_page(page):

    try:

        page.close()

    except Exception:

        pass


# ============================================================
# Cleanup
# ============================================================

def shutdown_browser():

    global _browser
    global _playwright
    global _edge_process


    try:
        if _browser:
            _browser.close()

    except Exception:
        pass


    try:
        if _playwright:
            _playwright.stop()

    except Exception:
        pass


    try:
        if _edge_process:
            _edge_process.wait(timeout=10)

    except subprocess.TimeoutExpired:

        _edge_process.terminate()


    _browser = None
    _playwright = None
    _edge_process = None
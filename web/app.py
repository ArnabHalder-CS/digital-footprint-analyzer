from flask import Flask, render_template, request, jsonify
import requests
from datetime import datetime


app = Flask(__name__)


# =========================================================
# PLATFORM DATABASE
# =========================================================

PLATFORMS = [
    {
        "name": "GitHub",
        "url": "https://github.com/{}"
    },
    {
        "name": "Reddit",
        "url": "https://www.reddit.com/user/{}"
    },
    {
        "name": "GitLab",
        "url": "https://gitlab.com/{}"
    },
    {
        "name": "Pinterest",
        "url": "https://www.pinterest.com/{}/"
    },
    {
        "name": "Twitch",
        "url": "https://www.twitch.tv/{}"
    },
    {
        "name": "Medium",
        "url": "https://medium.com/@{}"
    },
    {
        "name": "Dev.to",
        "url": "https://dev.to/{}"
    },
    {
        "name": "CodePen",
        "url": "https://codepen.io/{}"
    }
]


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")
def home():

    return render_template("index.html")


# =========================================================
# PWA SERVICE WORKER
# =========================================================

@app.route("/sw.js")
def service_worker():

    return app.send_static_file("sw.js")


# =========================================================
# USERNAME SCANNER
# =========================================================

@app.route("/api/scan", methods=["POST"])
def scan():

    try:

        data = request.get_json(silent=True) or {}

        username = str(
            data.get("username", "")
        ).strip()


        # -----------------------------
        # VALIDATION
        # -----------------------------

        if not username:

            return jsonify({
                "success": False,
                "message": "Username is required."
            }), 400


        if len(username) > 50:

            return jsonify({
                "success": False,
                "message": "Username is too long."
            }), 400


        results = []


        # -----------------------------
        # PLATFORM SCAN
        # -----------------------------

        headers = {
            "User-Agent": (
                "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/151.0 Safari/537.36"
            )
        }


        for platform in PLATFORMS:

            profile_url = platform["url"].format(
                username
            )


            try:

                response = requests.get(
                    profile_url,
                    timeout=8,
                    headers=headers,
                    allow_redirects=True
                )


                code = response.status_code


                if code == 200:

                    status = "FOUND"


                elif code in [401, 403, 429]:

                    status = "BLOCKED"


                elif code == 404:

                    status = "NOT FOUND"


                else:

                    status = "UNABLE"


            except requests.RequestException:

                code = 0
                status = "UNABLE"


            results.append({

                "platform": platform["name"],

                "status": status,

                "code": code,

                "url": profile_url

            })


        # -----------------------------
        # STATISTICS
        # -----------------------------

        total = len(results)


        found = sum(
            1
            for item in results
            if item["status"] == "FOUND"
        )


        blocked = sum(
            1
            for item in results
            if item["status"] == "BLOCKED"
        )


        not_found = sum(
            1
            for item in results
            if item["status"] == "NOT FOUND"
        )


        unable = sum(
            1
            for item in results
            if item["status"] == "UNABLE"
        )


        # -----------------------------
        # EXPOSURE SCORE
        # -----------------------------

        score = min(
            100,
            found * 12
        )


        if score >= 70:

            risk = "HIGH"


        elif score >= 40:

            risk = "MEDIUM"


        elif score > 0:

            risk = "LOW"


        else:

            risk = "MINIMAL"


        # -----------------------------
        # DATE / TIME
        # -----------------------------

        now = datetime.now()


        # -----------------------------
        # RESPONSE
        # -----------------------------

        return jsonify({

            "success": True,

            "username": username,

            "total": total,

            "found": found,

            "blocked": blocked,

            "not_found": not_found,

            "unable": unable,

            "score": score,

            "risk": risk,

            "date": now.strftime(
                "%d %b %Y"
            ),

            "time": now.strftime(
                "%H:%M:%S"
            ),

            "results": results

        })


    except Exception as error:

        print(
            "SCAN ERROR:",
            error
        )


        return jsonify({

            "success": False,

            "message":
                "Internal server error."

        }), 500


# =========================================================
# IP ANALYZER
# =========================================================

@app.route("/api/ip", methods=["POST"])
def ip_lookup():

    try:

        data = request.get_json(
            silent=True
        ) or {}


        ip = str(
            data.get("ip", "")
        ).strip()


        if not ip:

            return jsonify({

                "success": False,

                "message":
                    "IP address is required."

            }), 400


        # -----------------------------
        # IP API REQUEST
        # -----------------------------

        response = requests.get(

            f"https://ipapi.co/{ip}/json/",

            timeout=10,

            headers={
                "User-Agent":
                    "DigitalFootprintAnalyzer/1.0"
            }

        )


        if response.status_code != 200:

            return jsonify({

                "success": False,

                "message":
                    "Unable to lookup this IP."

            }), 400


        info = response.json()


        return jsonify({

            "success": True,

            "ip":
                info.get(
                    "ip",
                    ip
                ),

            "isp":
                info.get(
                    "org",
                    "Unknown"
                ),

            "region":
                info.get(
                    "region",
                    "Unknown"
                ),

            "city":
                info.get(
                    "city",
                    "Unknown"
                ),

            "country":
                info.get(
                    "country_name",
                    "Unknown"
                ),

            "asn":
                info.get(
                    "asn",
                    "Unknown"
                ),

            "timezone":
                info.get(
                    "timezone",
                    "Unknown"
                )

        })


    except requests.RequestException as error:

        print(
            "IP REQUEST ERROR:",
            error
        )


        return jsonify({

            "success": False,

            "message":
                "IP lookup service is unavailable."

        }), 500


    except Exception as error:

        print(
            "IP LOOKUP ERROR:",
            error
        )


        return jsonify({

            "success": False,

            "message":
                "IP lookup failed."

        }), 500


# =========================================================
# SERVER
# =========================================================

if __name__ == "__main__":

    print("")
    print(
        "=============================================="
    )

    print(
        " DIGITAL FOOTPRINT ANALYZER"
    )

    print(
        " Flask server starting..."
    )

    print(
        "=============================================="
    )

    print("")


    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True

    )
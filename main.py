import requests
import socket
import re
from pathlib import Path
from urllib.parse import quote_plus
from datetime import datetime


# ============================================================
# DIGITAL FOOTPRINT ANALYZER
# Created by ARNAB
# ============================================================


# ============================================================
# PLATFORM DATABASE
# ============================================================

PLATFORMS = {
    "Instagram": "https://www.instagram.com/{username}/",
    "Facebook": "https://www.facebook.com/{username}",
    "TikTok": "https://www.tiktok.com/@{username}",
    "X": "https://x.com/{username}",
    "GitHub": "https://github.com/{username}",
    "GitLab": "https://gitlab.com/{username}",
    "Reddit": "https://www.reddit.com/user/{username}/",
    "YouTube": "https://www.youtube.com/@{username}",
    "Pinterest": "https://www.pinterest.com/{username}/",
    "Twitch": "https://www.twitch.tv/{username}",
}

GAMING_PLATFORMS = {
    "Steam": "https://steamcommunity.com/id/{username}",
    "Chess.com": "https://www.chess.com/member/{username}",
    "Roblox": "https://www.roblox.com/user.aspx?username={username}",
}

COMMUNITY_PLATFORMS = {
    "Quora": "https://www.quora.com/profile/{username}",
    "Medium": "https://medium.com/@{username}",
    "Tumblr": "https://{username}.tumblr.com",
    "Stack Overflow": "https://stackoverflow.com/users/{username}",
}

PROFESSIONAL_PLATFORMS = {
    "LinkedIn": "https://www.linkedin.com/in/{username}",
    "Kaggle": "https://www.kaggle.com/{username}",
    "Dev.to": "https://dev.to/{username}",
    "Behance": "https://www.behance.net/{username}",
}


# ============================================================
# COMMON PLATFORM CHECKER
# ============================================================

def check_profile(platform, url):

    try:
        response = requests.get(
            url,
            timeout=7,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            allow_redirects=True
        )

        if response.status_code == 200:
            status = "MEDIUM CONFIDENCE"

        elif response.status_code == 404:
            status = "NOT FOUND"

        elif response.status_code in (401, 403):
            status = "PROTECTED/BLOCKED"

        else:
            status = "UNABLE TO VERIFY"

        print(f"[{status}] {platform}")
        print("URL:", url)
        print()

        return {
            "platform": platform,
            "status": status,
            "url": url
        }

    except requests.RequestException:

        print(f"[ERROR] {platform}")
        print()

        return {
            "platform": platform,
            "status": "ERROR",
            "url": url
        }


# ============================================================
# PLATFORM SCANNER
# ============================================================

def scan_platform_group(username, platform_group, title):

    results = []

    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)

    for platform, template in platform_group.items():

        url = template.format(username=username)

        print("Checking", platform + "...")

        result = check_profile(platform, url)

        results.append(result)

    return results


def scan_platforms(username):

    return scan_platform_group(
        username,
        PLATFORMS,
        "PUBLIC PLATFORM SCAN"
    )


def scan_gaming_platforms(username):

    results = scan_platform_group(
        username,
        GAMING_PLATFORMS,
        "GAMING PLATFORM SCAN"
    )

    print("Gaming platforms checked:", len(results))

    return results


def scan_community_platforms(username):

    results = scan_platform_group(
        username,
        COMMUNITY_PLATFORMS,
        "COMMUNITY PLATFORM SCAN"
    )

    print("Community platforms checked:", len(results))

    return results


def scan_professional_platforms(username):

    results = scan_platform_group(
        username,
        PROFESSIONAL_PLATFORMS,
        "PROFESSIONAL PLATFORM SCAN"
    )

    print("Professional platforms checked:", len(results))

    return results


# ============================================================
# RESULT MANAGEMENT
# ============================================================

def add_results(results, new_results):

    existing = set()

    for item in results:

        if isinstance(item, dict):
            existing.add(item.get("platform"))

    for item in new_results:

        if isinstance(item, dict):

            platform = item.get("platform")

            if platform not in existing:

                results.append(item)
                existing.add(platform)


# ============================================================
# RISK SCORE
# ============================================================

def calculate_risk_score(results):

    if not results:
        return 0, "LOW"

    total = len(results)

    medium = 0
    high = 0

    for item in results:

        if not isinstance(item, dict):
            continue

        status = item.get("status", "")

        if "MEDIUM" in status:
            medium += 1

        elif "HIGH" in status:
            high += 1

    score = 0

    score += medium * 4
    score += high * 8

    if total >= 15:
        score += 10

    elif total >= 10:
        score += 5

    if score > 100:
        score = 100

    if score >= 70:
        risk_level = "HIGH"

    elif score >= 40:
        risk_level = "MEDIUM"

    else:
        risk_level = "LOW"

    return score, risk_level


# ============================================================
# RISK ANALYSIS
# ============================================================

def show_risk_analysis(results):

    print("\n" + "=" * 60)
    print("DIGITAL RISK ANALYSIS")
    print("=" * 60)

    if not results:

        print("\nNo scan data available.")
        return

    score, risk_level = calculate_risk_score(results)

    total = len(results)

    possible = 0
    blocked = 0

    for item in results:

        if not isinstance(item, dict):
            continue

        status = item.get("status", "")

        if "MEDIUM" in status or "HIGH" in status:
            possible += 1

        if "PROTECTED" in status or "BLOCKED" in status:
            blocked += 1

    print("\nPlatforms checked:", total)
    print("Possible public profiles:", possible)
    print("Protected/Blocked:", blocked)

    print("\nRisk Score:", score, "/ 100")
    print("Risk Level:", risk_level)

    print("\nRisk Explanation:")

    if risk_level == "HIGH":

        print("- High username exposure detected.")
        print("- The identifier appears across many platforms.")
        print("- Review public information and account privacy.")

    elif risk_level == "MEDIUM":

        print("- Moderate username exposure detected.")
        print("- Several public profiles may use this identifier.")
        print("- Review privacy settings and username reuse.")

    else:

        print("- Limited username exposure detected.")
        print("- Continue following good privacy practices.")

    print("\n[GENERAL SECURITY RECOMMENDATIONS]")

    print("1. Use unique passwords.")
    print("2. Enable two-factor authentication.")
    print("3. Avoid username reuse.")
    print("4. Review privacy settings.")
    print("5. Remove unnecessary public information.")


# ============================================================
# GENERAL WEB SEARCH
# ============================================================

def general_web_search(username):

    print("\n" + "=" * 60)
    print("GENERAL WEB SEARCH")
    print("=" * 60)

    query = quote_plus(username)

    search_url = "https://www.google.com/search?q=" + query

    print("\nSearch query:", username)
    print("Search URL:", search_url)

    print("\nReview the public search results in your browser.")


# ============================================================
# TOOL 1 — PORT SCANNER
# ============================================================

def is_private_or_local_host(target):

    try:

        ip = socket.gethostbyname(target)

        private_ranges = [
            "10.",
            "192.168.",
            "127.",
            "172.16.",
            "172.17.",
            "172.18.",
            "172.19.",
            "172.20.",
            "172.21.",
            "172.22.",
            "172.23.",
            "172.24.",
            "172.25.",
            "172.26.",
            "172.27.",
            "172.28.",
            "172.29.",
            "172.30.",
            "172.31.",
        ]

        if ip.startswith(tuple(private_ranges)):
            return True

        return ip == "localhost"

    except socket.gaierror:

        return False


def port_scanner():

    print("\n" + "=" * 60)
    print("PORT SCANNER")
    print("=" * 60)

    target = input("\nEnter local/private target: ").strip()

    if not target:
        print("Target cannot be empty.")
        return

    if not is_private_or_local_host(target):

        print("\n[!] For safety, this scanner only accepts")
        print("[!] localhost or private network targets.")
        return

    try:

        start_port = int(
            input("Start port (1-1000): ").strip()
        )

        end_port = int(
            input("End port (1-1000): ").strip()
        )

    except ValueError:

        print("Invalid port number.")
        return

    if start_port < 1 or end_port > 1000:
        print("Port range must be between 1 and 1000.")
        return

    if start_port > end_port:
        print("Start port cannot be greater than end port.")
        return

    print("\nScanning:", target)
    print("Ports:", start_port, "-", end_port)
    print()

    open_ports = []

    try:

        ip = socket.gethostbyname(target)

        for port in range(start_port, end_port + 1):

            sock = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM
            )

            sock.settimeout(0.3)

            result = sock.connect_ex(
                (ip, port)
            )

            if result == 0:

                try:
                    service = socket.getservbyport(
                        port,
                        "tcp"
                    )
                except OSError:
                    service = "unknown"

                print(
                    f"[OPEN] Port {port} | Service: {service}"
                )

                open_ports.append(
                    {
                        "port": port,
                        "service": service
                    }
                )

            sock.close()

    except socket.gaierror:

        print("[ERROR] Unable to resolve target.")
        return

    print("\nOpen ports found:", len(open_ports))


# ============================================================
# TOOL 2 — IP INFORMATION
# ============================================================

def ip_information():

    print("\n" + "=" * 60)
    print("IP INFORMATION")
    print("=" * 60)

    ip = input("\nEnter IP address: ").strip()

    if not ip:
        print("IP address cannot be empty.")
        return

    try:

        response = requests.get(
            f"https://ipapi.co/{ip}/json/",
            timeout=10
        )

        if response.status_code != 200:

            print("[ERROR] Unable to retrieve IP information.")
            return

        data = response.json()

        if data.get("error"):

            print("[ERROR]", data.get("reason", "Invalid IP"))
            return

        print("\nIP Address :", data.get("ip", "N/A"))
        print("Country    :", data.get("country_name", "N/A"))
        print("Region     :", data.get("region", "N/A"))
        print("City       :", data.get("city", "N/A"))
        print("Postal     :", data.get("postal", "N/A"))
        print("Timezone   :", data.get("timezone", "N/A"))
        print("ISP        :", data.get("org", "N/A"))
        print("ASN        :", data.get("asn", "N/A"))

        print(
            "\nNote: IP geolocation gives approximate "
            "network location, not a person's exact location."
        )

    except requests.RequestException:

        print("[ERROR] Network request failed.")


# ============================================================
# TOOL 3 — LOG FILE ANALYZER
# ============================================================

def log_file_analyzer():

    print("\n" + "=" * 60)
    print("LOG FILE ANALYZER")
    print("=" * 60)

    file_path = input(
        "\nEnter path to log file: "
    ).strip()

    if not file_path:

        print("File path cannot be empty.")
        return

    path = Path(file_path)

    if not path.exists():

        print("[ERROR] File not found.")
        return

    if not path.is_file():

        print("[ERROR] Path is not a file.")
        return

    try:

        content = path.read_text(
            encoding="utf-8",
            errors="ignore"
        )

    except OSError:

        print("[ERROR] Unable to read file.")
        return

    lines = content.splitlines()

    total = len(lines)

    errors = 0
    warnings = 0
    failed_logins = 0
    successful_logins = 0

    ip_addresses = {}

    for line in lines:

        lower_line = line.lower()

        if "error" in lower_line:
            errors += 1

        if "warning" in lower_line or "warn" in lower_line:
            warnings += 1

        if (
            "failed login" in lower_line
            or "login failed" in lower_line
            or "authentication failure" in lower_line
        ):
            failed_logins += 1

        if (
            "successful login" in lower_line
            or "login successful" in lower_line
        ):
            successful_logins += 1

        found_ips = re.findall(
            r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
            line
        )

        for ip in found_ips:

            ip_addresses[ip] = (
                ip_addresses.get(ip, 0) + 1
            )

    print("\nLOG ANALYSIS RESULTS")
    print("-" * 40)

    print("Total Entries       :", total)
    print("Errors              :", errors)
    print("Warnings            :", warnings)
    print("Failed Logins       :", failed_logins)
    print("Successful Logins   :", successful_logins)

    print("\nIP ADDRESSES FOUND")

    if ip_addresses:

        sorted_ips = sorted(
            ip_addresses.items(),
            key=lambda item: item[1],
            reverse=True
        )

        for ip, count in sorted_ips[:10]:

            print(
                f"{ip:<18} {count} occurrence(s)"
            )

    else:

        print("No IP addresses found.")

    if failed_logins >= 5:

        print("\n[!] Multiple failed login attempts detected.")

    if errors >= 10:

        print("[!] High number of error entries detected.")


# ============================================================
# TEXT REPORT
# ============================================================

def generate_text_report(username, results):

    reports_folder = Path("reports")

    reports_folder.mkdir(
        exist_ok=True
    )

    report_file = (
        reports_folder /
        "digital_footprint_report.txt"
    )

    score, risk_level = calculate_risk_score(
        results
    )

    now = datetime.now()

    with open(
        report_file,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            "DIGITAL FOOTPRINT ANALYZER\n"
        )

        file.write(
            "=" * 60 + "\n\n"
        )

        file.write(
            "Created by: ARNAB\n"
        )

        file.write(
            "Username: " + username + "\n"
        )

        file.write(
            "Scan Date: "
            + now.strftime("%d-%m-%Y")
            + "\n"
        )

        file.write(
            "Scan Time: "
            + now.strftime("%H:%M:%S")
            + "\n"
        )

        file.write(
            "Platforms Checked: "
            + str(len(results))
            + "\n"
        )

        file.write(
            "Risk Score: "
            + str(score)
            + "/100\n"
        )

        file.write(
            "Risk Level: "
            + risk_level
            + "\n\n"
        )

        file.write(
            "PLATFORM RESULTS\n"
        )

        file.write(
            "-" * 60 + "\n"
        )

        for item in results:

            if not isinstance(item, dict):
                continue

            file.write(
                item.get("platform", "Unknown")
                + " | "
                + item.get("status", "Unknown")
                + " | "
                + item.get("url", "")
                + "\n"
            )

        file.write(
            "\nSECURITY RECOMMENDATIONS\n"
        )

        file.write(
            "-" * 60 + "\n"
        )

        file.write(
            "1. Use unique passwords.\n"
        )

        file.write(
            "2. Enable two-factor authentication.\n"
        )

        file.write(
            "3. Avoid username reuse.\n"
        )

        file.write(
            "4. Review privacy settings.\n"
        )

        file.write(
            "5. Remove unnecessary public information.\n"
        )

    print(
        "\n[+] Text report generated:"
    )

    print(report_file)


# ============================================================
# MAIN MENU
# ============================================================

def main():

    print("=" * 60)
    print("       DIGITAL FOOTPRINT ANALYZER")
    print("              Created by ARNAB")
    print("=" * 60)

    username = input(
        "\nEnter username: "
    ).strip()

    if not username:

        print("Username cannot be empty.")
        return

    now = datetime.now()

    print(
        "\nScan Date:",
        now.strftime("%d-%m-%Y")
    )

    print(
        "Scan Time:",
        now.strftime("%H:%M:%S")
    )

    results = scan_platforms(
        username
    )

    while True:

        print("\n" + "=" * 60)
        print("MAIN MENU")
        print("=" * 60)

        print("1. Scan Public Platforms")
        print("2. Scan Gaming Platforms")
        print("3. Scan Community Platforms")
        print("4. Scan Professional Platforms")
        print("5. General Web Search")
        print("6. Digital Risk Analysis")
        print("7. Generate Report")

        print("\n--- CYBERSECURITY TOOLKIT ---")

        print("8. Port Scanner")
        print("9. IP Information")
        print("10. Log File Analyzer")

        print("\n11. Exit")

        choice = input(
            "\nEnter your choice: "
        ).strip()

        if choice == "1":

            print(
                "\nPublic platform scan already completed."
            )

        elif choice == "2":

            add_results(
                results,
                scan_gaming_platforms(username)
            )

        elif choice == "3":

            add_results(
                results,
                scan_community_platforms(username)
            )

        elif choice == "4":

            add_results(
                results,
                scan_professional_platforms(username)
            )

        elif choice == "5":

            general_web_search(username)

        elif choice == "6":

            show_risk_analysis(results)

        elif choice == "7":

            generate_text_report(
                username,
                results
            )

        elif choice == "8":

            port_scanner()

        elif choice == "9":

            ip_information()

        elif choice == "10":

            log_file_analyzer()

        elif choice == "11":

            print(
                "\nExiting Digital Footprint Analyzer."
            )

            break

        else:

            print(
                "\nInvalid choice."
            )


# ============================================================
# PROGRAM START
# ============================================================

if __name__ == "__main__":
    main()
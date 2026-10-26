import requests

SITES = [
    # Pagini obișnuite (Părțile 2, 3 și 4)
    "https://example.com",
    "https://httpbin.org/html",
    "https://httpbin.org/json",
    "https://httpbin.org/status/200",
    "https://httpbin.org/redirect/1",
    "https://httpbin.org/delay/2",
    # Pagini care eșuează
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
    "https://httpbin.org/delay/10",
    "http://this-site-does-not-exist.invalid",
    # Anteturi de securitate (Partea 5)
    "https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff",
    "https://httpbin.org/response-headers?x-frame-options=DENY",
    # Răspunde aleatoriu cu 200 sau 500 (Partea 6)
    "https://httpbin.org/status/200,500",
]

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
]


def build_url(host, path):
    host = host.rstrip("/")
    if not path.startswith("/"):
        path = "/" + path
    return f"https://{host}{path}"


def is_https(url):
    return url.lower().startswith("https://")


def show_response(url):
    timeout(5)
    try:
        response = requests.get(SITES, timeout=timeout)
        print(f"Status: {response.status_code}")
        print(f"Content-Type: {response.headers.get('Content-Type', 'Unknown')}")
    except requests.RequestException as e:
        print(f"Eroare: {e}")


def check_site(url):
    timeout = 5
    try:
        r = requests.get(url, timeout=timeout)
        content_type = r.headers.get("Content-Type", "").strip()
        server = r.headers.get("Server", "unknown")

        return {
            "status": r.status_code,
            "content_type": content_type if content_type else "unknown",
            "length": len(r.content),
            "server": server
        }
    except requests.RequestException:
        return {"status": None, "error": "unknown"}


def scan_sites():
    rezultate = []
    numarat = 0
    fail = 0

    for site in SITES:
        res = check_site(site)
        if res.get("status") == 200:
            numarat += 1
            results.append((site, res.get("length", 0)))
        else:
            fail += 1

    results.sort(key=lambda x: x[1], reverse=True)

    for site, length in rezultate:
        print(f"{site} -> 200, {length} octeți")

    print(f"Reușite: {success_count} | Eșuate: {fail_count}")


def check_headers(url):
    try:
        response = requests.get(url, timeout=5)
        resp_headers = {k.lower(): v for k, v in response.headers.items()}

        present = []
        missing = []

        for header in SECURITY_HEADERS:
            if header.lower() in resp_headers:
                present.append(header)
            else:
                missing.append(header)

        score = int((len(present) / len(SECURITY_HEADERS)) * 100)

        return {
            "present": present,
            "missing": missing,
            "score": score
        }
    except requests.RequestException:
        return {"status": None, "error": "unknown"}


def retry_check(url, attempts=3):
    last_status = None
    last_error = None
    made_attempts = 0

    for i in range(1, attempts + 1):
        made_attempts = i
        try:
            response = requests.get(url, timeout=5)
            last_status = response.status_code

            if last_status < 500:
                return {"status": last_status, "attempts": made_attempts}

        except requests.RequestException as e:
            last_error = str(e)
            last_status = None

    result = {"status": last_status, "attempts": made_attempts}
    if last_error and last_status is None:
        result["error"] = "unknown"
    return result

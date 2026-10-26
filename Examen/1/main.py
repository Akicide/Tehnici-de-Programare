from checker import (
    build_url, is_https, show_response, 
    check_site, scan_sites, check_headers, retry_check
)

print("--- PARTEA 1: Funcții ajutătoare ---")
print("1. build_url (fără bară):", build_url("example.com", "login"))
print("2. build_url (cu bară):", build_url("example.com", "/login"))
print("3. is_https (caz valid):", is_https("https://example.com"))
print("4. is_https (caz invalid):", is_https("http://example.com"))

print("\n--- PARTEA 2: Trimiterea unei cereri ---")
show_response("https://example.com")

print("\n--- PARTEA 3: Verificatorul reutilizabil ---")
print("Caz de succes (example.com):", check_site("https://example.com"))
print("Caz de eroare (site inexistent):", check_site("http://this-site-does-not-exist.invalid"))

print("\n--- PARTEA 4: Verificarea mai multor site-uri (scan_sites) ---")
scan_sites()

print("\n--- PARTEA 5: Audit de securitate ---")
print("Audit httpbin:", check_headers("https://httpbin.org/html"))

print("\n--- PARTEA 6: Încercări repetate (retry_check) ---")
print("Retry status 200:", retry_check("https://httpbin.org/status/200"))
print("Retry status 404:", retry_check("https://httpbin.org/status/404"))
print("Retry status 500 (2 încercări):", retry_check("https://httpbin.org/status/500", attempts=2))
print("Retry site invalid:", retry_check("http://this-site-does-not-exist.invalid"))

print("\nToate testele din main.py s-au finalizat cu succes!")
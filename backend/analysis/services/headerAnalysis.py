from httpx import AsyncClient, RequestError
import re


IDEAL_HEADERS = {
    "x-frame-options": {
        "ideal" : "deny",
        "explanation" : "Use Content Security Policy (CSP) frame-ancestors directive if possible.\n Do not allow displaying of the page in a frame.",
        "mandatory" : True
    },
    "x-xss-protection" : {
        "ideal" : "0",
        "explanation" : "Use a Content Security Policy (CSP) that disables the use of inline JavaScript.\n Do not set this header or explicitly turn it off.",
        "mandatory" : False
    },
    "x-content-type-options" : {
        "ideal" : "nosniff",
        "explanation" : "Set the Content-Type header correctly throughout the site.",
        "mandatory" : True
    },
    "referrer-policy" : {
        "ideal" : "strict-origin-when-cross-origin",
        "explanation" : "For most websites, you would want 'strict-origin-when-cross-origin', but depending on your needs 'no-referrer' or 'origin-when-cross-origin' could also be accepted.",
        "mandatory" : True
    },
    "content-type" : {
        "ideal" : "text/html; charset=utf-8",
        "explanation" : "Always include charset in text/html content types.",
        "mandatory" : False
    },
    "strict-transport-security" : {
        "ideal" : re.compile(r"max-age=\d+;\s*includeSubDomains;\s*preload"),
        "explanation" : "Watch out for max-age values and SSL/TLS expirations, also includeSubDomains is recommended unless you have legacy subdomains that still use htps, and preload is recommended only if your site is verified",
        "mandatory" : True
    },
    "except-ct" : {
        "ideal" : "",
        "explanation" : "Outdated, Mozilla recommends avoiding it, and removing it from existing code if possible.",
        "mandatory" : False
    }
    ,
    "content-security-policy": {
        "ideal": ["default-src 'self'", "script-src 'self'", "style-src 'self' 'unsafe-inline'", "object-src 'none'", "base-uri 'self'", "frame-ancestors 'none'"],
        "explanation": "CSP helps prevent XSS and data injection attacks. Check https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html",
        "mandatory": True
    },
    "server" : {
        "ideal" : "webserver",
        "explanation" : "Remove this header or set non-informative values.",
        "mandatory" : False
    }
    ,
    "x-powered-by" : {
        "ideal" : "",
        "explanation" : "Remove all X-Powered-By headers",
        "mandatory" : False
    }
}


def build_error_report(header, value):
    return {
        "value": value,
        "ideal": IDEAL_HEADERS[header]['ideal'],
        "error": True,
        "explanation": IDEAL_HEADERS[header]['explanation']
    }

async def try_request(url_base: str):
    for scheme in ["","https://", "http://"]:
        try:
            async with AsyncClient() as client:
                response = await client.get(scheme + url_base, timeout=5)

            return response
        except RequestError:
            continue
    raise Exception(f"Could not connect to {url_base} via HTTP or HTTPS")


async def checkHeaders(url: str):
    try:
        response = await try_request(url)
        report = []
        seen_headers = set()

        for header, value in response.headers.items():
            if header in IDEAL_HEADERS:
                ideal = IDEAL_HEADERS[header]['ideal']
                seen_headers.add(header)

                if isinstance(ideal, re.Pattern):
                    if not ideal.match(value.lower()):
                        report.insert(0, {header: build_error_report(header, value)})
                        continue

                elif isinstance(ideal, list) and header == 'content-security-policy':
                    directives = [d.strip() for d in value.split(';')]
                    missing = [ property for property in ideal if property not in directives ]
                    if missing:
                        report.insert(0, {
                            header: {
                                "value": value,
                                "ideal": ideal,
                                "error": True,
                                "explanation": IDEAL_HEADERS[header]['explanation'],
                                "missing": missing
                            }
                        })
                        continue

                elif value.lower() != ideal:
                    report.insert(0, {header: build_error_report(header, value)})
                    continue

            report.append({
                header: {
                    "value": value,
                    "ideal": "",
                    "error": False,
                    "explanation": ""
                }
            })

        for header, config in IDEAL_HEADERS.items():
            if config['mandatory'] and header not in seen_headers:
                report.insert(0, {
                    header: {
                        "value": "",
                        "ideal": config['ideal'],
                        "error": True,
                        "explanation": config['explanation']
                    }
                })

        return report

    except Exception as e:
        raise e


        
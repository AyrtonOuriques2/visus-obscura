import re
from bs4 import BeautifulSoup
from httpx import AsyncClient
import hashlib


#todo finish this
async def get_favicon_hash(url):
    try:
        async with AsyncClient() as client:
            resp = await client.get(url+ '/favicon.ico', timeout=5)
            if resp.status_code == 200:
                return hashlib.md5(resp.content).hexdigest()
    except Exception as e:
        raise e



def detectStack(html):
    frameworks = []
    seen_frameworks = set()

    def add_framework(name, version):
        if name not in seen_frameworks:
            seen_frameworks.add(name)
            frameworks.append({
                "name": name,
                "version": version
            })

    name_map = {
        "jquery": "jQuery",
        "angular": "AngularJs",
        "react": "React",
        "vue": "Vuejs",
        "webcomponents": "Web Components",
        "svelte": "Svelte",
        "ember": "Ember",
        "backbone": "Backbone",
        "alpine": "Alpine.js",
        "polymer": "Polymer",
        "next": "Next.js"
    }

    try:
        soup = BeautifulSoup(html, 'html.parser')
        html_str = str(soup).lower()

        for script in soup.find_all("script", src=True):
            src = script['src'].lower()
            for framework in name_map:
                if re.search(rf"(?<=[\/\-_\.@=]){framework}", src):
                    match = re.search(r"\d+\.\d+\.\d+", src)
                    version = match.group(0) if match else "unknown"
                    add_framework(name_map[framework], version)

        ng_version_tag = soup.find(attrs={"ng-version": True})
        if ng_version_tag:
            add_framework("Angular", ng_version_tag["ng-version"])
        if re.search(r'\bng-[a-z]+=', html_str):
            add_framework("Angular", "unknown")

        if re.search(r'\bv-[a-z]+=', html_str):
            add_framework("Vuejs", "unknown")

        if re.search(r'data-reactroot', html_str):
            add_framework("React", "unknown")

        if re.search(r'data-svelte', html_str) or re.search(r'svelte-[a-z0-9]+', html_str):
            add_framework("Svelte", "unknown")

        if re.search(r'data-ember-extension', html_str):
            add_framework("Ember", "unknown")

        if re.search(r'\bx-data=', html_str):
            add_framework("Alpine.js", "unknown")

        if re.search(r'polymer-element', html_str) or re.search(r'polymer-', html_str):
            add_framework("Polymer", "unknown")

        if re.search(r'__next', html_str) or re.search(r'_next\/static', html_str):
            add_framework("Next.js", "unknown")

        generator = soup.find("meta", attrs={"name": "generator"})
        if generator and "wordpress" in generator.get("content", "").lower():
            wp_version = re.search(r"wordpress\s*([\d.]+)", generator['content'].lower())
            if wp_version:
                add_framework("WordPress", wp_version.group(1))
            else:
                add_framework("WordPress", "unknown")
        elif re.search(r'/wp-(content|includes|json)/', html_str) or \
             re.search(r'<!--.*yoast seo plugin.*-->', html_str, re.IGNORECASE):
            add_framework("WordPress", "unknown")

    except Exception as e:
        raise e

    return frameworks if frameworks else ""

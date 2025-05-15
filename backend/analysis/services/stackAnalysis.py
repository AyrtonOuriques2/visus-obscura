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
    #todo Svelte, Ember, Backbone, Alpine.js, Polymer, Next.js
    #backend frameworks
    #redo version check to find word + any set os number.number

    frameworks = {}

    try:
        soup = BeautifulSoup(html, 'html.parser')
        for script in soup.find_all("script", src=True):
            src = script['src'].lower()

            if "jquery" in src and "jQuery" not in frameworks:
                match = re.search(r"jquery(?:\.min)?[-.]?([\d.]+)\.js", src)
                if not match:
                    match = re.search(r"[?&]ver=([\d.]+)", src)
                if not match:
                    match = re.search(r"jquery@([\d.]+)", src)
                if match:
                    frameworks["jQuery"] = match.group(1)

            elif "angular" in src:
                match = re.search(r"angular(?:\.min)?[-.]?([\d.]+)\.js", src)
                if not match:
                    match = re.search(r"[?&]ver=([\d.]+)", src)
                if not match:
                    match = re.search(r"angular@([\d.]+)", src)
                if match:
                    frameworks["AngularJS"] = match.group(1)

            elif "react" in src:
                match = re.search(r"react(?:\.min)?[-.]?([\d.]+)\.js", src)
                if not match:
                    match = re.search(r"[?&]ver=([\d.]+)", src)
                if not match:
                    match = re.search(r"react@([\d.]+)", src)
                if match:
                    frameworks["React"] = match.group(1)

            elif "vue" in src:
                match = re.search(r"vue(?:\.runtime)?(?:\.min)?[-.]?([\d.]+)\.js", src)
                if not match:
                    match = re.search(r"[?&]ver=([\d.]+)", src)
                if not match:
                    match = re.search(r"vue@([\d.]+)", src)
                if match:
                    frameworks["Vue.js"] = match.group(1)

            elif "webcomponents" in src:
                match = re.search(r"webcomponents(?:\.min)?[-.]?([\d.]+)\.js", src)               
                if not match:
                    match = re.search(r"[?&]ver=([\d.]+)", src)        
                if not match:
                    match = re.search(r"webcomponentsjs@([\d.]+)", src)
                if match:
                    frameworks["Web Components"] = match.group(1)


        html_str = str(soup)

        if re.search(r'\bng-[a-z]+=', html_str):
            frameworks.setdefault("AngularJS", "unknown")
        if re.search(r'\bv-[a-z]+=', html_str):
            frameworks.setdefault("Vue.js", "unknown")
        if re.search(r'data-reactroot', html_str):
            frameworks.setdefault("React", "unknown")

        ng_version_tag = soup.find(attrs={"ng-version": True})
        if ng_version_tag:
            frameworks["Angular"] = ng_version_tag["ng-version"]

        generator = soup.find("meta", attrs={"name": "generator"})
        if generator and "wordpress" in generator.get("content", "").lower():
            wp_version = re.search(r"wordpress\s*([\d.]+)", generator['content'].lower())
            if wp_version:
                frameworks["WordPress"] = wp_version.group(1)
            else:
                frameworks["WordPress"] = "unknown"
        elif re.search(r'/wp-(content|includes|json)/', html_str):
            frameworks["WordPress"] = "detected via file path"
        elif re.search(r'<!--.*yoast seo plugin.*-->', html_str, re.IGNORECASE):
            frameworks["WordPress"] = "detected via SEO comment"
    
    except Exception as e:
        print(e)
        pass

    return frameworks
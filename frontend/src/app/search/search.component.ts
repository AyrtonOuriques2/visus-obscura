import { Component, ElementRef, Renderer2, ViewChild } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../api.service';
import { MatIconModule } from '@angular/material/icon';
import { CommonModule } from '@angular/common';
import { catchError, of } from 'rxjs';
import { DisplayComponent } from '../display/display.component';

@Component({
  selector: 'app-search',
  standalone: true,
  imports: [
    FormsModule,
    MatIconModule,
    CommonModule,
    DisplayComponent
  ],
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.css'] 
})
export class SearchComponent {
  urlToSearch: string = '';
  loading: boolean = false;
  data : {} = '';

  @ViewChild('eye', { static: true }) eyeRef!: ElementRef;

  constructor(private apiService: ApiService, private renderer: Renderer2){}

  clear(){
    this.data = '';
    this.urlToSearch = '';
  }

  analyseUrl() {
    this.loading = true;
    // this.apiService.analyseUrl(this.urlToSearch).pipe(
    //   catchError((error) => {
    //     this.loading = false;
  
    //     if (error.status === 500 && error.error?.detail) {
    //       console.error('Backend Error:', error.error.detail);
    //     }
  
    //     return of(null); 
    //   })
    // ).subscribe((response) => {
    //   this.loading = false;
    //   if (response) {
    //     this.data = response;
    //   }
    // });
    setTimeout(() => {
      this.loading = false;
      this.data = {
        "status": "success",
        "report": {
          "stackReport": [
            {
              "name": "Next.js",
              "version": "unknown"
            },
            {
              "name": "Web Components",
              "version": "unknown"
            }
          ],
          "panelsReport": [
            "cpanel",
            "dashboard"
          ],
          "filesReport": "",
          "robotsReport": {
            "found": true,
            "status_code": 200,
            "user_agents": [
              "Mediapartners-Google*",
              "*"
            ],
            "disallowed_paths": [
              "",
              "/comment",
              "/feeds/videos.xml",
              "/get_video",
              "/get_video_info",
              "/get_midroll_info",
              "/live_chat",
              "/qr",
              "/results",
              "/signup",
              "/t/terms",
              "/timedtext_video",
              "/verify_age",
              "/watch_ajax",
              "/watch_fragments_ajax",
              "/watch_popup",
              "/watch_queue_ajax",
              "/youtubei/"
            ],
            "allowed_paths": "",
            "sitemaps": [
              "https://www.youtube.com/sitemaps/sitemap.xml",
              "https://www.youtube.com/product/sitemap.xml"
            ],
            "uses_wildcards": false,
            "uses_end_anchors": false,
            "suspicious_entries": [
              {
                "type": "Disallow",
                "path": "/api/"
              },
              {
                "type": "Disallow",
                "path": "/login"
              }
            ]
          },
          "redirectReport": "",
          "headerReport": [
            {
              "header": "referrer-policy",
              "value": "",
              "ideal": "strict-origin-when-cross-origin",
              "error": true,
              "explanation": "For most websites, you would want 'strict-origin-when-cross-origin', but depending on your needs 'no-referrer' or 'origin-when-cross-origin' could also be accepted."
            },
            {
              "header": "server",
              "value": "ESF",
              "ideal": "webserver",
              "error": true,
              "explanation": "Remove this header or set non-informative values."
            },
            {
              "header": "content-security-policy",
              "value": "require-trusted-types-for 'script'",
              "ideal": [
                "default-src 'self'",
                "script-src 'self'",
                "style-src 'self' 'unsafe-inline'",
                "object-src 'none'",
                "base-uri 'self'",
                "frame-ancestors 'none'"
              ],
              "error": true,
              "explanation": "CSP helps prevent XSS and data injection attacks. Check https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html",
              "missing": [
                "default-src 'self'",
                "script-src 'self'",
                "style-src 'self' 'unsafe-inline'",
                "object-src 'none'",
                "base-uri 'self'",
                "frame-ancestors 'none'"
              ]
            },
            {
              "header": "x-frame-options",
              "value": "SAMEORIGIN",
              "ideal": "deny",
              "error": true,
              "explanation": "Use Content Security Policy (CSP) frame-ancestors directive if possible.\n Do not allow displaying of the page in a frame."
            },
            {
              "header": "strict-transport-security",
              "value": "max-age=31536000",
              "ideal": "max-age=\\d+;\\s*includeSubDomains;\\s*preload",
              "error": true,
              "explanation": "Watch out for max-age values and SSL/TLS expirations, also includeSubDomains is recommended unless you have legacy subdomains that still use htps, and preload is recommended only if your site is verified"
            },
            {
              "header": "content-type",
              "value": "text/html; charset=utf-8",
              "ideal": "",
              "error": false,
              "explanation": ""
            },
            {
              "header": "x-content-type-options",
              "value": "nosniff",
              "ideal": "",
              "error": false,
              "explanation": ""
            },
            {
              "header": "cache-control",
              "value": "no-cache, no-store, max-age=0, must-revalidate",
              "ideal": "",
              "error": false,
              "explanation": ""
            },
            {
              "header": "pragma",
              "value": "no-cache",
              "ideal": "",
              "error": false,
              "explanation": ""
            },
            {
              "header": "expires",
              "value": "Mon, 01 Jan 1990 00:00:00 GMT",
              "ideal": "",
              "error": false,
              "explanation": ""
            },
            {
              "header": "date",
              "value": "Sun, 18 May 2025 02:11:02 GMT",
              "ideal": "",
              "error": false,
              "explanation": ""
            },
            {
              "header": "origin-trial",
              "value": "AmhMBR6zCLzDDxpW+HfpP67BqwIknWnyMOXOQGfzYswFmJe+fgaI6XZgAzcxOrzNtP7hEDsOo1jdjFnVr2IdxQ4AAAB4eyJvcmlnaW4iOiJodHRwczovL3lvdXR1YmUuY29tOjQ0MyIsImZlYXR1cmUiOiJXZWJWaWV3WFJlcXVlc3RlZFdpdGhEZXByZWNhdGlvbiIsImV4cGlyeSI6MTc1ODA2NzE5OSwiaXNTdWJkb21haW4iOnRydWV9",
              "ideal": "",
              "error": false,
              "explanation": ""
            },
            {
              "header": "permissions-policy",
              "value": "ch-ua-arch=*, ch-ua-bitness=*, ch-ua-full-version=*, ch-ua-full-version-list=*, ch-ua-model=*, ch-ua-wow64=*, ch-ua-form-factors=*, ch-ua-platform=*, ch-ua-platform-version=*",
              "ideal": "",
              "error": false,
              "explanation": ""
            },
            {
              "header": "report-to",
              "value": "{\"group\":\"youtube_main\",\"max_age\":2592000,\"endpoints\":[{\"url\":\"https://csp.withgoogle.com/csp/report-to/youtube_main\"}]}",
              "ideal": "",
              "error": false,
              "explanation": ""
            },
            {
              "header": "accept-ch",
              "value": "Sec-CH-UA-Arch, Sec-CH-UA-Bitness, Sec-CH-UA-Full-Version, Sec-CH-UA-Full-Version-List, Sec-CH-UA-Model, Sec-CH-UA-WoW64, Sec-CH-UA-Form-Factors, Sec-CH-UA-Platform, Sec-CH-UA-Platform-Version",
              "ideal": "",
              "error": false,
              "explanation": ""
            },
            {
              "header": "vary",
              "value": "Sec-CH-UA-Arch, Sec-CH-UA-Bitness, Sec-CH-UA-Full-Version, Sec-CH-UA-Full-Version-List, Sec-CH-UA-Model, Sec-CH-UA-WoW64, Sec-CH-UA-Form-Factors, Sec-CH-UA-Platform, Sec-CH-UA-Platform-Version",
              "ideal": "",
              "error": false,
              "explanation": ""
            },
            {
              "header": "cross-origin-opener-policy",
              "value": "same-origin-allow-popups; report-to=\"youtube_main\"",
              "ideal": "",
              "error": false,
              "explanation": ""
            },
            {
              "header": "p3p",
              "value": "CP=\"This is not a P3P policy! See http://support.google.com/accounts/answer/151657?hl=en for more info.\"",
              "ideal": "",
              "error": false,
              "explanation": ""
            },
            {
              "header": "content-encoding",
              "value": "gzip",
              "ideal": "",
              "error": false,
              "explanation": ""
            },
            {
              "header": "x-xss-protection",
              "value": "0",
              "ideal": "",
              "error": false,
              "explanation": ""
            },
            {
              "header": "set-cookie",
              "value": "GPS=1; Domain=.youtube.com; Expires=Sun, 18-May-2025 02:41:02 GMT; Path=/; Secure; HttpOnly, YSC=e3wiVRYBOpQ; Domain=.youtube.com; Path=/; Secure; HttpOnly; SameSite=none; Partitioned, __Secure-ROLLOUT_TOKEN=CLCkiajlsrrG4gEQ3InZt_irjQMY3InZt_irjQM%3D; Domain=youtube.com; Expires=Fri, 14-Nov-2025 02:11:02 GMT; Path=/; Secure; HttpOnly; SameSite=none; Partitioned, VISITOR_INFO1_LIVE=qVoM9vudPnY; Domain=.youtube.com; Expires=Fri, 14-Nov-2025 02:11:02 GMT; Path=/; Secure; HttpOnly; SameSite=none; Partitioned, VISITOR_PRIVACY_METADATA=CgJCUhIEGgAgbA%3D%3D; Domain=.youtube.com; Expires=Fri, 14-Nov-2025 02:11:02 GMT; Path=/; Secure; HttpOnly; SameSite=none; Partitioned",
              "ideal": "",
              "error": false,
              "explanation": ""
            },
            {
              "header": "alt-svc",
              "value": "h3=\":443\"; ma=2592000,h3-29=\":443\"; ma=2592000",
              "ideal": "",
              "error": false,
              "explanation": ""
            },
            {
              "header": "transfer-encoding",
              "value": "chunked",
              "ideal": "",
              "error": false,
              "explanation": ""
            }
          ],
          "httpsReport": {
            "hostname": "www.youtube.com",
            "ip": "142.251.135.78",
            "https_supported": true,
            "cert_present": true,
            "valid_now": true,
            "expires_on": "2025-07-14T08:40:41",
            "expires_in_days": 57,
            "issued_to": "*.google.com",
            "issued_by": "WR2",
            "subject": {
              "commonName": "*.google.com"
            },
            "issuer": {
              "countryName": "US",
              "organizationName": "Google Trust Services",
              "commonName": "WR2"
            }
          },
          "ssl_tlsReport": {
            "targetHost": "www.youtube.com",
            "ip": "142.251.135.78",
            "port": "443",
            "rDNS": "rio09s07-in-f14.1e100.net.",
            "service": "HTTP",
            "pretest": [
              {
                "id": "pre_128cipher",
                "severity": "INFO",
                "finding": "No 128 cipher limit bug"
              }
            ],
            "protocols": [
              {
                "id": "SSLv2",
                "severity": "OK",
                "finding": "not offered"
              },
              {
                "id": "SSLv3",
                "severity": "OK",
                "finding": "not offered"
              },
              {
                "id": "TLS1",
                "severity": "LOW",
                "finding": "offered (deprecated)"
              },
              {
                "id": "TLS1_1",
                "severity": "LOW",
                "finding": "offered (deprecated)"
              },
              {
                "id": "TLS1_2",
                "severity": "OK",
                "finding": "offered"
              },
              {
                "id": "TLS1_3",
                "severity": "OK",
                "finding": "offered with final"
              },
              {
                "id": "NPN",
                "severity": "INFO",
                "finding": "offered with grpc-exp, h2, http/1.1 (advertised)"
              },
              {
                "id": "ALPN_HTTP2",
                "severity": "OK",
                "finding": "h2"
              },
              {
                "id": "ALPN",
                "severity": "INFO",
                "finding": "http/1.1grpc-exp"
              }
            ],
            "grease": [],
            "ciphers": [
              {
                "id": "cipherlist_NULL",
                "severity": "OK",
                "cwe": "CWE-327",
                "finding": "not offered"
              },
              {
                "id": "cipherlist_aNULL",
                "severity": "OK",
                "cwe": "CWE-327",
                "finding": "not offered"
              },
              {
                "id": "cipherlist_EXPORT",
                "severity": "OK",
                "cwe": "CWE-327",
                "finding": "not offered"
              },
              {
                "id": "cipherlist_LOW",
                "severity": "OK",
                "cwe": "CWE-327",
                "finding": "not offered"
              },
              {
                "id": "cipherlist_3DES_IDEA",
                "severity": "MEDIUM",
                "cwe": "CWE-310",
                "finding": "offered"
              },
              {
                "id": "cipherlist_OBSOLETED",
                "severity": "LOW",
                "cwe": "CWE-310",
                "finding": "offered"
              },
              {
                "id": "cipherlist_STRONG_NOFS",
                "severity": "OK",
                "finding": "offered"
              },
              {
                "id": "cipherlist_STRONG_FS",
                "severity": "OK",
                "finding": "offered"
              }
            ],
            "serverPreferences": [],
            "fs": [],
            "serverDefaults": [],
            "vulnerabilities": [],
            "cipherTests": [],
            "browserSimulations": [],
            "rating": []
          }
        }
      }
    }, 3000);
  }

  ngAfterViewInit(): void {

    this.renderer.listen('document', 'mousemove', (event: MouseEvent) => {
      if (this.loading) return;
      const eyeEl = this.eyeRef.nativeElement;
      const socketEl = eyeEl.parentElement!;
      const socketRect = socketEl.getBoundingClientRect();

      const centerX = socketRect.left + socketRect.width / 2;
      const centerY = socketRect.top + socketRect.height / 2;

      const deltaX = event.clientX - centerX;
      const deltaY = event.clientY - centerY;

      const distance = Math.sqrt(deltaX * deltaX + deltaY * deltaY);
      const hoverThreshold = 32;

      const isHoveringOnEye = distance < hoverThreshold;

      if (isHoveringOnEye) {
        const maxX = 36;
        const maxY = 18;

        const clampedX = Math.max(-maxX, Math.min(maxX, deltaX));
        const clampedY = Math.max(-maxY, Math.min(maxY, deltaY));

        this.renderer.setStyle(
          eyeEl,
          'transform',
          `translate(calc(-50% + ${clampedX}px), calc(-50% + ${clampedY}px))`
        );
      } else {
        const angle = Math.atan2(deltaY, deltaX);
        const radius = 18;

        const x = Math.cos(angle) * radius * 2;
        const y = Math.sin(angle) * radius;

        this.renderer.setStyle(
          eyeEl,
          'transform',
          `translate(calc(-50% + ${x}px), calc(-50% + ${y}px))`
        );
      }
    });
  }

}

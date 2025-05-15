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
          "stackReport": {
            "Web Components": "2.2.10"
          },
          "panelsReport": [
            "administrator",
            "cpanel",
            "dashboard",
            "login"
          ],
          "filesReport": [
            ".env",
            ".htaccess",
            ".DS_Store"
          ],
          "robotsReport": {
            "found": true,
            "status_code": 200,
            "user_agents": [
              "*"
            ],
            "disallowed_paths": [
              "/*/actions_panel*",
              "/users/auth/twitter*",
              "/users/auth/github*",
              "/report-abuse?url=*",
              "/connect/@*",
              "/search?q=*",
              "/search/?q=*",
              "/search/feed_content?*",
              "/listings*?q=*",
              "/mod/*",
              "/mod?*",
              "/admin/*",
              "/reactions?*",
              "/async_info/base_data",
              "/ahoy/*",
              "/auth_pass/*"
            ],
            "allowed_paths": [],
            "sitemaps": [
              "https://dev.to/sitemap-index.xml"
            ],
            "uses_wildcards": true,
            "uses_end_anchors": false,
            "suspicious_entries": [
              {
                "type": "Disallow",
                "path": "/admin/*"
              }
            ]
          },
          "redirectReport": [],
          "headerReport": [
            {
              "header": "x-frame-options",
              "value": "",
              "ideal": "deny",
              "error": true,
              "explanation": "Use Content Security Policy (CSP) frame-ancestors directive if possible.\n Do not allow displaying of the page in a frame."
            },
            {
              "header": "strict-transport-security",
              "value": "max-age=31557600",
              "ideal": "max-age=\\d+;\\s*includeSubDomains;\\s*preload",
              "error": true,
              "explanation": "Watch out for max-age values and SSL/TLS expirations, also includeSubDomains is recommended unless you have legacy subdomains that still use htps, and preload is recommended only if your site is verified"
            },
            {
              "header": "content-security-policy",
              "value": "frame-ancestors https://bizarro.dev.to https://forem.com https://future.forem.com https://dev.to https://version-feb-19-mjhc7.b-cdn.net https://codenewbie.forem.com https://coss.forem.com https://dumb.dev.to https://music.forem.com https://vibe.forem.com https://gg.forem.com https://core.forem.com https://dev.to",
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
              "header": "server",
              "value": "Cowboy",
              "ideal": "webserver",
              "error": true,
              "explanation": "Remove this header or set non-informative values."
            },
            {
              "header": "connection",
              "value": "keep-alive",
              "ideal": "",
              "error": false,
              "explanation": ""
            },
            {
              "header": "content-length",
              "value": "37874",
              "ideal": "",
              "error": false,
              "explanation": ""
            },
            {
              "header": "report-to",
              "value": "{\"group\":\"heroku-nel\",\"max_age\":3600,\"endpoints\":[{\"url\":\"https://nel.heroku.com/reports?ts=1747336124&sid=929419e7-33ea-4e2f-85f0-7d8b7cd5cbd6&s=wt328evuOR3f47Xeg5pjsJq0AUmBBmMXZgNasiopLfk%3D\"}]}",
              "ideal": "",
              "error": false,
              "explanation": ""
            },
            {
              "header": "reporting-endpoints",
              "value": "heroku-nel=https://nel.heroku.com/reports?ts=1747336124&sid=929419e7-33ea-4e2f-85f0-7d8b7cd5cbd6&s=wt328evuOR3f47Xeg5pjsJq0AUmBBmMXZgNasiopLfk%3D",
              "ideal": "",
              "error": false,
              "explanation": ""
            },
            {
              "header": "nel",
              "value": "{\"report_to\":\"heroku-nel\",\"max_age\":3600,\"success_fraction\":0.005,\"failure_fraction\":0.05,\"response_headers\":[\"Via\"]}",
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
              "header": "x-content-type-options",
              "value": "nosniff",
              "ideal": "",
              "error": false,
              "explanation": ""
            },
            {
              "header": "x-download-options",
              "value": "noopen",
              "ideal": "",
              "error": false,
              "explanation": ""
            },
            {
              "header": "x-permitted-cross-domain-policies",
              "value": "none",
              "ideal": "",
              "error": false,
              "explanation": ""
            },
            {
              "header": "referrer-policy",
              "value": "strict-origin-when-cross-origin",
              "ideal": "",
              "error": false,
              "explanation": ""
            },
            {
              "header": "cache-control",
              "value": "public, no-cache",
              "ideal": "",
              "error": false,
              "explanation": ""
            },
            {
              "header": "x-accel-expires",
              "value": "172800",
              "ideal": "",
              "error": false,
              "explanation": ""
            },
            {
              "header": "link",
              "value": "<https://assets.dev.to/assets/minimal-35f63f367d855f6b96ce34f5ee637209befbd1ccab982d77db7fa68aefc310b8.css>; rel=preload; as=style; nopush,<https://assets.dev.to/assets/views-1c703342dce6eac414f19ca7fd07bcf83cbe44088659758144e52e7fa1e92dd3.css>; rel=preload; as=style; nopush,<https://assets.dev.to/assets/crayons-0f2fc85bc159498f8ae6fba58c460e6deba863d02d59dfa994c1954976ddb6cc.css>; rel=preload; as=style; nopush",
              "ideal": "",
              "error": false,
              "explanation": ""
            },
            {
              "header": "content-type",
              "value": "text/html; charset=utf-8",
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
              "header": "etag",
              "value": "W/\"c2597153d71cdf6f6bcd2a1fcfe3d0a3\"",
              "ideal": "",
              "error": false,
              "explanation": ""
            },
            {
              "header": "x-request-id",
              "value": "5fb04d6f-073a-47f9-84b9-2d8db53ab300",
              "ideal": "",
              "error": false,
              "explanation": ""
            },
            {
              "header": "x-runtime",
              "value": "0.097178",
              "ideal": "",
              "error": false,
              "explanation": ""
            },
            {
              "header": "via",
              "value": "1.1 vegur, 1.1 varnish, 1.1 varnish",
              "ideal": "",
              "error": false,
              "explanation": ""
            },
            {
              "header": "access-control-allow-origin",
              "value": "*",
              "ideal": "",
              "error": false,
              "explanation": ""
            },
            {
              "header": "accept-ranges",
              "value": "bytes",
              "ideal": "",
              "error": false,
              "explanation": ""
            },
            {
              "header": "age",
              "value": "131",
              "ideal": "",
              "error": false,
              "explanation": ""
            },
            {
              "header": "date",
              "value": "Thu, 15 May 2025 19:10:55 GMT",
              "ideal": "",
              "error": false,
              "explanation": ""
            },
            {
              "header": "x-served-by",
              "value": "cache-den-kden1300067-DEN, cache-for8429-FOR",
              "ideal": "",
              "error": false,
              "explanation": ""
            },
            {
              "header": "x-cache",
              "value": "HIT, MISS",
              "ideal": "",
              "error": false,
              "explanation": ""
            },
            {
              "header": "x-cache-hits",
              "value": "4, 0",
              "ideal": "",
              "error": false,
              "explanation": ""
            },
            {
              "header": "x-timer",
              "value": "S1747336255.301994,VS0,VE132",
              "ideal": "",
              "error": false,
              "explanation": ""
            },
            {
              "header": "vary",
              "value": "Accept-Encoding, X-Loggedin",
              "ideal": "",
              "error": false,
              "explanation": ""
            }
          ],
          "httpsReport": {
            "hostname": "dev.to",
            "ip": "151.101.194.217",
            "https_supported": true,
            "cert_present": true,
            "valid_now": true,
            "expires_on": "2026-02-08T22:00:09",
            "expires_in_days": 269,
            "issued_to": "dev.to",
            "issued_by": "GlobalSign Atlas R3 DV TLS CA 2024 Q4",
            "subject": {
              "commonName": "dev.to"
            },
            "issuer": {
              "countryName": "BE",
              "organizationName": "GlobalSign nv-sa",
              "commonName": "GlobalSign Atlas R3 DV TLS CA 2024 Q4"
            }
          },
          "ssl_tlsReport": {
            "targetHost": "dev.to",
            "ip": "151.101.194.217",
            "port": "443",
            "rDNS": "--",
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
                "severity": "INFO",
                "finding": "not offered"
              },
              {
                "id": "TLS1_1",
                "severity": "INFO",
                "finding": "not offered"
              },
              {
                "id": "TLS1_2",
                "severity": "OK",
                "finding": "offered"
              },
              {
                "id": "TLS1_3",
                "severity": "INFO",
                "finding": "not offered + downgraded to weaker protocol"
              },
              {
                "id": "NPN",
                "severity": "INFO",
                "finding": "not offered"
              },
              {
                "id": "ALPN_HTTP2",
                "severity": "OK",
                "finding": "h2"
              },
              {
                "id": "ALPN",
                "severity": "INFO",
                "finding": "http/1.1"
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
                "severity": "INFO",
                "cwe": "CWE-310",
                "finding": "not offered"
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

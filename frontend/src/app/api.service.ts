import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private  apiUrl = 'https://visus-obscura-latest.onrender.com';

  constructor(private http: HttpClient) {}

  analyseUrl(query: string): Observable<any> {
    let payload = {
      url : query
    }
    return this.http.post(`${this.apiUrl}`, payload);
  }
}

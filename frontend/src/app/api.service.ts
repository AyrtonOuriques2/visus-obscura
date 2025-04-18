import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private  apiUrl = 'http://127.0.0.1:8000';

  constructor(private http: HttpClient) {}

  analyseUrl(query: string): Observable<any> {
    let payload = {
      url : query
    }
    return this.http.post(`${this.apiUrl}`, payload);
  }
}

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { BotResponse } from './models/botresponse.model';

const baseUrl = 'http://localhost:5000/bot';

@Injectable({
  providedIn: 'root'
})
export class ApiServiceService {
  constructor(private http: HttpClient) { }

  getResponse(message: string): Observable<BotResponse> {
    const body = {prompt: message}
    return this.http.post<BotResponse>(`${baseUrl}`, body);
  }
}

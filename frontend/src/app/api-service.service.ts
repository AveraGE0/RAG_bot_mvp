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

  askOllama(question: string): Observable<string> {
    return new Observable((observer) => {
      fetch(baseUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({prompt: question}),
      })
      .then((response) => {
        const reader = response.body?.getReader();
        const decoder = new TextDecoder();
        const read = () => {
          reader?.read().then(({ done, value }) => {
            if (done) {
              observer.complete();
              return;
            }
            const text = decoder.decode(value);
            try {
              const jsonObj = JSON.parse(text); // Parse the text as JSON
              const specificValue = jsonObj.response; // Replace 'yourKey' with the actual key you're interested in
              observer.next(specificValue); // Emit the specific value
            } catch (error) {
              observer.error(`Error parsing JSON: ${error}`);
              return;
            }
            read(); // Read the next chunk
          });
        };
        read();
      })
      .catch((error) => {
        observer.error(error);
      });
    });
  }
}

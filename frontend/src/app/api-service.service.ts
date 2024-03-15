import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { BotResponse } from './models/botresponse.model';

const baseUrl =  'http://192.168.178.14:5000/bot' // 'http://localhost:5000/bot';

@Injectable({
  providedIn: 'root'
})
export class ApiServiceService {
  constructor(private http: HttpClient) { }

  getResponse(message: string): Observable<BotResponse> {
    const body = {prompt: message}
    return this.http.post<BotResponse>(`${baseUrl}`, body);
  }

  cleanMessage(message: string) {
    // Example: simplistic approach to escaping quotes
    return message.replace(/[\n\r]+/g, '').trim(); // Adjust according to the specifics of your data
  }

  askOllama(question: string): Observable<string> {
    return new Observable((observer) => {
      fetch(baseUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({prompt: question}),
      })
      .then((response) => {
        if(response.status == 500){
            throw Error(response.statusText);
        }
        const reader = response.body?.getReader();
        const decoder = new TextDecoder("utf-8");
        const read = () => {
          reader?.read().then(({ done, value }) => {
            if (done) {
              observer.complete();
              return;
            }
            const text = decoder.decode(value);
            try {
              //console.log(text)
              const messages = text.trim().split('\n');
              for(let message of messages){
                const jsonObj = JSON.parse(message); // Parse the text as JSON
                observer.next(jsonObj.response); // Emit the specific value
              }
            } catch (error) {
              console.log("Skipping Erroneous text:")
              console.log(text)
              observer.complete()
              //observer.error(`Error parsing JSON: ${error}`);
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

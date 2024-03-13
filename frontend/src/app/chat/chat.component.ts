import { Component } from '@angular/core';
import {MatInputModule} from '@angular/material/input';
import {MatFormFieldModule} from '@angular/material/form-field'; 
import {MatButtonModule} from '@angular/material/button'; 
import {MatIconModule} from '@angular/material/icon'; 
import {MatDividerModule} from '@angular/material/divider'; 
import { FormControl, ReactiveFormsModule } from '@angular/forms';

import { ApiServiceService } from '../api-service.service';
import { HttpErrorResponse } from '@angular/common/http';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [
    MatInputModule,
    MatFormFieldModule,
    MatButtonModule,
    MatIconModule,
    MatDividerModule,
    ReactiveFormsModule,
    CommonModule,
  ],
  templateUrl: './chat.component.html',
  styleUrl: './chat.component.scss'
})
export class ChatComponent {

  constructor(private _apiService: ApiServiceService){};
  liveChat = ""
  botName = "Digital Student Advisor";
  idCount = 0;
  prompt = new FormControl('');
  waiting = false;

  addMessage(message: string, src: string){
    let mgs = {id: this.idCount, msg: message, src: src}

    this.idCount += 1
    this.messages.push(mgs)
  }

  send(event: MouseEvent): void {
    event.stopPropagation(); // Stops the click event from reaching the input field
    let message = this.prompt.value ? this.prompt.value: "";
    if(message === ""){
      return
    }
    console.log("sending message to bot: ", message)
    if( !this.prompt.value){
      this.prompt.setValue("")
    }
    this.addMessage(message, "You")
    this.prompt.setValue('');
    this.waiting = true
    // API CALL HERE
    this._apiService.askOllama(message).subscribe({
      next: (chunk) => {
        this.liveChat += chunk; // Append each received chunk to the chatContent variable
      },
      error: (error) => {
        console.error(error);
        this.waiting=false;
        this.addMessage(this.liveChat, this.botName)
        this.liveChat=""
      },
      complete: () => {
        console.log('Stream completed');
        this.waiting=false;
        this.addMessage(this.liveChat, this.botName)
        this.liveChat=""
      },
    });
    /*this._apiService.getResponse(message)
      .subscribe({
        next: (res) => {
          console.log(res);
          let response = res.response ? res.response: "";
          this.addMessage(response, this.botName);
          this.waiting = false;
        },
        error: (e) => {
          console.log(e)
          if(e.status==0){
            this.addMessage("Error, could not get response :(", this.botName);
            this.waiting = false;
          }
        }
      })*/
  }

  messages = [
    {id: 0, msg: "This is the digital student advisor! How may I help you?😏", src: this.botName}
    /*{id: 1, msg: "HI there", src: "You"},
    {id: 2, msg: "Hello, i am bot", src: "Digital Study Advisor"},
    {id: 3, msg: "Cool, i am not bot", src: "You"},
    {id: 4, msg: "Nah you are geh", src: "Digital Study Advisor"},
    {id: 5, msg: "Spam", src: "Digital Study Advisor"},
    {id: 6, msg: "Spam", src: "Digital Study Advisor"},
    {id: 7, msg: "Spam", src: "Digital Study Advisor"},
    {id: 8, msg: "Super long message Super long messageSuper long messageSuper long messageSuper long messageSuper long messageSuper long messageSuper long messageSuper long messageSuper long message", src: "Digital Study Advisor"},
    {id: 9, msg: "End", src: "Digital Study Advisor"}*/
  ]
}

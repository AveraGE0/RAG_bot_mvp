import { Pipe, PipeTransform } from '@angular/core';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';

@Pipe({
  name: 'linkify',
  standalone: true,
})
export class LinkifyPipe implements PipeTransform {
  constructor(private sanitizer: DomSanitizer) {}

  transform(text: string): SafeHtml {
    if (!text) return '';
    text = text.replace(/[<>]/g, '');
    const transformedText = text.replace(/(https?:\/\/[^\s]+)/g, url => `<a href="${url}" target="_blank">link</a>`);
    return this.sanitizer.bypassSecurityTrustHtml(transformedText);
  }
}

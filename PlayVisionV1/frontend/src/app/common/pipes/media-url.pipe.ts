import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'mediaUrl',
  standalone: true
})
export class MediaUrlPipe implements PipeTransform {
  private apiHost = 'http://localhost:80';

  transform(path: string): string {
    if (!path) return '';
    return `/media/${path}`;
  }
}

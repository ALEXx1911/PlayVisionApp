import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';
import { MatIconModule } from '@angular/material/icon';

@Component({
  selector: 'app-footer',
  imports: [RouterLink,MatIconModule],
  templateUrl: './app-footer.html',
  styleUrl: './app-footer.css',
})
export class AppFooter {

}

import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { CompetitionNavbar } from "./competition-navbar/competition-navbar";
import { AppHeader } from "./app-header/app-header";
import { AppFooter } from "./app-footer/app-footer";

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, CompetitionNavbar, AppHeader, AppFooter],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected readonly title = signal('frontend');
}

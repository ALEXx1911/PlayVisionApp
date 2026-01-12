import { Component, effect, signal, ViewChild } from '@angular/core';
import { NavigationEnd, Router, RouterOutlet } from '@angular/router';
import { CompetitionNavbar } from "./competition-navbar/competition-navbar";
import { AppHeader } from "./app-header/app-header";
import { AppFooter } from "./app-footer/app-footer";
import {MatDrawer, MatSidenavModule} from '@angular/material/sidenav';
import { SideNavService } from './services/sideNav-service/sideNav-service';
import { filter } from 'rxjs';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, CompetitionNavbar, AppHeader, AppFooter , MatSidenavModule],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected readonly title = signal('frontend');
  competitionNavbarOpen = signal(false);

  constructor(private sideNavService: SideNavService, private router: Router) {
    effect(() => {
      this.competitionNavbarOpen.set(this.sideNavService.isOpen());
    })
    //Close the drawer on route change
    this.router.events.pipe(filter(e => e instanceof NavigationEnd))
    .subscribe(() => {
      this.sideNavService.close();
    })
  }

  closeDrawer(){
    this.competitionNavbarOpen.set(false);
    this.sideNavService.close();
  }


}

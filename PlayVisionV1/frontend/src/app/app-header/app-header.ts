import { Component, EventEmitter, Output } from '@angular/core';
import { RouterLink, RouterLinkActive } from '@angular/router';
import { MatIcon } from "@angular/material/icon";
import { SideNavService } from '../services/sideNav-service/sideNav-service';

@Component({
  selector: 'app-header',
  imports: [RouterLink,RouterLinkActive, MatIcon],
  templateUrl: './app-header.html',
  styleUrl: './app-header.css',
})
export class AppHeader {

    @Output() menuToggle = new EventEmitter<void>();

    constructor(private sideNavService: SideNavService) {}

    onMenuToggle() {
      this.sideNavService.toggle();
    }
    readonly navOptions = [
      {
      label:"Home",
      route:"/home"
    },
    {
      label:"Search",
      route:"/search"
    },
    {
      label:"Compare",
      route:"/compare"
    },
    {
      label:"About Us",
      route:"/aboutUs"
    },
    ]
}

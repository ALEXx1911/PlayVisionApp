import { Component } from '@angular/core';
import { RouterLink, RouterLinkActive } from '@angular/router';
import { MatIcon } from "@angular/material/icon";

@Component({
  selector: 'app-header',
  imports: [RouterLink,RouterLinkActive, MatIcon],
  templateUrl: './app-header.html',
  styleUrl: './app-header.css',
})
export class AppHeader {
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

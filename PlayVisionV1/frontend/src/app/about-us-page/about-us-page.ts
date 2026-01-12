import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-about-us-page',
  imports: [],
  templateUrl: './about-us-page.html',
  styleUrl: './about-us-page.css',
})
export class AboutUsPage {
  infoCard1 = ["PlayVision was born as a class project, where we put into practice all the techniques we have learned throughout our years as students.",
    "And thus create a professional application that is up to the users.",
    "To be able to create a project that we love to work on and continue to improve, we have combined two of our great passions in PlayVision, technology and football."
  ];
  infoCard2= ["The main objective of PlayVision is to bring together in one place the most relevant data in the world of football.",
    "Such as: live results, match statistics, club data, competitions, players, etc.",
    "All this with the aim that users do not have to bother looking for that data elsewhere."
  ]; 
}

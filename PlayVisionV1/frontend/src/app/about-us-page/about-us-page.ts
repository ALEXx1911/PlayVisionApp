import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-about-us-page',
  imports: [RouterLink],
  templateUrl: './about-us-page.html',
  styleUrl: './about-us-page.css',
})
export class AboutUsPage {
  infoCard1 = ["PlayVison nace como un proyecto para clase, en el ponemos en práctica todas las técnicas aprendidas a lo largo de nuestros años siendo estudiantes.",
    "Y así crear una aplicación profesional que este a la altura de los usuarios.",
    "Para poder crear un proyecto en el que nos encante trabajar y seguir superandonos, hemos juntado en PlayVision dos de nuestras grandes pasiones, la tecnología y el fútbol."
  ];
  infoCard2= ["El principal objetivo de PlayVision, es poder reunir en un solo sitio, los datos más relevantes en el mundo del fútbol.",
    "Tales como: resultados en vivo, estadísticas de partidos, datos de clubes, competiciones, jugadores, etc.",
    "Todo esto con el fin de que los usuarios no se tengan que molestar en buscar esos datos en otros sitios."
  ]; 
}

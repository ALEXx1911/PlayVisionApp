import { Component, input, InputSignal } from "@angular/core";
import { Match } from "../../../models/app-models";
import { RouterLink } from "@angular/router";
import { MatIcon } from "@angular/material/icon";

@Component({
    selector: "home-match-slot",
    imports: [RouterLink, MatIcon],
    templateUrl: "./home-match-slot.html",

})
export class HomeMatchSlot{
    readonly matchData: InputSignal<Match> = input.required<Match>();
}
//{{matchData().away_team.logo_url}}
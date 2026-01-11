import { Component, input, InputSignal } from "@angular/core";
import { Match } from "../../../models/app-models";
import { RouterLink } from "@angular/router";

@Component({
    selector: "match-slot",
    imports: [RouterLink],
    templateUrl: "./match-slot.html",

})
export class MatchSlot{
    readonly matchData: InputSignal<Match> = input.required<Match>();
}
//{{matchData().away_team.logo_url}}
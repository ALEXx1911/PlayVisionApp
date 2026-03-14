import { Component, input, InputSignal } from "@angular/core";
import { Match } from "../../../models/app-models";
import { RouterLink } from "@angular/router";
import { MatIcon } from "@angular/material/icon";

@Component({
    selector: "simple-match-slot",
    imports: [RouterLink, MatIcon],
    templateUrl: "./simple-match-slot.html",
})
export class SimpleMatchSlot{
    readonly matchData: InputSignal<Match> = input.required<Match>();
}
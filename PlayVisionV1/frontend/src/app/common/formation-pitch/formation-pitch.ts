import { Component, computed, input, signal } from "@angular/core";
import { FORMATIONS, PlayerSlotWithCoords} from "./formations";
import { PlayerSlotLineup } from "../../models/app-models";

@Component({
    selector: 'app-formation-pitch',
    imports: [],
    templateUrl: './formation-pitch.html',
})
export class FormationPitch {
    //formationNames = Object.keys(FORMATIONS);

    formation = signal(FORMATIONS['4-3-3']);
    flipPitch = signal(false);
    playersLineup = input<PlayerSlotWithCoords[]>([]);
    playerSlotsWithCoordsComputed = computed(() => 
        this.playersLineup()
    );

    changeFormation(formationName: string): void {
        //this.formation.set(FORMATIONS[formationName]);
    }
}
import { PlayerSlotLineup, PlayerStat } from "../../models/app-models";
import { PlayersListWithFlag, PlayerSlot } from "../../models/team-models/team-models";

type PlayerPosition = 
    | 'GK' 
    | 'LB' | 'LCB'| 'CB' | 'RCB' | 'RB' 
    | 'CDM' | 'LCM' | 'CM' | 'RCM' | 'MP' | 'LM' | 'RM' 
    | 'RW' | 'LW' | 'SS' | 'DC';

export interface FormationSlot {
    label: string;
    x: number;
    y: number;
}

export interface PlayerSlotWithCoords extends PlayerSlotLineup{
    x: number;
    y: number;
}

export const FORMATIONS: Record<string, FormationSlot[]> = {
    '4-3-3': [
        { label: 'GK', x: 10, y: 50 },

        { label: 'LB', x: 25, y: 15 },
        { label: 'LCB', x: 25, y: 40 },
        { label: 'RCB', x: 25, y: 60 },
        { label: 'RB', x: 25, y: 85 },

        { label: 'RCM', x: 60, y: 30 },
        { label: 'CM', x: 45, y: 50 },
        { label: 'LCM', x: 60, y: 70 },

        { label: 'RW', x: 80, y: 15 },
        { label: 'DC', x: 85, y: 50 },
        { label: 'LW', x: 80, y: 85 }, 
    ],
    '4-4-2': [
        { label: 'GK', x: 10, y: 50 },

        { label: 'LB', x: 25, y: 15 },
        { label: 'LCB', x: 25, y: 40 },
        { label: 'RCB', x: 25, y: 60 },
        { label: 'RB', x: 25, y: 85 },

        { label: 'LM', x: 45, y: 15 },
        { label: 'LCM', x: 45, y: 40 },
        { label: 'RCM', x: 45, y: 60 },
        { label: 'RM', x: 45, y: 85 },

        { label: 'DC', x: 65, y: 30 },
        { label: 'SS', x: 65, y: 70 },
    ],
    '4-2-3-1': [
        { label: 'GK', x: 10, y: 50 },

        { label: 'LB', x: 25, y: 15 },
        { label: 'LCB', x: 25, y: 40 },
        { label: 'RCB', x: 25, y: 60 },
        { label: 'RB', x: 25, y: 85 },

        { label: 'LCM', x: 45, y: 35 },
        { label: 'RCM', x: 45, y: 65 },

        { label: 'LW', x: 70, y: 15 },
        { label: 'MP', x: 70, y: 50 },
        { label: 'RW', x: 70, y: 85 },

        { label: 'DC', x: 85, y: 50 },
    ],
    '3-5-2': [
        { label: 'GK', x: 10, y: 50 },

        { label: 'LCB', x: 25, y: 30 },
        { label: 'CB', x: 25, y: 50 },
        { label: 'RCB', x: 25, y: 70 },
        
        { label: 'LCM', x: 45, y: 35 },
        { label: 'RCM', x: 45, y: 65 },

        { label: 'LM', x: 65, y: 20 },
        { label: 'RM', x: 65, y: 80 },
        { label: 'MP', x: 65, y: 50 },

        { label: 'DC', x: 85, y: 35 },
        { label: 'SS', x: 85, y: 65 },
    ]
};

export function mapPlayersToFormationSlots(formationKey: string, playersLineup: PlayerSlotLineup[]): PlayerSlotWithCoords[] {
    const formation = FORMATIONS[formationKey];

    return formation.map(slot => {
        const player = playersLineup.find(p => p.position === slot.label);
        if (!player) return null;
        
        return{
            ...player,
            x: slot.x,
            y: slot.y,
        }
    }).filter(Boolean) as PlayerSlotWithCoords[];
}

export function mapPlayersDataToFormationSlots(formationKey: string, playersLineup: PlayerSlotLineup[]): PlayerSlotWithCoords[] {
    const formation = FORMATIONS[formationKey];

    return formation.map(slot => {
        const playerSlot = playersLineup.find(p => p.position === slot.label);
        if (!playerSlot) return null;
        
        return{
            pname: playerSlot.pname,
            position: playerSlot.position,
            media: playerSlot.media,
            dorsal: playerSlot.dorsal,
            team_name: playerSlot.team_name,
            team_logo_url: playerSlot.team_logo_url,
            x: slot.x,
            y: slot.y,
        }
    }).filter(Boolean) as PlayerSlotWithCoords[];
}
import { signal } from "@angular/core";

export type PlayerAnalysisMessage = {
    key: string;
    message: string;
};

export const DEFAULT_MESSAGES_TO_ANALIZE_DATA = signal<PlayerAnalysisMessage[]>([
    {
        key: 'Goalkeeper Stats',
        message: 'When analyzing goalkeepers, the focus should be on shot-stopping ability and reliability and clean sheets'
    },
    {
        key: 'Defender Stats',
        message: 'For defenders, defensive consistency and positioning are essential. Important statistics include tackles won, interceptions.It is also useful to consider passing accuracy to evaluate their contribution to ball progression'
    },
    {
        key: 'Winger Stats',
        message: 'Wingers require a balance between defense and attack. Relevant statistics include crosses completed, assists, key passes, and dribbles, alongside defensive actions such as tackles and recoveries'
    },
    {
        key: 'Midfielder Stats',
        message: 'Midfield analysis should focus on control, creativity, and work rate.Key metrics include passes completed, pass accuracy, chances created, and ball recoveries'
    },
    {
        key: 'Forward Stats',
        message: 'For forwards, the main focus is efficiency in scoring and attacking contribution. Important statistics include goals, shots on target, conversion rate, and assists'
    }
]);

export type MatchAnalysisMessage = {
  key: string;
  message: string;
};

export const DEFAULT_MESSAGES_TO_ANALYZE_MATCH_DATA = signal<MatchAnalysisMessage[]>([
  {
    key: 'Match Result',
    message: 'The final score provides an overview of the match outcome. It should be analyzed together with goal timing and goal difference to understand how the result was achieved'
  },
  {
    key: 'Possession and Passing',
    message: 'Possession and passing statistics show which team controlled the match. Key metrics include possession percentage, total passes, pass accuracy, and passes in the final third'
  },
  {
    key: 'Attacking Performance',
    message: 'Attacking performance highlights chance creation and efficiency. Important statistics include shots, shots on target, big chances created, expected goals, and touches inside the penalty area'
  },
  {
    key: 'Defensive Performance',
    message: 'Defensive statistics reflect how well teams prevented scoring opportunities. Metrics such as tackles, interceptions, clearances, blocks, and saves are essential for analysis'
  },
  {
    key: 'Discipline and Fouls',
    message: 'Disciplinary data shows the physical and tactical intensity of the match. Fouls committed, yellow cards, red cards, and offsides can significantly affect match flow'
  },
  {
    key: 'Set Pieces',
    message: 'Set-piece statistics help evaluate effectiveness in dead-ball situations. Corners, free kicks, penalties, and goals from set pieces indicate preparation and execution'
  }
]);

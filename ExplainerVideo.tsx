import React from 'react';
import { AbsoluteFill, Sequence } from 'remotion';
import { PALETTE } from './theme';
import { Scene1Hook } from './scenes/Scene1Hook';
import { Scene2WhatIsIt } from './scenes/Scene2WhatIsIt';
import { Scene3InsideBody } from './scenes/Scene3InsideBody';
import { Scene4RiskFactors } from './scenes/Scene4RiskFactors';
import { Scene5HowToFindOut } from './scenes/Scene5HowToFindOut';
import { Scene6GoodNews } from './scenes/Scene6GoodNews';
import { Scene7Closing } from './scenes/Scene7Closing';

export const ExplainerVideo: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: PALETTE.bg }}>
      {/* 0:00 - 0:16 (480 frames): Hook & Global Prevalence */}
      <Sequence from={0} durationInFrames={480}>
        <Scene1Hook />
      </Sequence>

      {/* 0:16 - 0:32 (480 frames): What Is Prediabetes & A1C Gauge */}
      <Sequence from={480} durationInFrames={480}>
        <Scene2WhatIsIt />
      </Sequence>

      {/* 0:32 - 0:48 (480 frames): What Happens Inside the Body */}
      <Sequence from={960} durationInFrames={480}>
        <Scene3InsideBody />
      </Sequence>

      {/* 0:48 - 1:10 (660 frames): Combined Risk Factors */}
      <Sequence from={1440} durationInFrames={660}>
        <Scene4RiskFactors />
      </Sequence>

      {/* 1:10 - 1:30 (600 frames): How Do You Find Out? (Fixed Layout + Ranges) */}
      <Sequence from={2100} durationInFrames={600}>
        <Scene5HowToFindOut />
      </Sequence>

      {/* 1:30 - 1:45 (450 frames): The Good News (58% Reduction) */}
      <Sequence from={2700} durationInFrames={450}>
        <Scene6GoodNews />
      </Sequence>

      {/* 1:45 - 2:00 (450 frames): Take Action Today + Purpose & References */}
      <Sequence from={3150} durationInFrames={450}>
        <Scene7Closing />
      </Sequence>
    </AbsoluteFill>
  );
};

import React from 'react';
import { Composition } from 'remotion';
import { ExplainerVideo } from './ExplainerVideo';
import { VIDEO_CONFIG } from './theme';

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="PrediabetesExplainer"
      component={ExplainerVideo}
      durationInFrames={VIDEO_CONFIG.totalFrames}
      fps={VIDEO_CONFIG.fps}
      width={VIDEO_CONFIG.width}
      height={VIDEO_CONFIG.height}
    />
  );
};

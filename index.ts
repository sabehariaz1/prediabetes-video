import { registerRoot, Composition } from 'remotion';
import React from 'react';
import { ExplainerVideo } from './ExplainerVideo';

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="PrediabetesExplainer"
      component={ExplainerVideo}
      durationInFrames={450}
      fps={30}
      width={1920}
      height={1080}
    />
  );
};

registerRoot(RemotionRoot);

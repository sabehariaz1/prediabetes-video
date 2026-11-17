import React from 'react';
import {
  AbsoluteFill,
  Sequence,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
} from 'remotion';

const SceneContainer: React.FC<{
  children: React.ReactNode;
  bgColor: string;
}> = ({ children, bgColor }) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 15], [0, 1], {
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: bgColor,
        justifyContent: 'center',
        alignItems: 'center',
        padding: 80,
        fontFamily: 'system-ui, -apple-system, sans-serif',
        opacity,
      }}
    >
      {children}
    </AbsoluteFill>
  );
};

export const ExplainerVideo: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const scale = spring({
    frame,
    fps,
    config: { damping: 12 },
  });

  return (
    <AbsoluteFill style={{ backgroundColor: '#0F172A' }}>
      {/* SCENE 1: Hook & Definition (0s - 5s) */}
      <Sequence from={0} durationInFrames={150}>
        <SceneContainer bgColor="#0F172A">
          <div style={{ textAlign: 'center', transform: `scale(${scale})` }}>
            <span
              style={{
                backgroundColor: '#F59E0B',
                color: '#0F172A',
                padding: '10px 24px',
                borderRadius: 50,
                fontSize: 28,
                fontWeight: 700,
                textTransform: 'uppercase',
                letterSpacing: 2,
              }}
            >
              Health Alert
            </span>
            <h1
              style={{
                color: '#F8FAFC',
                fontSize: 84,
                marginTop: 30,
                marginBottom: 20,
              }}
            >
              What is Prediabetes?
            </h1>
            <p
              style={{
                color: '#94A3B8',
                fontSize: 40,
                maxWidth: 1100,
                lineHeight: 1.4,
              }}
            >
              Blood sugar levels are higher than normal, but not yet high enough
              to be diagnosed as Type 2 diabetes.
            </p>
          </div>
        </SceneContainer>
      </Sequence>

      {/* SCENE 2: Diagnostic Numbers (5s - 10s) */}
      <Sequence from={150} durationInFrames={150}>
        <SceneContainer bgColor="#1E293B">
          <div style={{ textAlign: 'center', width: '100%' }}>
            <h2 style={{ color: '#38BDF8', fontSize: 64, marginBottom: 50 }}>
              Know Your Numbers
            </h2>
            <div
              style={{
                display: 'flex',
                justifyContent: 'center',
                gap: 40,
              }}
            >
              <div
                style={{
                  backgroundColor: '#0F172A',
                  padding: 40,
                  borderRadius: 24,
                  width: 480,
                  border: '2px solid #38BDF8',
                }}
              >
                <div style={{ color: '#94A3B8', fontSize: 30 }}>HbA1c Test</div>
                <div
                  style={{
                    color: '#F59E0B',
                    fontSize: 72,
                    fontWeight: 800,
                    margin: '15px 0',
                  }}
                >
                  5.7% – 6.4%
                </div>
                <div style={{ color: '#CBD5E1', fontSize: 26 }}>
                  3-Month Average Blood Sugar
                </div>
              </div>

              <div
                style={{
                  backgroundColor: '#0F172A',
                  padding: 40,
                  borderRadius: 24,
                  width: 480,
                  border: '2px solid #38BDF8',
                }}
              >
                <div style={{ color: '#94A3B8', fontSize: 30 }}>
                  Fasting Glucose
                </div>
                <div
                  style={{
                    color: '#F59E0B',
                    fontSize: 72,
                    fontWeight: 800,
                    margin: '15px 0',
                  }}
                >
                  100 – 125
                </div>
                <div style={{ color: '#CBD5E1', fontSize: 26 }}>
                  mg/dL After Overnight Fast
                </div>
              </div>
            </div>
          </div>
        </SceneContainer>
      </Sequence>

      {/* SCENE 3: Reversibility & Action (10s - 15s) */}
      <Sequence from={300} durationInFrames={150}>
        <SceneContainer bgColor="#064E3B">
          <div style={{ textAlign: 'center' }}>
            <h2 style={{ color: '#6EE7B7', fontSize: 76, marginBottom: 30 }}>
              The Good News: It’s Reversible
            </h2>
            <p
              style={{
                color: '#ECFDF5',
                fontSize: 42,
                maxWidth: 1150,
                lineHeight: 1.5,
              }}
            >
              Losing just <strong>5% to 7%</strong> of body weight and getting{' '}
              <strong>150 minutes</strong> of brisk walking per week can cut
              your risk of Type 2 diabetes by up to <strong>58%</strong>.
            </p>
          </div>
        </SceneContainer>
      </Sequence>
    </AbsoluteFill>
  );
};

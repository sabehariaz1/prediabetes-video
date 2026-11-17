import React from 'react';
import {
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
  Easing,
} from 'remotion';
import { PALETTE, SERIF } from '../theme';
import { SlideShell } from '../components/SlideShell';
import { HeartIcon } from '../components/Icons';

export const Scene6GoodNews: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const countProgress = interpolate(frame, [20, 110], [0, 1], {
    easing: Easing.out(Easing.cubic),
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const pct = Math.round(countProgress * 58);

  const pillars = [
    { text: 'Lose 5%–7% of body weight', delay: 140 },
    { text: '150 minutes of brisk activity a week', delay: 210 },
    { text: 'Eat more whole, high-fiber foods', delay: 280 },
  ];

  let caption =
    'In the landmark Diabetes Prevention Program study, healthy lifestyle changes lowered type 2 diabetes risk by 58%.';
  if (frame >= 140) {
    caption =
      'Losing 5% to 7% of body weight, walking 150 minutes a week, and eating whole foods can reverse prediabetes.';
  }

  return (
    <SlideShell
      title="The Good News: You Can Lower Your Risk"
      caption={caption}
    >
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          gap: 90,
          width: '100%',
        }}
      >
        {/* Left: 58% Counter */}
        <div style={{ flex: 0.9, textAlign: 'left' }}>
          <HeartIcon />
          <div
            style={{
              fontFamily: SERIF,
              fontSize: 132,
              fontWeight: 700,
              color: PALETTE.teal,
              lineHeight: 1,
            }}
          >
            {pct}%
          </div>
          <div
            style={{
              fontFamily: SERIF,
              fontSize: 36,
              fontWeight: 700,
              color: PALETTE.navy,
              marginTop: 14,
              lineHeight: 1.3,
            }}
          >
            lower risk of type 2 diabetes with lifestyle changes
          </div>
          <div
            style={{
              fontFamily: SERIF,
              fontSize: 22,
              color: PALETTE.slate,
              marginTop: 14,
            }}
          >
            Diabetes Prevention Program Clinical Study
          </div>
        </div>

        {/* Right: 3 Action Pills */}
        <div
          style={{
            flex: 1.1,
            display: 'flex',
            flexDirection: 'column',
            gap: 26,
          }}
        >
          {pillars.map((p, idx) => {
            const scale = spring({
              frame: Math.max(0, frame - p.delay),
              fps,
              config: { damping: 16, stiffness: 120 },
            });
            const opacity = interpolate(frame, [p.delay, p.delay + 15], [0, 1], {
              extrapolateLeft: 'clamp',
              extrapolateRight: 'clamp',
            });

            return (
              <div
                key={idx}
                style={{
                  backgroundColor: PALETTE.white,
                  border: `3px solid ${PALETTE.navy}`,
                  borderRadius: 20,
                  padding: '26px 34px',
                  display: 'flex',
                  alignItems: 'center',
                  gap: 22,
                  boxShadow: '0 8px 20px rgba(15, 43, 70, 0.05)',
                  transform: `scale(${scale})`,
                  opacity,
                }}
              >
                <div
                  style={{
                    width: 44,
                    height: 44,
                    borderRadius: '50%',
                    backgroundColor: PALETTE.teal,
                    color: PALETTE.white,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontSize: 26,
                    fontWeight: 900,
                    flexShrink: 0,
                  }}
                >
                  ✓
                </div>
                <span
                  style={{
                    fontFamily: SERIF,
                    fontSize: 32,
                    fontWeight: 700,
                    color: PALETTE.navy,
                  }}
                >
                  {p.text}
                </span>
              </div>
            );
          })}
        </div>
      </div>
    </SlideShell>
  );
};

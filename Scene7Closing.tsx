import React from 'react';
import { useCurrentFrame, interpolate, Easing } from 'remotion';
import { PALETTE, SERIF } from '../theme';
import { SlideShell } from '../components/SlideShell';

export const Scene7Closing: React.FC = () => {
  const frame = useCurrentFrame();

  const steps = [
    { text: 'Know your personal risk factors', delay: 15 },
    { text: 'Ask your doctor about a simple blood test', delay: 65 },
    { text: 'Move more, eat balanced meals, and sleep well', delay: 115 },
    {
      text: 'Small daily steps protect your health for years',
      delay: 165,
      accent: true,
    },
  ];

  return (
    <SlideShell
      title="Take Action Today"
      caption="This video is created for community education and awareness only, and is not personal medical advice."
    >
      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          width: '100%',
          maxWidth: 1320,
        }}
      >
        <div
          style={{
            display: 'flex',
            flexDirection: 'column',
            gap: 22,
            width: '100%',
            paddingLeft: 60,
          }}
        >
          {steps.map((s, idx) => {
            const opacity = interpolate(frame, [s.delay, s.delay + 18], [0, 1], {
              extrapolateLeft: 'clamp',
              extrapolateRight: 'clamp',
            });
            const x = interpolate(frame, [s.delay, s.delay + 18], [24, 0], {
              easing: Easing.out(Easing.cubic),
              extrapolateLeft: 'clamp',
              extrapolateRight: 'clamp',
            });

            return (
              <div
                key={idx}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: 22,
                  opacity,
                  transform: `translateX(${x}px)`,
                }}
              >
                <div
                  style={{
                    width: 40,
                    height: 40,
                    borderRadius: '50%',
                    backgroundColor: s.accent ? '#67E8F9' : PALETTE.teal,
                    color: PALETTE.white,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontSize: 24,
                    fontWeight: 900,
                    flexShrink: 0,
                  }}
                >
                  ✓
                </div>
                <span
                  style={{
                    fontFamily: SERIF,
                    fontSize: 38,
                    fontWeight: 700,
                    color: s.accent ? PALETTE.teal : PALETTE.navy,
                  }}
                >
                  {s.text}
                </span>
              </div>
            );
          })}
        </div>

        {/* Community Awareness Purpose & Scientific References Box */}
        <div
          style={{
            marginTop: 38,
            width: '100%',
            backgroundColor: PALETTE.white,
            border: `2px solid ${PALETTE.border}`,
            borderLeft: `8px solid ${PALETTE.teal}`,
            borderRadius: 16,
            padding: '20px 30px',
            opacity: interpolate(frame, [210, 235], [0, 1], {
              extrapolateLeft: 'clamp',
              extrapolateRight: 'clamp',
            }),
          }}
        >
          <div
            style={{
              fontSize: 21,
              color: PALETTE.navy,
              lineHeight: 1.45,
            }}
          >
            <strong>Purpose:</strong> Created to spread community awareness and
            help everyday people understand, prevent, and reverse prediabetes.
          </div>
          <div
            style={{
              fontSize: 19,
              color: PALETTE.slate,
              marginTop: 8,
            }}
          >
            <strong>Scientific References:</strong> American Diabetes
            Association (ADA) Standards of Care in Diabetes &amp; CDC
            Prediabetes Prevention Guidelines.
          </div>
        </div>
      </div>
    </SlideShell>
  );
};

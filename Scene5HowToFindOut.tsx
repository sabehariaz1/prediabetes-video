import React from 'react';
import { useCurrentFrame, useVideoConfig, interpolate, spring } from 'remotion';
import { PALETTE, SERIF } from '../theme';
import { SlideShell } from '../components/SlideShell';
import {
  BloodDropIcon,
  GlucoseMeterIcon,
  GlucoseDrinkIcon,
} from '../components/Icons';

export const Scene5HowToFindOut: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const tests = [
    {
      name: 'A1C Test',
      desc: 'Average blood sugar over 2–3 months',
      normal: 'Below 5.7%',
      prediabetes: '5.7% – 6.4%',
      delay: 30,
      icon: <BloodDropIcon />,
    },
    {
      name: 'Fasting Glucose',
      desc: 'Blood sugar after not eating overnight',
      normal: 'Below 100 mg/dL',
      prediabetes: '100 – 125 mg/dL',
      delay: 140,
      icon: <GlucoseMeterIcon />,
    },
    {
      name: 'Glucose Tolerance',
      desc: 'Blood sugar 2 hours after a sweet drink',
      normal: 'Below 140 mg/dL',
      prediabetes: '140 – 199 mg/dL',
      delay: 250,
      icon: <GlucoseDrinkIcon />,
    },
  ];

  return (
    <SlideShell
      title="How Do You Find Out?"
      caption="The only way to know for sure is a simple blood test—ask your doctor how often you should be tested."
    >
      <div
        style={{
          display: 'flex',
          gap: 36,
          width: '100%',
          alignItems: 'stretch',
          justifyContent: 'center',
        }}
      >
        {tests.map((t, idx) => {
          const scale = spring({
            frame: Math.max(0, frame - t.delay),
            fps,
            config: { damping: 16, stiffness: 120 },
          });
          const opacity = interpolate(frame, [t.delay, t.delay + 18], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          });

          return (
            <div
              key={idx}
              style={{
                flex: 1,
                maxWidth: 540,
                backgroundColor: PALETTE.white,
                border: `3px solid ${PALETTE.navy}`,
                borderRadius: 24,
                padding: '26px 28px',
                boxShadow: '0 10px 26px rgba(15, 43, 70, 0.06)',
                transform: `scale(${scale})`,
                opacity,
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                textAlign: 'center',
              }}
            >
              <div style={{ marginBottom: 12 }}>{t.icon}</div>

              <div
                style={{
                  fontFamily: SERIF,
                  fontSize: 34,
                  fontWeight: 700,
                  color: PALETTE.navy,
                }}
              >
                {t.name}
              </div>

              <div
                style={{
                  fontFamily: SERIF,
                  fontSize: 22,
                  color: PALETTE.slate,
                  marginTop: 8,
                  marginBottom: 20,
                  lineHeight: 1.35,
                  padding: '0 8px',
                }}
              >
                {t.desc}
              </div>

              <div
                style={{
                  width: '100%',
                  marginTop: 'auto',
                  display: 'flex',
                  flexDirection: 'column',
                  gap: 10,
                }}
              >
                <div
                  style={{
                    backgroundColor: PALETTE.tealLight,
                    borderLeft: `6px solid ${PALETTE.teal}`,
                    borderRadius: 10,
                    padding: '10px 16px',
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                  }}
                >
                  <span
                    style={{
                      fontSize: 20,
                      fontWeight: 700,
                      color: PALETTE.teal,
                    }}
                  >
                    Normal:
                  </span>
                  <span
                    style={{
                      fontSize: 21,
                      fontWeight: 800,
                      color: PALETTE.navy,
                    }}
                  >
                    {t.normal}
                  </span>
                </div>

                <div
                  style={{
                    backgroundColor: PALETTE.amberLight,
                    borderLeft: `6px solid ${PALETTE.amber}`,
                    borderRadius: 10,
                    padding: '10px 16px',
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                  }}
                >
                  <span
                    style={{
                      fontSize: 20,
                      fontWeight: 700,
                      color: PALETTE.amber,
                    }}
                  >
                    Prediabetes:
                  </span>
                  <span
                    style={{
                      fontSize: 21,
                      fontWeight: 800,
                      color: PALETTE.navy,
                    }}
                  >
                    {t.prediabetes}
                  </span>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </SlideShell>
  );
};

import React from 'react';
import { useCurrentFrame, useVideoConfig, interpolate, spring } from 'remotion';
import { PALETTE, SERIF } from '../theme';
import { SlideShell } from '../components/SlideShell';

export const Scene4RiskFactors: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const groups = [
    {
      header: 'Factors You Can’t Change',
      badgeBg: PALETTE.coral,
      borderColor: PALETTE.coral,
      delay: 15,
      items: [
        { title: 'Age 45 or Older', desc: 'Risk naturally rises as we get older' },
        {
          title: 'Family History',
          desc: 'A parent or sibling with type 2 diabetes',
        },
        {
          title: 'Higher-Risk Backgrounds',
          desc: 'South Asian, Middle Eastern, African, Hispanic, or Indigenous heritage',
        },
      ],
    },
    {
      header: 'Daily Habits You Can Change',
      badgeBg: PALETTE.teal,
      borderColor: PALETTE.teal,
      delay: 180,
      items: [
        {
          title: 'Extra Belly Weight',
          desc: 'Carrying extra weight around the waist',
        },
        {
          title: 'Low Physical Activity',
          desc: 'Sitting too much or little regular movement',
        },
        {
          title: 'Sugary Foods & Poor Sleep',
          desc: 'Sweet drinks, processed snacks, smoking, or short sleep',
        },
      ],
    },
    {
      header: 'Related Health History',
      badgeBg: PALETTE.blue,
      borderColor: PALETTE.blue,
      delay: 360,
      items: [
        {
          title: 'High Blood Pressure or Cholesterol',
          desc: 'Elevated blood pressure or unhealthy blood fats',
        },
        {
          title: 'High Blood Sugar During Pregnancy',
          desc: 'A past history of pregnancy-related high blood sugar',
        },
        {
          title: 'PCOS or Heart History',
          desc: 'Polycystic ovary syndrome or past heart or stroke issues',
        },
      ],
    },
  ];

  let caption =
    'Some risk factors cannot be changed, like age over 45, family history, or ethnic background.';
  if (frame >= 180 && frame < 360) {
    caption =
      'Other risks come from daily habits you can improve—like extra belly weight, low activity, sugary drinks, or poor sleep.';
  } else if (frame >= 360) {
    caption =
      'Health history also matters, including high blood pressure, abnormal cholesterol, PCOS, or high blood sugar during pregnancy.';
  }

  return (
    <SlideShell
      title="What Raises Your Risk?"
      subtitleBadge={{ text: 'Risk Factors Add Up Over Time', bg: PALETTE.amber }}
      caption={caption}
    >
      <div
        style={{
          display: 'flex',
          gap: 36,
          width: '100%',
          alignItems: 'stretch',
        }}
      >
        {groups.map((grp, gIdx) => {
          const scale = spring({
            frame: Math.max(0, frame - grp.delay),
            fps,
            config: { damping: 16, stiffness: 120 },
          });
          const opacity = interpolate(
            frame,
            [grp.delay, grp.delay + 18],
            [0, 1],
            {
              extrapolateLeft: 'clamp',
              extrapolateRight: 'clamp',
            }
          );

          return (
            <div
              key={gIdx}
              style={{
                flex: 1,
                backgroundColor: PALETTE.white,
                border: `3px solid ${grp.borderColor}`,
                borderRadius: 24,
                padding: '28px 32px',
                boxShadow: '0 10px 26px rgba(15, 43, 70, 0.06)',
                transform: `scale(${scale})`,
                opacity,
                display: 'flex',
                flexDirection: 'column',
              }}
            >
              <div
                style={{
                  backgroundColor: grp.badgeBg,
                  color: PALETTE.white,
                  fontSize: 21,
                  fontWeight: 800,
                  textTransform: 'uppercase',
                  letterSpacing: 1.2,
                  padding: '10px 18px',
                  borderRadius: 12,
                  textAlign: 'center',
                  marginBottom: 22,
                }}
              >
                {grp.header}
              </div>

              <div
                style={{
                  display: 'flex',
                  flexDirection: 'column',
                  gap: 20,
                  flex: 1,
                  justifyContent: 'center',
                }}
              >
                {grp.items.map((item, iIdx) => (
                  <div
                    key={iIdx}
                    style={{
                      borderBottom:
                        iIdx < 2 ? `1px solid ${PALETTE.border}` : 'none',
                      paddingBottom: iIdx < 2 ? 16 : 0,
                    }}
                  >
                    <div
                      style={{
                        fontFamily: SERIF,
                        fontSize: 27,
                        fontWeight: 700,
                        color: PALETTE.navy,
                      }}
                    >
                      • {item.title}
                    </div>
                    <div
                      style={{
                        fontSize: 21,
                        color: PALETTE.slate,
                        marginTop: 4,
                        lineHeight: 1.35,
                        paddingLeft: 20,
                      }}
                    >
                      {item.desc}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          );
        })}
      </div>
    </SlideShell>
  );
};

import React from 'react';
import { useCurrentFrame, interpolate, Easing } from 'remotion';
import { PALETTE, SERIF } from '../theme';
import { SlideShell } from '../components/SlideShell';
import { BloodDropIcon } from '../components/Icons';

export const Scene2WhatIsIt: React.FC = () => {
  const frame = useCurrentFrame();

  let needleAngle = -55;
  if (frame < 120) {
    needleAngle = -55;
  } else if (frame < 220) {
    needleAngle = interpolate(frame, [120, 160], [-55, 0], {
      easing: Easing.out(Easing.cubic),
      extrapolateRight: 'clamp',
    });
  } else if (frame < 310) {
    needleAngle = interpolate(frame, [220, 260], [0, 55], {
      easing: Easing.out(Easing.cubic),
      extrapolateRight: 'clamp',
    });
  } else {
    needleAngle = interpolate(frame, [310, 350], [55, 0], {
      easing: Easing.out(Easing.cubic),
      extrapolateRight: 'clamp',
    });
  }

  let caption =
    'Prediabetes means your blood sugar is higher than normal, but not yet high enough to be diabetes.';
  if (frame >= 90 && frame < 150) {
    caption =
      'A simple blood test called A1C shows your 3-month average blood sugar.';
  } else if (frame >= 150 && frame < 230) {
    caption = 'Below 5.7% is normal. Between 5.7% and 6.4% is prediabetes.';
  } else if (frame >= 230) {
    caption = 'And 6.5% or higher is diabetes.';
  }

  return (
    <SlideShell title="What Is Prediabetes?" caption={caption}>
      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          width: '100%',
        }}
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
          {/* Left Blood Drop Icon */}
          <div
            style={{
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              opacity: interpolate(frame, [70, 95], [0, 1], {
                extrapolateLeft: 'clamp',
                extrapolateRight: 'clamp',
              }),
            }}
          >
            <BloodDropIcon width={90} height={120} />
            <div
              style={{
                fontFamily: SERIF,
                fontSize: 30,
                fontWeight: 700,
                color: PALETTE.navy,
                marginTop: 12,
              }}
            >
              A1C Blood Test
            </div>
          </div>

          {/* Center Semicircular Gauge */}
          <div
            style={{
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
            }}
          >
            <svg width="640" height="320" viewBox="0 0 640 320">
              <path
                d="M 110 260 A 210 210 0 0 1 235 68"
                fill="none"
                stroke={PALETTE.teal}
                strokeWidth="44"
              />
              <path
                d="M 243 65 A 210 210 0 0 1 397 65"
                fill="none"
                stroke={PALETTE.amber}
                strokeWidth="44"
              />
              <path
                d="M 405 68 A 210 210 0 0 1 530 260"
                fill="none"
                stroke={PALETTE.coral}
                strokeWidth="44"
              />

              <text
                x="55"
                y="135"
                fill={PALETTE.teal}
                fontSize="28"
                fontWeight="700"
                fontFamily={SERIF}
              >
                Normal
              </text>
              <text
                x="242"
                y="28"
                fill={PALETTE.amber}
                fontSize="28"
                fontWeight="700"
                fontFamily={SERIF}
              >
                Prediabetes
              </text>
              <text
                x="485"
                y="135"
                fill={PALETTE.coral}
                fontSize="28"
                fontWeight="700"
                fontFamily={SERIF}
              >
                Diabetes
              </text>

              <g transform={`translate(320, 260) rotate(${needleAngle})`}>
                <line
                  x1="0"
                  y1="0"
                  x2="0"
                  y2="-165"
                  stroke={PALETTE.navy}
                  strokeWidth="9"
                  strokeLinecap="round"
                />
                <circle cx="0" cy="0" r="18" fill={PALETTE.navy} />
              </g>
            </svg>

            <div
              style={{
                fontFamily: SERIF,
                fontSize: 34,
                fontWeight: 700,
                color: PALETTE.navy,
                letterSpacing: 1,
              }}
            >
              3-MONTH BLOOD SUGAR (A1C)
            </div>
          </div>

          <div style={{ width: 140 }} />
        </div>

        {/* Bottom Legend Row */}
        <div
          style={{
            display: 'flex',
            gap: 64,
            marginTop: 34,
            opacity: interpolate(frame, [110, 135], [0, 1], {
              extrapolateLeft: 'clamp',
              extrapolateRight: 'clamp',
            }),
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
            <div
              style={{
                width: 22,
                height: 22,
                borderRadius: '50%',
                backgroundColor: PALETTE.teal,
              }}
            />
            <span
              style={{
                fontFamily: SERIF,
                fontSize: 32,
                fontWeight: 700,
                color: PALETTE.navy,
              }}
            >
              Normal: Below 5.7%
            </span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
            <div
              style={{
                width: 22,
                height: 22,
                borderRadius: '50%',
                backgroundColor: PALETTE.amber,
              }}
            />
            <span
              style={{
                fontFamily: SERIF,
                fontSize: 32,
                fontWeight: 700,
                color: PALETTE.navy,
              }}
            >
              Prediabetes: 5.7% – 6.4%
            </span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
            <div
              style={{
                width: 22,
                height: 22,
                borderRadius: '50%',
                backgroundColor: PALETTE.coral,
              }}
            />
            <span
              style={{
                fontFamily: SERIF,
                fontSize: 32,
                fontWeight: 700,
                color: PALETTE.navy,
              }}
            >
              Diabetes: 6.5% or higher
            </span>
          </div>
        </div>
      </div>
    </SlideShell>
  );
};

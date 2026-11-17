import React from 'react';
import { useCurrentFrame, interpolate, Easing } from 'remotion';
import { PALETTE, SERIF } from '../theme';
import { SlideShell } from '../components/SlideShell';

export const Scene3InsideBody: React.FC = () => {
  const frame = useCurrentFrame();

  const sugarMoveHealthy = interpolate(frame, [60, 160], [0, 250], {
    easing: Easing.inOut(Easing.cubic),
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const arrowHeight = interpolate(frame, [210, 290], [0, 160], {
    easing: Easing.out(Easing.cubic),
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  let caption =
    'Normally, insulin acts like a key that lets sugar move from your blood into your cells for energy.';
  if (frame >= 180) {
    caption =
      'With insulin resistance, your cells stop responding well—so sugar builds up in your blood.';
  }

  return (
    <SlideShell title="What Happens Inside the Body" caption={caption}>
      <div
        style={{
          display: 'flex',
          justifyContent: 'center',
          gap: 140,
          width: '100%',
        }}
      >
        {/* Left: Healthy Body */}
        <div
          style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
          }}
        >
          <div
            style={{
              fontFamily: SERIF,
              fontSize: 40,
              fontWeight: 700,
              color: PALETTE.teal,
              marginBottom: 34,
            }}
          >
            Healthy Body
          </div>

          <div
            style={{
              position: 'relative',
              width: 520,
              height: 260,
              display: 'flex',
              alignItems: 'center',
            }}
          >
            <div
              style={{
                display: 'flex',
                flexDirection: 'column',
                gap: 14,
                transform: `translateX(${sugarMoveHealthy}px)`,
              }}
            >
              {[0, 1, 2, 3, 4].map((i) => (
                <div
                  key={i}
                  style={{
                    width: 24,
                    height: 24,
                    borderRadius: '50%',
                    backgroundColor: '#F59E0B',
                  }}
                />
              ))}
            </div>
            <div
              style={{
                position: 'absolute',
                left: -12,
                bottom: 10,
                fontFamily: SERIF,
                fontSize: 26,
                color: PALETTE.slate,
              }}
            >
              sugar
            </div>

            <div
              style={{
                position: 'absolute',
                left: 110,
                backgroundColor: PALETTE.blue,
                color: PALETTE.white,
                fontFamily: SERIF,
                fontSize: 26,
                fontWeight: 700,
                padding: '12px 26px',
                borderRadius: 999,
                zIndex: 3,
              }}
            >
              insulin
            </div>

            <div
              style={{
                marginLeft: 'auto',
                width: 340,
                height: 230,
                border: `5px solid ${PALETTE.teal}`,
                borderRadius: 28,
                backgroundColor: PALETTE.white,
                display: 'flex',
                alignItems: 'flex-end',
                justifyContent: 'center',
                paddingBottom: 22,
              }}
            >
              <span
                style={{
                  fontFamily: SERIF,
                  fontSize: 34,
                  fontWeight: 700,
                  color: PALETTE.navy,
                }}
              >
                Cell
              </span>
            </div>
          </div>

          <div
            style={{
              fontFamily: SERIF,
              fontSize: 30,
              fontWeight: 700,
              color: PALETTE.teal,
              marginTop: 26,
            }}
          >
            Sugar enters cells for energy
          </div>
        </div>

        {/* Right: Insulin Resistance */}
        <div
          style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
          }}
        >
          <div
            style={{
              fontFamily: SERIF,
              fontSize: 40,
              fontWeight: 700,
              color: PALETTE.coral,
              marginBottom: 34,
            }}
          >
            Insulin Resistance
          </div>

          <div
            style={{
              position: 'relative',
              width: 540,
              height: 260,
              display: 'flex',
              alignItems: 'center',
            }}
          >
            {arrowHeight > 0 && (
              <svg
                width="44"
                height="200"
                style={{ position: 'absolute', left: -45, bottom: 35 }}
              >
                <line
                  x1="22"
                  y1="190"
                  x2="22"
                  y2={190 - arrowHeight}
                  stroke={PALETTE.coral}
                  strokeWidth="6"
                  strokeLinecap="round"
                />
                <polygon
                  points={`22,${176 - arrowHeight} 10,${196 - arrowHeight} 34,${196 - arrowHeight}`}
                  fill={PALETTE.coral}
                />
              </svg>
            )}

            <div
              style={{
                display: 'flex',
                flexDirection: 'column',
                gap: 14,
                marginLeft: 16,
              }}
            >
              {[0, 1, 2, 3, 4].map((i) => (
                <div
                  key={i}
                  style={{
                    width: 24,
                    height: 24,
                    borderRadius: '50%',
                    backgroundColor: '#F59E0B',
                  }}
                />
              ))}
            </div>
            <div
              style={{
                position: 'absolute',
                left: 4,
                bottom: 10,
                fontFamily: SERIF,
                fontSize: 26,
                color: PALETTE.slate,
              }}
            >
              sugar
            </div>

            <div
              style={{
                position: 'absolute',
                left: 120,
                backgroundColor: '#CBD5E1',
                color: PALETTE.white,
                fontFamily: SERIF,
                fontSize: 26,
                fontWeight: 700,
                padding: '12px 26px',
                borderRadius: 999,
                zIndex: 3,
              }}
            >
              insulin
              <span
                style={{
                  position: 'absolute',
                  inset: 0,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: PALETTE.coral,
                  fontSize: 48,
                  fontWeight: 900,
                }}
              >
                ✕
              </span>
            </div>

            <div
              style={{
                marginLeft: 'auto',
                width: 340,
                height: 230,
                border: `5px solid ${PALETTE.coral}`,
                borderRadius: 28,
                backgroundColor: PALETTE.white,
                display: 'flex',
                alignItems: 'flex-end',
                justifyContent: 'center',
                paddingBottom: 22,
              }}
            >
              <span
                style={{
                  fontFamily: SERIF,
                  fontSize: 34,
                  fontWeight: 700,
                  color: PALETTE.navy,
                }}
              >
                Cell
              </span>
            </div>
          </div>

          <div
            style={{
              fontFamily: SERIF,
              fontSize: 30,
              fontWeight: 700,
              color: PALETTE.coral,
              marginTop: 26,
            }}
          >
            Sugar builds up in the blood
          </div>
        </div>
      </div>
    </SlideShell>
  );
};

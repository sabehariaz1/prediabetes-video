import React from 'react';
import { useCurrentFrame, interpolate } from 'remotion';
import { PALETTE, SERIF } from '../theme';
import { SlideShell } from '../components/SlideShell';
import { PersonIcon } from '../components/Icons';

export const Scene1Hook: React.FC = () => {
  const frame = useCurrentFrame();

  const highlightPeople = frame >= 75;
  const showQuestions = frame >= 180;
  const showNoSymptoms = frame >= 280;

  let caption =
    'Imagine a common health condition affecting more than 1 in 3 adults worldwide.';
  if (frame >= 180 && frame < 280) {
    caption = 'And about 8 in 10 people who have it do not even know it.';
  } else if (frame >= 280) {
    caption =
      "It's called prediabetes, and it usually causes no warning signs at all.";
  }

  const highlightedIndices = new Set([2, 4, 6, 8, 11, 13, 17, 20, 23]);
  const questionIndices = new Set([2, 4, 6, 8, 11, 13, 17]);

  return (
    <SlideShell title="Prediabetes: Are You at Risk?" caption={caption}>
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          gap: 130,
          width: '100%',
        }}
      >
        {/* 5x5 Global Population Grid */}
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(5, 1fr)',
            gap: '20px 26px',
            padding: 24,
          }}
        >
          {Array.from({ length: 25 }).map((_, idx) => {
            const delay = idx * 1.5;
            const opacity = interpolate(frame, [delay, delay + 12], [0, 1], {
              extrapolateLeft: 'clamp',
              extrapolateRight: 'clamp',
            });
            const isAffected = highlightPeople && highlightedIndices.has(idx);
            const hasQ = showQuestions && questionIndices.has(idx);

            return (
              <div key={idx} style={{ opacity, transform: 'scale(1.15)' }}>
                <PersonIcon
                  color={isAffected ? PALETTE.coral : PALETTE.navy}
                  showQuestion={hasQ}
                />
              </div>
            );
          })}
        </div>

        {/* Global Community Stats */}
        <div style={{ maxWidth: 640 }}>
          <div
            style={{
              opacity: interpolate(frame, [65, 85], [0, 1], {
                extrapolateLeft: 'clamp',
                extrapolateRight: 'clamp',
              }),
              transform: `translateY(${interpolate(frame, [65, 85], [20, 0], {
                extrapolateLeft: 'clamp',
                extrapolateRight: 'clamp',
              })}px)`,
            }}
          >
            <div
              style={{
                fontFamily: SERIF,
                fontSize: 104,
                fontWeight: 700,
                color: PALETTE.coral,
                lineHeight: 1,
              }}
            >
              More than 1 in 3
            </div>
            <div
              style={{
                fontFamily: SERIF,
                fontSize: 42,
                fontWeight: 700,
                color: PALETTE.navy,
                marginTop: 10,
              }}
            >
              adults worldwide have prediabetes
            </div>
          </div>

          <div
            style={{
              marginTop: 34,
              opacity: interpolate(frame, [175, 195], [0, 1], {
                extrapolateLeft: 'clamp',
                extrapolateRight: 'clamp',
              }),
            }}
          >
            <div
              style={{
                fontFamily: SERIF,
                fontSize: 42,
                fontWeight: 700,
                color: PALETTE.amber,
              }}
            >
              8 in 10 don’t know it
            </div>
          </div>

          {showNoSymptoms && (
            <div
              style={{
                marginTop: 22,
                opacity: interpolate(frame, [280, 300], [0, 1], {
                  extrapolateLeft: 'clamp',
                  extrapolateRight: 'clamp',
                }),
              }}
            >
              <div
                style={{
                  fontFamily: SERIF,
                  fontSize: 40,
                  fontWeight: 700,
                  color: PALETTE.teal,
                }}
              >
                Usually has no symptoms
              </div>
            </div>
          )}
        </div>
      </div>
    </SlideShell>
  );
};

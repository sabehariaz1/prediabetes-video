import React from 'react';
import { AbsoluteFill, useCurrentFrame, interpolate } from 'remotion';
import { PALETTE, SERIF, SANS } from '../theme';

export const SlideShell: React.FC<{
  title: string;
  subtitleBadge?: { text: string; bg: string; color?: string };
  caption: string;
  children: React.ReactNode;
}> = ({ title, subtitleBadge, caption, children }) => {
  const frame = useCurrentFrame();
  const fadeIn = interpolate(frame, [0, 12], [0, 1], { extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: PALETTE.bg,
        fontFamily: SANS,
        opacity: fadeIn,
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'space-between',
        padding: '44px 76px 34px 76px',
        overflow: 'hidden',
      }}
    >
      {/* Subtle Medical Background Watermarks */}
      <svg
        width="1920"
        height="1080"
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          pointerEvents: 'none',
          opacity: 0.35,
        }}
      >
        <circle cx="80" cy="80" r="190" fill="none" stroke="#BFDBFE" strokeWidth="24" />
        <circle cx="1850" cy="960" r="240" fill="none" stroke="#BFDBFE" strokeWidth="28" />
        <path
          d="M 1760 150 h 30 M 1775 135 v 30"
          stroke="#93C5FD"
          strokeWidth="6"
          strokeLinecap="round"
        />
        <path
          d="M 140 840 h 30 M 155 825 v 30"
          stroke="#93C5FD"
          strokeWidth="6"
          strokeLinecap="round"
        />
      </svg>

      {/* Top Slide Header */}
      <div style={{ textAlign: 'center', zIndex: 2 }}>
        <h1
          style={{
            fontFamily: SERIF,
            fontSize: 62,
            fontWeight: 700,
            color: PALETTE.navy,
            margin: 0,
            lineHeight: 1.15,
          }}
        >
          {title}
        </h1>
        {subtitleBadge && (
          <div style={{ marginTop: 12 }}>
            <span
              style={{
                display: 'inline-block',
                backgroundColor: subtitleBadge.bg,
                color: subtitleBadge.color || PALETTE.white,
                fontSize: 21,
                fontWeight: 800,
                letterSpacing: 1.6,
                textTransform: 'uppercase',
                padding: '7px 26px',
                borderRadius: 999,
              }}
            >
              {subtitleBadge.text}
            </span>
          </div>
        )}
      </div>

      {/* Center Content Area */}
      <div
        style={{
          flex: 1,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          width: '100%',
          zIndex: 2,
          margin: '14px 0',
        }}
      >
        {children}
      </div>

      {/* Single Clean Bottom Caption Bar (Zero Overlap / Clipping) */}
      <div style={{ display: 'flex', justifyContent: 'center', zIndex: 2 }}>
        <div
          style={{
            backgroundColor: PALETTE.captionBg,
            border: `2px solid ${PALETTE.border}`,
            borderRadius: 18,
            padding: '13px 34px',
            maxWidth: 1480,
            boxShadow: '0 6px 20px rgba(15, 43, 70, 0.06)',
            textAlign: 'center',
          }}
        >
          <span
            style={{
              fontFamily: SERIF,
              fontSize: 28,
              color: PALETTE.navy,
              lineHeight: 1.35,
            }}
          >
            {caption}
          </span>
        </div>
      </div>
    </AbsoluteFill>
  );
};

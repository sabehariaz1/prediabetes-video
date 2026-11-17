import React from 'react';
import { PALETTE } from '../theme';

export const PersonIcon: React.FC<{ color: string; showQuestion?: boolean }> = ({
  color,
  showQuestion = false,
}) => (
  <div
    style={{
      position: 'relative',
      width: 42,
      height: 74,
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
    }}
  >
    {showQuestion && (
      <div
        style={{
          position: 'absolute',
          top: -16,
          width: 24,
          height: 24,
          borderRadius: '50%',
          backgroundColor: '#F59E0B',
          color: '#FFFFFF',
          fontSize: 16,
          fontWeight: 800,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          boxShadow: '0 2px 6px rgba(0,0,0,0.15)',
        }}
      >
        ?
      </div>
    )}
    <svg width="38" height="68" viewBox="0 0 38 68">
      <circle cx="19" cy="14" r="10" fill={color} />
      <rect x="6" y="27" width="26" height="36" rx="11" fill={color} />
    </svg>
  </div>
);

export const BloodDropIcon: React.FC<{ width?: number; height?: number }> = ({
  width = 64,
  height = 82,
}) => (
  <svg width={width} height={height} viewBox="0 0 90 120">
    <path
      d="M45 8 C45 8 10 55 10 80 C10 100 26 114 45 114 C64 114 80 100 80 80 C80 55 45 8 45 8 Z"
      fill={PALETTE.coral}
    />
    <path
      d="M32 75 C32 86 38 94 46 96"
      fill="none"
      stroke="#FFFFFF"
      strokeWidth="5"
      strokeLinecap="round"
      opacity="0.7"
    />
  </svg>
);

export const GlucoseMeterIcon: React.FC = () => (
  <svg width="64" height="82" viewBox="0 0 70 105">
    <rect x="14" y="4" width="42" height="66" rx="10" fill={PALETTE.blue} />
    <rect x="21" y="12" width="28" height="20" rx="4" fill="#93C5FD" />
    <text
      x="35"
      y="27"
      textAnchor="middle"
      fill={PALETTE.navy}
      fontSize="13"
      fontWeight="800"
    >
      110
    </text>
    <circle cx="28" cy="50" r="4" fill="#FFFFFF" />
    <circle cx="42" cy="50" r="4" fill="#FFFFFF" />
    <rect x="31" y="70" width="8" height="12" fill="#CBD5E1" />
    <path
      d="M35 82 C35 82 28 90 28 95 C28 99 31 101 35 101 C39 101 42 99 42 95 C42 90 35 82 35 82 Z"
      fill={PALETTE.coral}
    />
  </svg>
);

export const GlucoseDrinkIcon: React.FC = () => (
  <svg width="64" height="82" viewBox="0 0 76 100">
    <polygon
      points="14,12 62,12 54,90 22,90"
      fill="none"
      stroke={PALETTE.navy}
      strokeWidth="4"
    />
    <polygon points="18,36 58,36 54,88 22,88" fill="#F59E0B" opacity="0.85" />
  </svg>
);

export const HeartIcon: React.FC = () => (
  <svg width="72" height="66" viewBox="0 0 72 66" style={{ marginBottom: 12 }}>
    <path
      d="M36 60 C36 60 6 40 6 20 C6 10 14 4 23 4 C29 4 34 8 36 13 C38 8 43 4 49 4 C58 4 66 10 66 20 C66 40 36 60 36 60 Z"
      fill={PALETTE.teal}
    />
  </svg>
);

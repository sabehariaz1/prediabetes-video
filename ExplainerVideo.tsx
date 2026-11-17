import React from 'react';
import {
  AbsoluteFill,
  Audio,
  Composition,
  Easing,
  Sequence,
  interpolate,
  interpolateColors,
  spring,
  staticFile,
  useCurrentFrame,
} from 'remotion';

/* -------------------------------------------------------------------------- */
/*  Global settings                                                           */
/* -------------------------------------------------------------------------- */

const FPS = 30;
const WIDTH = 1920;
const HEIGHT = 1080;

// Scene lengths in frames. They add up to exactly 3,600 frames = 2:00 at 30 fps.
const D = {
  intro: 360, // 12 s
  gauge: 420, // 14 s
  body: 480, // 16 s
  risks: 900, // 30 s
  tests: 600, // 20 s
  good: 420, // 14 s
  close: 420, // 14 s
} as const;

const TOTAL_FRAMES = D.intro + D.gauge + D.body + D.risks + D.tests + D.good + D.close; // 3600

const C = {
  bg: '#E8F4FD',
  navy: '#1B3A6B',
  teal: '#2EC4B6',
  red: '#FF4D5E',
  orange: '#FF9F1C',
  blue: '#3B82F6',
  line: '#D3E3F3',
  gray: '#5F7391',
  white: '#FFFFFF',
  pale: '#C8DFF5',
};

const SERIF = "'DejaVu Serif', Georgia, 'Times New Roman', serif";

/* -------------------------------------------------------------------------- */
/*  Animation helpers                                                         */
/* -------------------------------------------------------------------------- */

const CLAMP = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const SMOOTH = Easing.bezier(0.22, 1, 0.36, 1);

/** Eased 0 -> 1 progress between `start` and `start + dur`. */
const prog = (f: number, start: number, dur: number): number =>
  interpolate(f, [start, start + dur], [0, 1], {...CLAMP, easing: SMOOTH});

/** Gentle springy pop-in, 0 before `start`. */
const pop = (f: number, start: number): number =>
  f < start
    ? 0
    : spring({
        frame: f - start,
        fps: FPS,
        config: {damping: 15, stiffness: 150, mass: 0.7},
      });

const lerp = (a: number, b: number, t: number): number => a + (b - a) * t;

const fadeUp = (p: number): React.CSSProperties => ({
  opacity: Math.min(1, p),
  transform: `translateY(${(1 - Math.min(1, p)) * 22}px)`,
});

const polar = (cx: number, cy: number, r: number, deg: number) => ({
  x: cx + r * Math.cos((deg * Math.PI) / 180),
  y: cy - r * Math.sin((deg * Math.PI) / 180),
});

const arcPath = (cx: number, cy: number, r: number, a1: number, a2: number): string => {
  const p1 = polar(cx, cy, r, a1);
  const p2 = polar(cx, cy, r, a2);
  return `M ${p1.x} ${p1.y} A ${r} ${r} 0 0 1 ${p2.x} ${p2.y}`;
};

/* -------------------------------------------------------------------------- */
/*  Shared pieces: background, progress bar, title, caption, scene fade       */
/* -------------------------------------------------------------------------- */

const Background: React.FC = () => {
  const f = useCurrentFrame();
  const pluses: Array<[number, number]> = [
    [150, 250],
    [270, 560],
    [1790, 200],
    [1500, 830],
    [640, 900],
    [1600, 520],
    [90, 790],
    [1010, 985],
    [880, 200],
  ];
  return (
    <AbsoluteFill style={{backgroundColor: C.bg}}>
      <svg width={WIDTH} height={HEIGHT} style={{position: 'absolute', left: 0, top: 0}}>
        <circle cx={0} cy={90} r={190} fill="none" stroke="#D5E4F6" strokeWidth={34} />
        <circle cx={1900} cy={70} r={120} fill="none" stroke="#D5E4F6" strokeWidth={26} />
        <circle cx={1850} cy={930} r={250} fill="none" stroke="#D5E4F6" strokeWidth={34} />
        {pluses.map(([x, y], i) => {
          const dy = Math.sin(f / 40 + i) * 6;
          return (
            <path
              key={i}
              d={`M ${x - 15} ${y + dy} h 30 M ${x} ${y - 15 + dy} v 30`}
              stroke="#D5E4F6"
              strokeWidth={6}
              strokeLinecap="round"
            />
          );
        })}
      </svg>
    </AbsoluteFill>
  );
};

const ProgressBar: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <div
      style={{
        position: 'absolute',
        left: 0,
        right: 0,
        bottom: 0,
        height: 10,
        backgroundColor: '#C9DCF0',
      }}
    >
      <div
        style={{
          width: `${(f / TOTAL_FRAMES) * 100}%`,
          height: '100%',
          backgroundColor: C.teal,
        }}
      />
    </div>
  );
};

const SceneFade: React.FC<{duration: number; children: React.ReactNode}> = ({
  duration,
  children,
}) => {
  const f = useCurrentFrame();
  const o = Math.min(
    interpolate(f, [0, 14], [0, 1], CLAMP),
    interpolate(f, [duration - 14, duration], [1, 0], CLAMP),
  );
  return <AbsoluteFill style={{opacity: o}}>{children}</AbsoluteFill>;
};

const Title: React.FC<{text: string; color?: string}> = ({text, color = C.navy}) => {
  const f = useCurrentFrame();
  const p = prog(f, 0, 24);
  return (
    <div
      style={{
        position: 'absolute',
        top: 34,
        left: 0,
        right: 0,
        textAlign: 'center',
        fontFamily: SERIF,
        fontWeight: 700,
        fontSize: 64,
        color,
        opacity: p,
        transform: `translateY(${(1 - p) * -18}px)`,
      }}
    >
      {text}
    </div>
  );
};

type CapItem = {from: number; text: string};

const CAPTION_STYLE: React.CSSProperties = {
  backgroundColor: C.white,
  border: `2px solid ${C.line}`,
  borderRadius: 20,
  padding: '14px 38px',
  fontFamily: SERIF,
  fontSize: 34,
  lineHeight: 1.25,
  color: C.navy,
  textAlign: 'center',
  maxWidth: 1560,
  boxShadow: '0 4px 14px rgba(27,58,107,0.08)',
};

/** One single centered caption pill. Cross-fades between lines. */
const Caption: React.FC<{items: CapItem[]}> = ({items}) => {
  const f = useCurrentFrame();
  let idx = -1;
  items.forEach((it, i) => {
    if (f >= it.from) idx = i;
  });
  if (idx < 0) return null;
  const t = f - items[idx].from;
  const cur = interpolate(t, [0, 10], [0, 1], CLAMP);
  const wrap = (text: string, opacity: number, dy: number) => (
    <div
      style={{
        position: 'absolute',
        left: 0,
        right: 0,
        bottom: 44,
        display: 'flex',
        justifyContent: 'center',
        opacity,
        transform: `translateY(${dy}px)`,
      }}
    >
      <div style={CAPTION_STYLE}>{text}</div>
    </div>
  );
  return (
    <>
      {idx > 0 && wrap(items[idx - 1].text, 1 - cur, 0)}
      {wrap(items[idx].text, cur, (1 - cur) * 8)}
    </>
  );
};

/* -------------------------------------------------------------------------- */
/*  Icons                                                                     */
/* -------------------------------------------------------------------------- */

const Person: React.FC<{x: number; y: number; color: string; s?: number}> = ({
  x,
  y,
  color,
  s = 1,
}) => (
  <g transform={`translate(${x} ${y}) scale(${s})`}>
    <circle cx={0} cy={-38} r={15} fill={color} />
    <rect x={-24} y={-16} width={48} height={66} rx={20} fill={color} />
    <rect x={-2.5} y={30} width={5} height={22} fill={C.bg} />
  </g>
);

const Svg: React.FC<{size?: number; children: React.ReactNode}> = ({size = 72, children}) => (
  <svg viewBox="0 0 64 64" width={size} height={size}>
    {children}
  </svg>
);

const IconAge: React.FC<{size?: number}> = ({size}) => (
  <Svg size={size}>
    <circle cx={32} cy={32} r={27} fill="#fff" stroke={C.navy} strokeWidth={3.5} />
    <text
      x={32}
      y={40}
      textAnchor="middle"
      fontFamily={SERIF}
      fontWeight={700}
      fontSize={22}
      fill={C.navy}
    >
      35+
    </text>
  </Svg>
);

const IconFamily: React.FC<{size?: number}> = ({size}) => (
  <Svg size={size}>
    <circle cx={16} cy={12} r={6} fill={C.navy} />
    <rect x={9} y={20} width={14} height={18} rx={6} fill={C.navy} />
    <circle cx={48} cy={12} r={6} fill={C.red} />
    <rect x={41} y={20} width={14} height={18} rx={6} fill={C.red} />
    <path d="M16 40 L32 50 M48 40 L32 50" stroke={C.navy} strokeWidth={3} fill="none" />
    <circle cx={32} cy={50} r={5} fill={C.navy} />
    <rect x={26} y={55} width={12} height={8} rx={4} fill={C.navy} />
  </Svg>
);

const IconGlobe: React.FC<{size?: number}> = ({size}) => (
  <Svg size={size}>
    <circle cx={32} cy={32} r={26} fill="#fff" stroke={C.navy} strokeWidth={3} />
    <ellipse cx={32} cy={32} rx={11} ry={26} fill="none" stroke={C.navy} strokeWidth={2.5} />
    <path d="M6 32 H58" stroke={C.navy} strokeWidth={2.5} />
    <path d="M10 18 Q32 26 54 18 M10 46 Q32 38 54 46" stroke={C.navy} strokeWidth={2.5} fill="none" />
  </Svg>
);

const IconWeight: React.FC<{size?: number}> = ({size}) => (
  <Svg size={size}>
    <rect x={7} y={9} width={50} height={46} rx={11} fill="#fff" stroke={C.navy} strokeWidth={3.5} />
    <path d="M18 36 A14 14 0 0 1 46 36" stroke={C.navy} strokeWidth={3} fill="none" />
    <line x1={32} y1={36} x2={40} y2={25} stroke={C.red} strokeWidth={3.5} strokeLinecap="round" />
    <circle cx={32} cy={36} r={3.5} fill={C.navy} />
  </Svg>
);

const IconCouch: React.FC<{size?: number}> = ({size}) => (
  <Svg size={size}>
    <rect x={15} y={14} width={34} height={20} rx={7} fill={C.pale} stroke={C.navy} strokeWidth={3} />
    <circle cx={32} cy={24} r={4} fill={C.navy} />
    <rect x={5} y={26} width={12} height={26} rx={6} fill={C.pale} stroke={C.navy} strokeWidth={3} />
    <rect x={47} y={26} width={12} height={26} rx={6} fill={C.pale} stroke={C.navy} strokeWidth={3} />
    <rect x={12} y={36} width={40} height={16} rx={5} fill={C.pale} stroke={C.navy} strokeWidth={3} />
    <path d="M14 52 v6 M50 52 v6" stroke={C.navy} strokeWidth={3} strokeLinecap="round" />
  </Svg>
);

const IconCup: React.FC<{size?: number}> = ({size}) => (
  <Svg size={size}>
    <path d="M17 22 L21 58 H43 L47 22 Z" fill={C.red} stroke={C.navy} strokeWidth={2.5} />
    <rect x={13} y={16} width={38} height={8} rx={3} fill={C.navy} />
    <path d="M36 16 L43 5" stroke={C.navy} strokeWidth={3} strokeLinecap="round" />
    <rect x={25} y={34} width={6} height={9} rx={2} fill="#fff" />
    <rect x={34} y={38} width={6} height={9} rx={2} fill="#fff" />
  </Svg>
);

const IconSmoke: React.FC<{size?: number}> = ({size}) => (
  <Svg size={size}>
    <rect x={5} y={40} width={15} height={11} fill={C.orange} stroke={C.navy} strokeWidth={2} />
    <rect x={20} y={40} width={34} height={11} fill="#fff" stroke={C.navy} strokeWidth={2} />
    <rect x={54} y={40} width={5} height={11} fill={C.red} />
    <path d="M46 35 C41 28 52 24 47 16 C45 12 49 8 49 6" stroke={C.gray} strokeWidth={3} fill="none" strokeLinecap="round" />
  </Svg>
);

const IconMoon: React.FC<{size?: number}> = ({size}) => (
  <Svg size={size}>
    <path d="M38 6 A26 26 0 1 0 58 42 A21 21 0 1 1 38 6 Z" fill={C.navy} />
    <circle cx={50} cy={14} r={3.5} fill={C.orange} />
    <circle cx={57} cy={26} r={2.5} fill={C.orange} />
  </Svg>
);

const IconBP: React.FC<{size?: number}> = ({size}) => (
  <Svg size={size}>
    <circle cx={32} cy={32} r={25} fill="#fff" stroke={C.navy} strokeWidth={3.5} />
    <path d="M14 38 A18 18 0 0 1 50 38" stroke={C.navy} strokeWidth={2.5} fill="none" strokeDasharray="2 5" />
    <line x1={32} y1={34} x2={44} y2={21} stroke={C.red} strokeWidth={3.5} strokeLinecap="round" />
    <circle cx={32} cy={34} r={4} fill={C.navy} />
  </Svg>
);

const IconCholesterol: React.FC<{size?: number}> = ({size}) => (
  <Svg size={size}>
    <rect x={5} y={20} width={54} height={24} rx={12} fill="#FDE3E6" stroke={C.navy} strokeWidth={3} />
    {[17, 27, 37, 47].map((x) => (
      <circle key={x} cx={x} cy={32} r={4.2} fill={C.orange} />
    ))}
  </Svg>
);

const IconVenus: React.FC<{size?: number}> = ({size}) => (
  <Svg size={size}>
    <circle cx={32} cy={23} r={14} fill="none" stroke={C.navy} strokeWidth={4} />
    <path d="M32 37 V59 M21 48 H43" stroke={C.navy} strokeWidth={4} strokeLinecap="round" />
  </Svg>
);

const IconPregnancy: React.FC<{size?: number}> = ({size}) => (
  <Svg size={size}>
    <circle cx={26} cy={11} r={8} fill={C.navy} />
    <rect x={14} y={22} width={24} height={38} rx={11} fill={C.navy} />
    <circle cx={39} cy={38} r={12} fill={C.orange} />
  </Svg>
);

const IconDrop: React.FC<{size?: number}> = ({size}) => (
  <Svg size={size}>
    <path d="M32 5 C38 19 51 29 51 42 A19 19 0 0 1 13 42 C13 29 26 19 32 5 Z" fill={C.red} />
    <path d="M22 44 A10 10 0 0 0 30 53" stroke="#fff" strokeWidth={3} fill="none" strokeLinecap="round" opacity={0.7} />
  </Svg>
);

const IconMeter: React.FC<{size?: number}> = ({size}) => (
  <Svg size={size}>
    <rect x={18} y={4} width={28} height={44} rx={5} fill={C.blue} />
    <rect x={22} y={9} width={20} height={12} rx={2} fill={C.navy} />
    <text x={32} y={19} textAnchor="middle" fontFamily={SERIF} fontWeight={700} fontSize={9} fill="#fff">
      120
    </text>
    <circle cx={26} cy={29} r={2.4} fill="#fff" />
    <circle cx={38} cy={29} r={2.4} fill="#fff" />
    <rect x={29} y={48} width={6} height={8} fill="#B8C4D4" />
    <path d="M32 55 C34 59 36 60 36 62 A4 4 0 0 1 28 62 C28 60 30 59 32 55 Z" fill={C.red} />
  </Svg>
);

const IconGlass: React.FC<{size?: number}> = ({size}) => (
  <Svg size={size}>
    <path d="M12 8 H52 L47 58 H17 Z" fill="#D8ECFB" stroke={C.navy} strokeWidth={3} />
    <path d="M14 30 H50 L47 58 H17 Z" fill={C.orange} />
    <rect x={12} y={8} width={40} height={6} fill="#fff" opacity={0.5} />
  </Svg>
);

const IconHeart: React.FC<{size?: number; color?: string}> = ({size = 90, color = C.teal}) => (
  <Svg size={size}>
    <path
      d="M32 57 C8 41 4 22 16 14 C24 9 30 14 32 20 C34 14 40 9 48 14 C60 22 56 41 32 57 Z"
      fill={color}
    />
  </Svg>
);

const IconRunner: React.FC<{size?: number}> = ({size}) => (
  <Svg size={size}>
    <circle cx={38} cy={10} r={6} fill={C.teal} />
    <path
      d="M36 18 L28 32 L18 34 M28 32 L36 40 L32 56 M36 20 L46 28 L54 26 M28 32 L22 46 L10 50"
      stroke={C.teal}
      strokeWidth={5}
      fill="none"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
  </Svg>
);

const IconApple: React.FC<{size?: number}> = ({size}) => (
  <Svg size={size}>
    <circle cx={25} cy={38} r={16} fill={C.red} />
    <circle cx={39} cy={38} r={16} fill={C.red} />
    <path d="M32 24 C32 16 36 11 42 9" stroke={C.navy} strokeWidth={3} fill="none" strokeLinecap="round" />
    <path d="M40 12 C46 8 52 12 52 17 C46 18 41 16 40 12 Z" fill={C.teal} />
  </Svg>
);

const CheckCircle: React.FC<{size?: number}> = ({size = 52}) => (
  <svg viewBox="0 0 64 64" width={size} height={size}>
    <circle cx={32} cy={32} r={30} fill={C.teal} />
    <path d="M18 33 L28 43 L47 22" stroke="#fff" strokeWidth={7} fill="none" strokeLinecap="round" strokeLinejoin="round" />
  </svg>
);

/* -------------------------------------------------------------------------- */
/*  Scene 1: Intro  (12 s)                                                    */
/* -------------------------------------------------------------------------- */

const IntroScene: React.FC = () => {
  const f = useCurrentFrame();
  const flagged = [7, 16];
  const cols = 5;

  return (
    <AbsoluteFill>
      <Title text="Prediabetes: Are You at Risk?" />
      <svg width={WIDTH} height={HEIGHT} style={{position: 'absolute', left: 0, top: 0}}>
        {Array.from({length: 20}, (_, i) => {
          const c = i % cols;
          const r = Math.floor(i / cols);
          const x = 330 + c * 125;
          const y = 300 + r * 150;
          const p = pop(f, 22 + i * 4);
          const isFlag = flagged.includes(i);
          const hl = isFlag ? prog(f, 135, 24) : 0;
          const color = interpolateColors(hl, [0, 1], [C.navy, C.red]);
          const badge = isFlag ? pop(f, 170 + (i === 7 ? 0 : 14)) : 0;
          return (
            <g key={i}>
              <Person x={x} y={y} color={color} s={Math.max(0, p) * (1 + hl * 0.08)} />
              {isFlag && badge > 0 && (
                <g transform={`translate(${x + 26} ${y - 54}) scale(${badge})`}>
                  <circle r={17} fill={C.orange} stroke="#fff" strokeWidth={3} />
                  <text
                    y={7}
                    textAnchor="middle"
                    fontFamily={SERIF}
                    fontWeight={700}
                    fontSize={22}
                    fill="#fff"
                  >
                    ?
                  </text>
                </g>
              )}
            </g>
          );
        })}
      </svg>

      <div style={{position: 'absolute', left: 1000, top: 200, width: 860, fontFamily: SERIF}}>
        <div
          style={{
            fontSize: 180,
            fontWeight: 700,
            lineHeight: 1,
            whiteSpace: 'nowrap',
            color: C.red,
            opacity: prog(f, 150, 24),
            transform: `scale(${0.88 + 0.12 * prog(f, 150, 24)})`,
            transformOrigin: 'left center',
          }}
        >
          1 in 10
        </div>
        <div
          style={{
            fontSize: 56,
            fontWeight: 700,
            lineHeight: 1.15,
            color: C.navy,
            marginTop: 8,
            ...fadeUp(prog(f, 190, 24)),
          }}
        >
          adults worldwide have prediabetes
        </div>
        <div style={{fontSize: 38, color: C.gray, marginTop: 14, ...fadeUp(prog(f, 215, 24))}}>
          That’s over 500 million people
        </div>
        <div
          style={{
            fontSize: 48,
            fontWeight: 700,
            color: C.orange,
            marginTop: 22,
            ...fadeUp(prog(f, 245, 24)),
          }}
        >
          Most don’t know they have it
        </div>
        <div
          style={{
            fontSize: 48,
            fontWeight: 700,
            color: C.teal,
            marginTop: 12,
            ...fadeUp(prog(f, 290, 24)),
          }}
        >
          Often no symptoms
        </div>
      </div>

      <Caption
        items={[
          {from: 0, text: 'Imagine a condition that affects hundreds of millions of adults around the world.'},
          {from: 125, text: 'About 1 in 10 adults worldwide has prediabetes, and most don’t know it.'},
          {from: 255, text: 'It’s called prediabetes, and it often causes no symptoms at all.'},
        ]}
      />
    </AbsoluteFill>
  );
};

/* -------------------------------------------------------------------------- */
/*  Scene 2: What is prediabetes? HbA1C gauge  (14 s)                         */
/* -------------------------------------------------------------------------- */

const GaugeScene: React.FC = () => {
  const f = useCurrentFrame();
  const cx = 1010;
  const cy = 610;
  const R = 330;

  const segs = [
    {a1: 180, a2: 128, color: C.teal, start: 20},
    {a1: 124, a2: 56, color: C.orange, start: 42},
    {a1: 52, a2: 0, color: C.red, start: 64},
  ];

  const needleAngle = interpolate(
    f,
    [110, 140, 200, 240, 290, 330],
    [180, 154, 154, 90, 90, 28],
    {...CLAMP, easing: Easing.inOut(Easing.cubic)},
  );
  const tip = polar(cx, cy, 265, needleAngle);
  const needleOpacity = prog(f, 100, 12);

  const labelOpacity = prog(f, 75, 24);
  const legend = [
    {color: C.teal, text: 'Below 5.7%', x: 500, start: 145},
    {color: C.orange, text: '5.7% – 6.4%', x: 860, start: 225},
    {color: C.red, text: '6.5% or higher', x: 1260, start: 315},
  ];

  return (
    <AbsoluteFill>
      <Title text="What Is Prediabetes?" />
      <svg width={WIDTH} height={HEIGHT} style={{position: 'absolute', left: 0, top: 0}}>
        {segs.map((s, i) => (
          <path
            key={i}
            d={arcPath(cx, cy, R, s.a1, s.a2)}
            pathLength={1}
            stroke={s.color}
            strokeWidth={56}
            fill="none"
            strokeDasharray={1}
            strokeDashoffset={1 - prog(f, s.start, 32)}
          />
        ))}

        <g opacity={labelOpacity} fontFamily={SERIF} fontWeight={700} fontSize={38} fill={C.navy}>
          <text x={cx - R - 80} y={cy - 150} textAnchor="end">
            Normal
          </text>
          <text x={cx} y={cy - R - 62} textAnchor="middle">
            Prediabetes
          </text>
          <text x={cx + R + 80} y={cy - 150} textAnchor="start">
            Diabetes
          </text>
        </g>

        <g opacity={needleOpacity}>
          <line
            x1={cx}
            y1={cy}
            x2={tip.x}
            y2={tip.y}
            stroke={C.navy}
            strokeWidth={9}
            strokeLinecap="round"
          />
          <circle cx={cx} cy={cy} r={21} fill="#3A5A8C" />
        </g>

        <text
          x={cx}
          y={cy + 100}
          textAnchor="middle"
          fontFamily={SERIF}
          fontWeight={700}
          fontSize={44}
          fill={C.navy}
          letterSpacing={1}
          opacity={labelOpacity}
        >
          BLOOD SUGAR (HbA1C)
        </text>

        <g opacity={prog(f, 88, 24)} transform="translate(250 600)">
          <g transform="translate(-55 -80) scale(1.7)">
            <IconDrop size={64} />
          </g>
          <text
            x={0}
            y={110}
            textAnchor="middle"
            fontFamily={SERIF}
            fontWeight={700}
            fontSize={32}
            fill={C.navy}
          >
            HbA1C blood test
          </text>
        </g>

        {legend.map((l, i) => {
          const p = prog(f, l.start, 20);
          return (
            <g key={i} opacity={p} transform={`translate(${l.x} ${790 + (1 - p) * 14})`}>
              <circle cx={0} cy={-10} r={13} fill={l.color} />
              <text
                x={26}
                y={0}
                fontFamily={SERIF}
                fontWeight={700}
                fontSize={34}
                fill={C.navy}
              >
                {l.text}
              </text>
            </g>
          );
        })}
      </svg>
      <Caption
        items={[
          {
            from: 0,
            text: 'Prediabetes means your blood sugar is higher than normal, but not yet high enough to be called diabetes.',
          },
          {from: 125, text: 'A common blood test, the HbA1C, shows where you stand.'},
          {from: 205, text: '5.7% to 6.4% is prediabetes.'},
          {from: 295, text: 'And 6.5% or higher is diabetes.'},
        ]}
      />
    </AbsoluteFill>
  );
};

/* -------------------------------------------------------------------------- */
/*  Scene 3: What goes wrong inside the body (insulin key + cell lock)        */
/* -------------------------------------------------------------------------- */

const Lock: React.FC<{x: number; y: number; color: string; open: number}> = ({x, y, color, open}) => (
  <g transform={`translate(${x} ${y}) scale(1.5)`}>
    <g transform={`translate(0 ${-open * 9}) rotate(${-open * 22} 10 -12)`}>
      <path d="M -10 -4 V -14 a 10 10 0 0 1 20 0 V -4" fill="none" stroke={color} strokeWidth={6} strokeLinecap="round" />
    </g>
    <rect x={-20} y={-6} width={40} height={34} rx={8} fill={color} stroke="#fff" strokeWidth={3} />
    <circle cx={0} cy={9} r={4.5} fill="#fff" />
    <rect x={-2} y={10} width={4} height={10} rx={2} fill="#fff" />
  </g>
);

const Key: React.FC<{x: number; y: number; rot: number; fill: string; opacity: number}> = ({
  x,
  y,
  rot,
  fill,
  opacity,
}) => (
  <g transform={`translate(${x} ${y}) rotate(${rot})`} opacity={opacity}>
    <rect x={-65} y={-23} width={130} height={46} rx={23} fill={fill} />
    <text
      x={0}
      y={9}
      textAnchor="middle"
      fontFamily={SERIF}
      fontWeight={700}
      fontSize={26}
      fill="#fff"
    >
      insulin
    </text>
  </g>
);

const BodyScene: React.FC = () => {
  const f = useCurrentFrame();
  const OFF = 940;
  const doorY = 525;
  const cellX = 520;

  const panelIn = prog(f, 10, 24);

  /* healthy panel */
  const healthyKeyT = prog(f, 90, 40);
  const healthyOpen = prog(f, 132, 18);
  const healthyLockColor = interpolateColors(healthyOpen, [0, 1], ['#9FB3CC', C.teal]);
  const targets: Array<[number, number]> = [
    [610, 470],
    [700, 455],
    [770, 505],
    [650, 545],
    [740, 555],
  ];

  /* resistant panel */
  const resKeyT = prog(f, 215, 40);
  const resReject = prog(f, 266, 26);
  const resLockColor = interpolateColors(prog(f, 262, 14), [0, 1], ['#9FB3CC', C.red]);
  const xPop = pop(f, 266);

  const dotPos = (i: number, off: number, healthy: boolean) => {
    const sx = 250 + off;
    const sy = 450 + i * 40;
    if (healthy) {
      const t = prog(f, 150 + i * 14, 62);
      const door = {x: cellX + off, y: doorY};
      const [tx, ty] = targets[i];
      if (t < 0.45) {
        const k = t / 0.45;
        return {x: lerp(sx, door.x - 12, k), y: lerp(sy, door.y, k)};
      }
      const k = (t - 0.45) / 0.55;
      const settle = prog(f, 150 + i * 14 + 62, 10);
      return {
        x: lerp(door.x - 12, tx, k) + Math.sin((f + i * 9) / 11) * 4 * settle,
        y: lerp(door.y, ty, k) + Math.cos((f + i * 7) / 12) * 4 * settle,
      };
    }
    const start = 275 + i * 10;
    const t = prog(f, start, 55);
    const stop = {x: cellX + off - 25, y: doorY + (i - 2) * 16};
    const rest = {x: 1330 + (i % 3) * 40, y: 440 + i * 44};
    const wig = prog(f, start + 55, 15);
    if (t < 0.55) {
      const k = t / 0.55;
      return {x: lerp(sx, stop.x, k), y: lerp(sy, stop.y, k)};
    }
    const k = (t - 0.55) / 0.45;
    return {
      x: lerp(stop.x, rest.x, k) + Math.sin((f + i * 9) / 10) * 5 * wig,
      y: lerp(stop.y, rest.y, k) + Math.cos((f + i * 6) / 9) * 5 * wig,
    };
  };

  const arrowP = prog(f, 365, 55);

  return (
    <AbsoluteFill>
      <Title text="What Goes Wrong Inside the Body" />
      <svg width={WIDTH} height={HEIGHT} style={{position: 'absolute', left: 0, top: 0}}>
        <g opacity={panelIn}>
          {/* titles */}
          <text x={535} y={285} textAnchor="middle" fontFamily={SERIF} fontWeight={700} fontSize={52} fill={C.teal}>
            Healthy
          </text>
          <text x={1475} y={285} textAnchor="middle" fontFamily={SERIF} fontWeight={700} fontSize={48} fill={C.red}>
            Cells stop responding
          </text>

          {/* cells */}
          <rect
            x={cellX}
            y={410}
            width={300}
            height={230}
            rx={30}
            fill={interpolateColors(prog(f, 200, 60), [0, 1], ['#FFFFFF', '#DDF6F3'])}
            stroke={C.teal}
            strokeWidth={5}
          />
          <rect x={cellX + OFF} y={410} width={300} height={230} rx={30} fill="#fff" stroke={C.red} strokeWidth={5} />
          <text x={cellX + 150} y={622} textAnchor="middle" fontFamily={SERIF} fontWeight={700} fontSize={30} fill={C.navy}>
            Cell
          </text>
          <text x={cellX + OFF + 150} y={622} textAnchor="middle" fontFamily={SERIF} fontWeight={700} fontSize={30} fill={C.navy}>
            Cell
          </text>

          {/* sugar labels */}
          <text x={250} y={690} textAnchor="middle" fontFamily={SERIF} fontSize={26} fill={C.gray}>
            sugar
          </text>
          <text x={250 + OFF} y={690} textAnchor="middle" fontFamily={SERIF} fontSize={26} fill={C.gray}>
            sugar
          </text>
        </g>

        {/* locks */}
        <Lock x={cellX} y={doorY - 14} color={healthyLockColor} open={healthyOpen} />
        <Lock x={cellX + OFF} y={doorY - 14} color={resLockColor} open={0} />

        {/* keys */}
        <Key
          x={lerp(300, 440, healthyKeyT)}
          y={lerp(345, doorY, healthyKeyT)}
          rot={lerp(-28, 0, healthyKeyT)}
          fill={C.blue}
          opacity={prog(f, 70, 16)}
        />
        <Key
          x={lerp(1240, 1380, resKeyT) - 85 * resReject}
          y={lerp(345, doorY, resKeyT) + 34 * resReject}
          rot={lerp(-28, 0, resKeyT) + 20 * resReject}
          fill={interpolateColors(resReject, [0, 1], [C.blue, '#A9B7C9'])}
          opacity={prog(f, 195, 16) * (1 - 0.4 * resReject)}
        />

        {/* red X on the closed door */}
        <g transform={`translate(${cellX + OFF - 52} ${doorY - 6}) scale(${xPop})`}>
          <path d="M -22 -22 L 22 22 M 22 -22 L -22 22" stroke={C.red} strokeWidth={9} strokeLinecap="round" />
        </g>

        {/* sugar dots */}
        {[0, 1, 2, 3, 4].map((i) => {
          const a = dotPos(i, 0, true);
          const b = dotPos(i, OFF, false);
          const o = prog(f, 12 + i * 3, 18);
          return (
            <g key={i} opacity={o}>
              <circle cx={a.x} cy={a.y} r={15} fill={C.orange} />
              <circle cx={b.x} cy={b.y} r={15} fill={C.orange} />
            </g>
          );
        })}

        {/* rising blood sugar arrow */}
        <g opacity={arrowP}>
          <line x1={1105} y1={640} x2={1105} y2={640 - 220 * arrowP + 28} stroke={C.red} strokeWidth={9} strokeLinecap="round" />
          <polygon
            points={`1105,${640 - 220 * arrowP} 1083,${640 - 220 * arrowP + 38} 1127,${640 - 220 * arrowP + 38}`}
            fill={C.red}
          />
        </g>

        <text
          x={535}
          y={745}
          textAnchor="middle"
          fontFamily={SERIF}
          fontWeight={700}
          fontSize={36}
          fill={C.teal}
          opacity={prog(f, 235, 24)}
        >
          Sugar enters the cells
        </text>
        <text
          x={1475}
          y={745}
          textAnchor="middle"
          fontFamily={SERIF}
          fontWeight={700}
          fontSize={36}
          fill={C.red}
          opacity={prog(f, 385, 24)}
        >
          Sugar stays in the blood
        </text>
      </svg>
      <Caption
        items={[
          {from: 0, text: 'So what is happening inside the body?'},
          {
            from: 90,
            text: 'Normally, insulin works like a key. It lets sugar move from your blood into your cells for energy.',
          },
          {from: 205, text: 'But sometimes your cells stop responding well to insulin.'},
          {from: 345, text: 'So sugar stays in your blood, and your blood sugar rises.'},
        ]}
      />
    </AbsoluteFill>
  );
};

/* -------------------------------------------------------------------------- */
/*  Scene 4: What raises your risk? (all risk factors in ONE sequence, 30 s)  */
/* -------------------------------------------------------------------------- */

type RiskItem = {icon: React.ReactNode; label: string; desc: string; start: number};

const RiskCard: React.FC<{item: RiskItem}> = ({item}) => {
  const f = useCurrentFrame();
  const p = pop(f, item.start);
  return (
    <div
      style={{
        flex: 1,
        display: 'flex',
        alignItems: 'center',
        gap: 20,
        padding: '0 22px',
        backgroundColor: C.white,
        border: `2.5px solid ${C.navy}`,
        borderRadius: 22,
        opacity: Math.min(1, p * 1.6),
        transform: `scale(${0.88 + 0.12 * Math.min(1.05, p)}) translateY(${(1 - Math.min(1, p)) * 18}px)`,
      }}
    >
      <div style={{width: 72, height: 72, flexShrink: 0}}>{item.icon}</div>
      <div style={{fontFamily: SERIF, minWidth: 0}}>
        <div style={{fontSize: 30, fontWeight: 700, color: C.navy, lineHeight: 1.15}}>{item.label}</div>
        <div style={{fontSize: 21, color: C.gray, marginTop: 4, lineHeight: 1.2}}>{item.desc}</div>
      </div>
    </div>
  );
};

const RiskColumn: React.FC<{
  pill: string;
  color: string;
  pillStart: number;
  items: RiskItem[];
}> = ({pill, color, pillStart, items}) => {
  const f = useCurrentFrame();
  const p = prog(f, pillStart, 22);
  return (
    <div style={{width: 570, display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
      <div
        style={{
          fontFamily: SERIF,
          fontWeight: 700,
          fontSize: 24,
          letterSpacing: 1.5,
          color: '#fff',
          backgroundColor: color,
          padding: '9px 28px',
          borderRadius: 999,
          height: 30,
          display: 'flex',
          alignItems: 'center',
          opacity: p,
          transform: `translateY(${(1 - p) * -10}px)`,
        }}
      >
        {pill}
      </div>
      <div
        style={{
          marginTop: 18,
          width: '100%',
          height: 520,
          display: 'flex',
          flexDirection: 'column',
          gap: 12,
        }}
      >
        {items.map((it) => (
          <RiskCard key={it.label} item={it} />
        ))}
      </div>
    </div>
  );
};

const RisksScene: React.FC = () => {
  const f = useCurrentFrame();

  const fixed: RiskItem[] = [
    {icon: <IconAge />, label: 'Getting older', desc: 'Risk rises, especially after 35–45', start: 32},
    {icon: <IconFamily />, label: 'Family history', desc: 'Parent or sibling with type 2 diabetes', start: 78},
    {icon: <IconGlobe />, label: 'Family background', desc: 'Some backgrounds have higher rates', start: 124},
  ];
  const habits: RiskItem[] = [
    {icon: <IconWeight />, label: 'Extra weight', desc: 'Especially around the belly', start: 182},
    {icon: <IconCouch />, label: 'Not moving much', desc: 'Little regular physical activity', start: 218},
    {icon: <IconCup />, label: 'Sugary diet', desc: 'Lots of sugary drinks and snacks', start: 254},
    {icon: <IconSmoke />, label: 'Smoking', desc: 'Raises the risk of type 2 diabetes', start: 290},
    {icon: <IconMoon />, label: 'Poor sleep', desc: 'Too little or broken sleep', start: 326},
  ];
  const conditions: RiskItem[] = [
    {icon: <IconBP />, label: 'High blood pressure', desc: 'Often 130/80 or higher', start: 398},
    {icon: <IconCholesterol />, label: 'Unhealthy cholesterol', desc: 'Too little good, or too much bad', start: 440},
    {icon: <IconVenus />, label: 'PCOS', desc: 'A common hormone condition in women', start: 482},
    {icon: <IconPregnancy />, label: 'High blood sugar', desc: 'During a past pregnancy', start: 524},
  ];

  const meterIn = prog(f, 560, 24);
  const marker = prog(f, 585, 170);
  const bannerP = prog(f, 790, 24);
  const markerColor = interpolateColors(marker, [0, 0.5, 1], [C.teal, C.orange, C.red]);

  return (
    <AbsoluteFill>
      <Title text="What Raises Your Risk?" />

      <div
        style={{
          position: 'absolute',
          left: 70,
          top: 128,
          width: 1780,
          display: 'flex',
          justifyContent: 'space-between',
        }}
      >
        <RiskColumn pill="OUT OF YOUR CONTROL" color={C.red} pillStart={14} items={fixed} />
        <RiskColumn pill="HABITS YOU CAN CHANGE" color={C.teal} pillStart={168} items={habits} />
        <RiskColumn pill="HEALTH CONDITIONS" color={C.blue} pillStart={382} items={conditions} />
      </div>

      {/* risk meter */}
      <div
        style={{
          position: 'absolute',
          left: 460,
          top: 752,
          width: 1000,
          fontFamily: SERIF,
          opacity: meterIn,
        }}
      >
        <div style={{display: 'flex', justifyContent: 'space-between', fontSize: 24, color: C.gray}}>
          <span>Lower risk</span>
          <span style={{fontWeight: 700, color: C.navy}}>Risk factors add up</span>
          <span>Higher risk</span>
        </div>
        <div
          style={{
            position: 'relative',
            marginTop: 10,
            height: 22,
            borderRadius: 11,
            background: `linear-gradient(90deg, ${C.teal}, ${C.orange}, ${C.red})`,
          }}
        >
          <div
            style={{
              position: 'absolute',
              top: -8,
              left: marker * 966,
              width: 38,
              height: 38,
              borderRadius: 19,
              backgroundColor: markerColor,
              border: `5px solid ${C.white}`,
              boxShadow: `0 0 0 3px ${C.navy}`,
              boxSizing: 'border-box',
            }}
          />
        </div>
      </div>

      <div
        style={{
          position: 'absolute',
          left: 0,
          right: 0,
          top: 846,
          display: 'flex',
          justifyContent: 'center',
          ...fadeUp(bannerP),
        }}
      >
        <div
          style={{
            fontFamily: SERIF,
            fontWeight: 700,
            fontSize: 34,
            color: C.navy,
            backgroundColor: '#FDE9C9',
            border: `3px solid ${C.orange}`,
            borderRadius: 16,
            padding: '8px 34px',
          }}
        >
          High risk = a warning, not a diagnosis
        </div>
      </div>

      <Caption
        items={[
          {from: 0, text: 'Some risk factors are out of your control.'},
          {from: 170, text: 'Other risk factors come from daily life, and these are the ones you can change.'},
          {from: 385, text: 'Certain health conditions also raise your risk.'},
          {
            from: 570,
            text: 'The more risk factors you have, the higher your chance of prediabetes and, later, type 2 diabetes.',
          },
          {from: 790, text: 'But a high risk is a warning, not a diagnosis.'},
        ]}
      />
    </AbsoluteFill>
  );
};

/* -------------------------------------------------------------------------- */
/*  Scene 5: How do you find out?  (20 s)                                     */
/* -------------------------------------------------------------------------- */

type TestCard = {
  name: string;
  desc: string;
  normal: string;
  pre: string;
  icon: React.ReactNode;
  start: number;
};

const RangeBox: React.FC<{label: string; value: string; color: string; tint: string; p: number}> = ({
  label,
  value,
  color,
  tint,
  p,
}) => (
  <div
    style={{
      width: '100%',
      boxSizing: 'border-box',
      backgroundColor: tint,
      borderLeft: `8px solid ${color}`,
      borderRadius: 14,
      padding: '10px 20px 12px',
      opacity: p,
      transform: `translateX(${(1 - p) * -16}px)`,
    }}
  >
    <div style={{fontSize: 20, fontWeight: 700, letterSpacing: 1.5, color, textTransform: 'uppercase'}}>
      {label}
    </div>
    <div style={{fontSize: 36, fontWeight: 700, color: C.navy, marginTop: 2, whiteSpace: 'nowrap'}}>
      {value}
    </div>
  </div>
);

const TestsScene: React.FC = () => {
  const f = useCurrentFrame();

  const cards: TestCard[] = [
    {
      name: 'HbA1C Test',
      desc: 'Average blood sugar over 2–3 months',
      normal: 'Below 5.7%',
      pre: '5.7% – 6.4%',
      icon: <IconDrop size={110} />,
      start: 28,
    },
    {
      name: 'Fasting Glucose',
      desc: 'Blood sugar after not eating overnight',
      normal: 'Below 100 mg/dL',
      pre: '100 – 125 mg/dL',
      icon: <IconMeter size={110} />,
      start: 190,
    },
    {
      name: 'Glucose Tolerance',
      desc: 'Blood sugar before and 2 hours after a sugary drink',
      normal: 'Below 140 mg/dL',
      pre: '140 – 199 mg/dL',
      icon: <IconGlass size={110} />,
      start: 350,
    },
  ];

  return (
    <AbsoluteFill>
      <Title text="How Do You Find Out?" />
      <div
        style={{
          position: 'absolute',
          left: 115,
          top: 190,
          width: 1690,
          display: 'flex',
          justifyContent: 'space-between',
          fontFamily: SERIF,
        }}
      >
        {cards.map((c) => {
          const p = pop(f, c.start);
          const r1 = prog(f, c.start + 36, 24);
          const r2 = prog(f, c.start + 60, 24);
          return (
            <div
              key={c.name}
              style={{
                width: 530,
                height: 590,
                boxSizing: 'border-box',
                padding: '30px 34px 32px',
                backgroundColor: C.white,
                border: `3px solid ${C.navy}`,
                borderRadius: 28,
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                opacity: Math.min(1, p * 1.6),
                transform: `scale(${0.9 + 0.1 * Math.min(1.05, p)}) translateY(${(1 - Math.min(1, p)) * 24}px)`,
              }}
            >
              <div style={{height: 112, display: 'flex', alignItems: 'center'}}>{c.icon}</div>
              <div style={{fontSize: 40, fontWeight: 700, color: C.navy, marginTop: 10}}>{c.name}</div>
              <div
                style={{
                  fontSize: 21,
                  lineHeight: 1.3,
                  color: C.gray,
                  textAlign: 'center',
                  marginTop: 8,
                  height: 56,
                  padding: '0 6px',
                }}
              >
                {c.desc}
              </div>
              <div style={{width: '100%', marginTop: 22, display: 'flex', flexDirection: 'column', gap: 16}}>
                <RangeBox label="Normal" value={c.normal} color={C.teal} tint="#E3F8F5" p={r1} />
                <RangeBox label="Prediabetes" value={c.pre} color={C.orange} tint="#FFF1DA" p={r2} />
              </div>
            </div>
          );
        })}
      </div>
      <Caption
        items={[
          {from: 0, text: 'Your doctor can use a simple blood test to check.'},
          {from: 150, text: 'An HbA1C test shows your average blood sugar. A fasting glucose test checks it after an overnight fast.'},
          {from: 330, text: 'Or a glucose tolerance test, which checks how your body handles a sugary drink.'},
          {from: 480, text: 'If you have risk factors, ask your doctor how often to get tested.'},
        ]}
      />
    </AbsoluteFill>
  );
};

/* -------------------------------------------------------------------------- */
/*  Scene 6: The good news  (14 s)                                            */
/* -------------------------------------------------------------------------- */

const GoodScene: React.FC = () => {
  const f = useCurrentFrame();
  const pct = Math.round(58 * prog(f, 25, 85));
  const heart = pop(f, 8);
  const beat = 1 + Math.sin(f / 7) * 0.03;

  const actions = [
    {icon: <IconWeight size={64} />, text: 'Lose 5–7% of your body weight', start: 150},
    {icon: <IconRunner size={64} />, text: '150 minutes of activity a week', start: 230},
    {icon: <IconApple size={64} />, text: 'Eat more whole foods', start: 315},
  ];

  return (
    <AbsoluteFill>
      <Title text="The Good News: You Can Lower Your Risk" color={C.teal} />

      <div style={{position: 'absolute', left: 110, top: 140, width: 820, fontFamily: SERIF}}>
        <div style={{transform: `scale(${Math.max(0, heart) * beat})`, transformOrigin: 'left center'}}>
          <IconHeart size={120} />
        </div>
        <div style={{fontSize: 270, fontWeight: 700, lineHeight: 1, color: C.teal, marginTop: 6}}>
          {pct}%
        </div>
        <div style={{fontSize: 44, fontWeight: 700, color: C.navy, lineHeight: 1.2, marginTop: 10, ...fadeUp(prog(f, 90, 24))}}>
          lower risk of type 2 diabetes
          <br />
          with lifestyle changes
        </div>
        <div style={{fontSize: 24, color: C.gray, marginTop: 14, lineHeight: 1.3, ...fadeUp(prog(f, 110, 24))}}>
          Major clinical trial (Diabetes Prevention Program),
          <br />
          over about 3 years
        </div>
      </div>

      <div
        style={{
          position: 'absolute',
          left: 960,
          top: 290,
          width: 880,
          display: 'flex',
          flexDirection: 'column',
          gap: 30,
          fontFamily: SERIF,
        }}
      >
        {actions.map((a) => {
          const p = pop(f, a.start);
          return (
            <div
              key={a.text}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: 28,
                padding: '24px 34px',
                backgroundColor: C.white,
                border: `2.5px solid ${C.line}`,
                borderRadius: 24,
                boxShadow: '0 4px 14px rgba(27,58,107,0.08)',
                opacity: Math.min(1, p * 1.6),
                transform: `translateX(${(1 - Math.min(1, p)) * 60}px)`,
              }}
            >
              <div style={{width: 64, height: 64}}>{a.icon}</div>
              <div style={{fontSize: 34, fontWeight: 700, color: C.navy, whiteSpace: 'nowrap'}}>{a.text}</div>
            </div>
          );
        })}
      </div>

      <Caption
        items={[
          {
            from: 0,
            text: 'In a major clinical trial, lifestyle changes lowered the risk of type 2 diabetes by 58%.',
          },
          {from: 150, text: 'Losing 5–7% of your body weight helps.'},
          {from: 230, text: 'Getting about 150 minutes of activity a week.'},
          {from: 315, text: 'And eating more whole foods.'},
        ]}
      />
    </AbsoluteFill>
  );
};

/* -------------------------------------------------------------------------- */
/*  Scene 7: Take action + purpose + references  (14 s)                       */
/* -------------------------------------------------------------------------- */

const CloseScene: React.FC = () => {
  const f = useCurrentFrame();
  const items = [
    'Learn your risk factors',
    'Talk to your doctor about a blood test',
    'Move more, eat well, sleep well',
    'Small steps now protect your health',
  ];

  return (
    <AbsoluteFill>
      <Title text="Take Action Today" />

      <div style={{position: 'absolute', left: 260, top: 150, fontFamily: SERIF}}>
        {items.map((t, i) => {
          const p = pop(f, 24 + i * 38);
          return (
            <div
              key={t}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: 26,
                height: 78,
                opacity: Math.min(1, p * 1.6),
                transform: `translateX(${(1 - Math.min(1, p)) * -40}px)`,
              }}
            >
              <CheckCircle size={52} />
              <div style={{fontSize: 44, fontWeight: 700, color: C.navy}}>{t}</div>
            </div>
          );
        })}
      </div>

      <div
        style={{
          position: 'absolute',
          left: 200,
          width: 1520,
          top: 490,
          boxSizing: 'border-box',
          fontFamily: SERIF,
          backgroundColor: C.white,
          border: `3px solid ${C.teal}`,
          borderRadius: 24,
          padding: '22px 40px',
          ...fadeUp(prog(f, 200, 26)),
        }}
      >
        <div style={{fontSize: 22, fontWeight: 700, letterSpacing: 2, color: C.teal}}>WHY WE MADE THIS VIDEO</div>
        <div style={{fontSize: 36, color: C.navy, lineHeight: 1.3, marginTop: 6}}>
          To spread community awareness and help more people learn about prediabetes.
        </div>
      </div>

      <div
        style={{
          position: 'absolute',
          left: 200,
          width: 1520,
          top: 690,
          boxSizing: 'border-box',
          fontFamily: SERIF,
          backgroundColor: 'rgba(255,255,255,0.9)',
          border: `2px solid ${C.line}`,
          borderRadius: 24,
          padding: '20px 40px',
          ...fadeUp(prog(f, 255, 26)),
        }}
      >
        <div style={{fontSize: 22, fontWeight: 700, letterSpacing: 2, color: C.gray}}>REFERENCES</div>
        <div style={{fontSize: 28, color: C.navy, lineHeight: 1.4, marginTop: 6}}>
          American Diabetes Association (ADA) – Standards of Care in Diabetes
        </div>
        <div style={{fontSize: 28, color: C.navy, lineHeight: 1.4}}>
          Centers for Disease Control and Prevention (CDC) – Prediabetes Guidelines
        </div>
      </div>

      <Caption
        items={[
          {from: 0, text: 'Small steps now can protect your health for years.'},
          {from: 300, text: 'This video is for education only and is not medical advice.'},
        ]}
      />
    </AbsoluteFill>
  );
};

/* -------------------------------------------------------------------------- */
/*  Main composition                                                          */
/* -------------------------------------------------------------------------- */

export const ExplainerVideo: React.FC = () => {
  const scenes: Array<{d: number; node: React.ReactNode}> = [
    {d: D.intro, node: <IntroScene />},
    {d: D.gauge, node: <GaugeScene />},
    {d: D.body, node: <BodyScene />},
    {d: D.risks, node: <RisksScene />},
    {d: D.tests, node: <TestsScene />},
    {d: D.good, node: <GoodScene />},
    {d: D.close, node: <CloseScene />},
  ];

  let from = 0;
  return (
    <AbsoluteFill style={{backgroundColor: C.bg}}>
      <Background />
      <Audio src={staticFile('music.mp3')} />
      {scenes.map((s, i) => {
        const start = from;
        from += s.d;
        return (
          <Sequence key={i} from={start} durationInFrames={s.d}>
            <SceneFade duration={s.d}>{s.node}</SceneFade>
          </Sequence>
        );
      })}
      <ProgressBar />
    </AbsoluteFill>
  );
};

export const RemotionRoot: React.FC = () => (
  <Composition
    id="PrediabetesExplainer"
    component={ExplainerVideo}
    durationInFrames={TOTAL_FRAMES}
    fps={FPS}
    width={WIDTH}
    height={HEIGHT}
  />
);

import React from "react";
import {AbsoluteFill, Sequence, interpolate, spring, useCurrentFrame, useVideoConfig} from "remotion";

const C = {bg1: "#0b1f2a", bg2: "#134e5e", accent: "#2ee6a6", warn: "#ffb703", text: "#f4f9fb", dim: "#9fb8c4"};
const font = "Inter, 'Segoe UI', Helvetica, Arial, sans-serif";

// ---- EDIT THESE: example profile and scoring (simplified, educational) ----
const MAX_SCORE = 11;
const HIGH_RISK_AT = 5;
const FACTORS = [
  {label: "Age 50–59", pts: 2},
  {label: "Parent or sibling with diabetes", pts: 1},
  {label: "High blood pressure", pts: 1},
  {label: "Physically inactive", pts: 1},
  {label: "Overweight (BMI 25–29.9)", pts: 1},
];
const TOTAL = FACTORS.reduce((s, f) => s + f.pts, 0);
// ---------------------------------------------------------------------------

const Scene: React.FC<{dur: number; children: React.ReactNode}> = ({dur, children}) => {
  const f = useCurrentFrame();
  const opacity = interpolate(f, [0, 15, dur - 15, dur], [0, 1, 1, 0], {extrapolateLeft: "clamp", extrapolateRight: "clamp"});
  return (
    <AbsoluteFill style={{opacity, justifyContent: "center", alignItems: "center", fontFamily: font, color: C.text}}>
      {children}
    </AbsoluteFill>
  );
};

const Title: React.FC = () => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const s = spring({frame: f, fps, config: {damping: 14}});
  const sub = interpolate(f, [25, 50], [0, 1], {extrapolateRight: "clamp"});
  return (
    <Scene dur={90}>
      <div style={{textAlign: "center", transform: `scale(${0.85 + 0.15 * s})`}}>
        <div style={{fontSize: 130, fontWeight: 800, letterSpacing: -2}}>
          Prediabetes <span style={{color: C.accent}}>Risk Score</span>
        </div>
        <div style={{fontSize: 48, color: C.dim, marginTop: 24, opacity: sub}}>
          How a simple screening calculator works
        </div>
      </div>
    </Scene>
  );
};

const Factors: React.FC = () => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const per = 35;
  const shown = FACTORS.filter((_, i) => f >= 15 + i * per);
  const running = shown.reduce((s, x) => s + x.pts, 0);
  return (
    <Scene dur={240}>
      <div style={{width: 1300}}>
        <div style={{fontSize: 56, fontWeight: 700, marginBottom: 40}}>
          Each risk factor adds points <span style={{color: C.dim, fontSize: 34}}>(example profile)</span>
        </div>
        {FACTORS.map((x, i) => {
          const p = spring({frame: f - (15 + i * per), fps, config: {damping: 15}});
          return (
            <div key={x.label} style={{
              display: "flex", justifyContent: "space-between", alignItems: "center",
              background: "rgba(255,255,255,0.08)", borderRadius: 20, padding: "22px 36px", marginBottom: 18,
              fontSize: 44, opacity: p, transform: `translateX(${(1 - p) * 120}px)`,
            }}>
              <span>{x.label}</span>
              <span style={{color: C.accent, fontWeight: 800}}>+{x.pts}</span>
            </div>
          );
        })}
        <div style={{textAlign: "right", fontSize: 52, marginTop: 20, color: C.dim}}>
          Running total: <b style={{color: C.text}}>{running}</b>
        </div>
      </div>
    </Scene>
  );
};

const Gauge: React.FC = () => {
  const f = useCurrentFrame();
  const t = interpolate(f, [20, 90], [0, 1], {extrapolateLeft: "clamp", extrapolateRight: "clamp"});
  const score = Math.round(TOTAL * t);
  const high = TOTAL >= HIGH_RISK_AT;
  const color = high ? C.warn : C.accent;
  const W = 1300;
  return (
    <Scene dur={150}>
      <div style={{width: W}}>
        <div style={{fontSize: 56, fontWeight: 700, marginBottom: 30}}>Your total score</div>
        <div style={{fontSize: 220, fontWeight: 900, color, lineHeight: 1}}>
          {score}<span style={{fontSize: 70, color: C.dim}}> / {MAX_SCORE}</span>
        </div>
        <div style={{position: "relative", height: 44, borderRadius: 22, background: "rgba(255,255,255,0.12)", marginTop: 50}}>
          <div style={{height: "100%", width: `${(TOTAL / MAX_SCORE) * 100 * t}%`, borderRadius: 22, background: color}} />
          <div style={{position: "absolute", left: `${(HIGH_RISK_AT / MAX_SCORE) * 100}%`, top: -18, height: 80, width: 4, background: C.text}} />
          <div style={{position: "absolute", left: `${(HIGH_RISK_AT / MAX_SCORE) * 100}%`, top: 70, transform: "translateX(-50%)", fontSize: 30, color: C.dim}}>
            {HIGH_RISK_AT}+ = higher risk
          </div>
        </div>
      </div>
    </Scene>
  );
};

const Result: React.FC = () => {
  const f = useCurrentFrame();
  const a = (d: number) => interpolate(f, [d, d + 20], [0, 1], {extrapolateRight: "clamp"});
  return (
    <Scene dur={120}>
      <div style={{width: 1300}}>
        <div style={{fontSize: 80, fontWeight: 800, color: C.warn, opacity: a(5)}}>Higher risk — time to get tested</div>
        <div style={{fontSize: 46, marginTop: 40, opacity: a(30), lineHeight: 1.5}}>
          A blood test (A1C or fasting glucose) can confirm prediabetes.<br />
          Activity, weight, and diet changes can lower your risk.
        </div>
        <div style={{fontSize: 32, marginTop: 60, color: C.dim, opacity: a(60), lineHeight: 1.4}}>
          Educational screening only — not a diagnosis. Talk to a doctor about your results.
        </div>
      </div>
    </Scene>
  );
};

export const Video: React.FC = () => {
  const f = useCurrentFrame();
  const shift = interpolate(f, [0, 600], [0, 40]);
  return (
    <AbsoluteFill style={{background: `linear-gradient(${135 + shift}deg, ${C.bg1}, ${C.bg2})`}}>
      <Sequence from={0} durationInFrames={90}><Title /></Sequence>
      <Sequence from={90} durationInFrames={240}><Factors /></Sequence>
      <Sequence from={330} durationInFrames={150}><Gauge /></Sequence>
      <Sequence from={480} durationInFrames={120}><Result /></Sequence>
    </AbsoluteFill>
  );
};

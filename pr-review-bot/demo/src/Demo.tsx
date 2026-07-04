import {
  AbsoluteFill,
  Img,
  Sequence,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';

export const FPS = 30;
export const DURATION_IN_FRAMES = 1200; // 40s

const C = {
  bg: '#0d1117',
  text: '#e6edf3',
  muted: '#8b949e',
  green: '#3fb950',
  blue: '#58a6ff',
  purple: '#bc8cff',
  orange: '#f0883e',
};
const MONO = 'ui-monospace, "SF Mono", Menlo, Consolas, monospace';
const SANS = '-apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif';

const fadeUp = (frame: number, start: number, dur = 15) => {
  const p = interpolate(frame, [start, start + dur], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  return {opacity: p, transform: `translateY(${(1 - p) * 20}px)`};
};

// Caption pill, bottom-left
const Caption: React.FC<{children: React.ReactNode; delay?: number}> = ({children, delay = 6}) => {
  const frame = useCurrentFrame();
  return (
    <div
      style={{
        position: 'absolute',
        left: 64,
        bottom: 64,
        ...fadeUp(frame, delay),
        backgroundColor: 'rgba(13,17,23,0.92)',
        border: `1px solid ${C.orange}`,
        color: C.text,
        borderRadius: 12,
        padding: '18px 30px',
        fontSize: 40,
        fontFamily: SANS,
        fontWeight: 600,
        maxWidth: 1400,
      }}
    >
      {children}
    </div>
  );
};

// ── Scene 1: Title ───────────────────────────────────────────────────────
const Title: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const pop = spring({frame, fps, config: {damping: 14}});
  return (
    <AbsoluteFill style={{backgroundColor: C.bg, color: C.text, fontFamily: SANS, justifyContent: 'center', alignItems: 'center', textAlign: 'center'}}>
      <div style={{transform: `scale(${0.9 + pop * 0.1})`, opacity: pop}}>
        <div style={{fontSize: 110, fontWeight: 800}}>🤖 PR Review Bot</div>
        <div style={{fontSize: 42, color: C.muted, marginTop: 20}}>
          LLM code review, the moment a PR opens.
        </div>
      </div>
      <div style={{...fadeUp(frame, 30), marginTop: 48, fontSize: 36, color: C.green, fontFamily: MONO}}>
        ⚡ ~500-line diff reviewed in ~3s
      </div>
    </AbsoluteFill>
  );
};

// ── Scene 2: real PR review, panned ──────────────────────────────────────
const PRReview: React.FC = () => {
  const frame = useCurrentFrame();
  // slow pan from the PR header down through the bot's 3 findings
  const top = interpolate(frame, [0, 600], [-120, -1560], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  return (
    <AbsoluteFill style={{backgroundColor: '#ffffff', overflow: 'hidden'}}>
      <Img
        src={staticFile('shots/pr_conversation.png')}
        style={{position: 'absolute', top, left: 0, width: 1920}}
      />
      <Caption>A real PR → the bot's actual, structured review</Caption>
    </AbsoluteFill>
  );
};

// A still shot with a gentle zoom, showing the top of the page
const ZoomShot: React.FC<{file: string; caption: React.ReactNode}> = ({file, caption}) => {
  const frame = useCurrentFrame();
  const scale = interpolate(frame, [0, 165], [1, 1.06], {extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{backgroundColor: '#ffffff', overflow: 'hidden'}}>
      <Img
        src={staticFile(file)}
        style={{position: 'absolute', top: 0, left: 0, width: 1920, transformOrigin: 'top center', transform: `scale(${scale})`}}
      />
      <Caption>{caption}</Caption>
    </AbsoluteFill>
  );
};

// ── Scene 5: Outro ───────────────────────────────────────────────────────
const Outro: React.FC = () => {
  const frame = useCurrentFrame();
  const badges = [
    {t: '● Live on Railway', c: C.green},
    {t: '✓ pytest CI green', c: C.green},
    {t: '~500 LOC in ~3s', c: C.blue},
    {t: 'Pydantic-validated', c: C.purple},
  ];
  return (
    <AbsoluteFill style={{backgroundColor: C.bg, color: C.text, fontFamily: SANS, justifyContent: 'center', alignItems: 'center', textAlign: 'center'}}>
      <div style={{...fadeUp(frame, 0), fontSize: 84, fontWeight: 800}}>Shipped. 🚀</div>
      <div style={{display: 'flex', gap: 18, flexWrap: 'wrap', marginTop: 40, justifyContent: 'center', maxWidth: 1500}}>
        {badges.map((b, i) => (
          <div
            key={b.t}
            style={{
              ...fadeUp(frame, 12 + i * 10),
              border: `1px solid ${b.c}`,
              color: b.c,
              borderRadius: 999,
              padding: '16px 30px',
              fontSize: 32,
              fontFamily: MONO,
            }}
          >
            {b.t}
          </div>
        ))}
      </div>
      <div style={{...fadeUp(frame, 60), marginTop: 52, fontSize: 30, color: C.muted, fontFamily: MONO}}>
        github.com/m67uzair/ai-pivot-practice · /pr-review-bot
      </div>
    </AbsoluteFill>
  );
};

export const Demo: React.FC = () => {
  return (
    <AbsoluteFill style={{backgroundColor: C.bg}}>
      <Sequence durationInFrames={90}>
        <Title />
      </Sequence>
      <Sequence from={90} durationInFrames={600}>
        <PRReview />
      </Sequence>
      <Sequence from={690} durationInFrames={165}>
        <ZoomShot file="shots/pr_diff.png" caption="…on the buggy diff it flagged" />
      </Sequence>
      <Sequence from={855} durationInFrames={165}>
        <ZoomShot file="shots/live_docs.png" caption="Live on Railway — FastAPI /docs" />
      </Sequence>
      <Sequence from={1020} durationInFrames={180}>
        <Outro />
      </Sequence>
    </AbsoluteFill>
  );
};

import {
  AbsoluteFill,
  Sequence,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';

export const FPS = 30;
export const DURATION_IN_FRAMES = 2700; // 90s

// ── GitHub dark palette ──────────────────────────────────────────────────
const C = {
  bg: '#0d1117',
  card: '#161b22',
  border: '#30363d',
  text: '#e6edf3',
  muted: '#8b949e',
  green: '#3fb950',
  blue: '#58a6ff',
  purple: '#bc8cff',
  orange: '#f0883e',
  red: '#f85149',
  yellow: '#d29922',
};
const MONO = 'ui-monospace, "SF Mono", Menlo, Consolas, monospace';
const SANS = '-apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif';

const REVIEW_SUMMARY =
  'The new transfer and apply_interest functions introduce functional bugs: a mutable ' +
  'default argument in transfer can leak history across calls, and transfer lacks validation ' +
  'for sufficient funds and non-negative amounts. apply_interest also miscalculates interest ' +
  'by omitting the percent-to-fraction conversion.';

const ISSUES = [
  {
    sev: 'HIGH',
    color: C.orange,
    dot: '🟠',
    title: 'Mutable default argument for history',
    why: 'A list default is shared across all calls, so histories leak between unrelated transfers.',
  },
  {
    sev: 'HIGH',
    color: C.orange,
    dot: '🟠',
    title: 'No sufficient-funds validation in transfer',
    why: 'Balances are mutated with no checks — allowing overdrafts and negative transfers.',
  },
  {
    sev: 'MEDIUM',
    color: C.yellow,
    dot: '🟡',
    title: 'Interest treats rate as a raw multiplier',
    why: 'Percent is never divided by 100, inflating the applied interest ~100×.',
  },
];

const BUGGY_CODE = `def transfer(source, dest, amount, history=[]):
    source.balance -= amount
    dest.balance   += amount
    history.append({"amount": amount})
    return history

def apply_interest(account, rate):
    account.balance += account.balance * rate / 12
    return account.balance`;

// fade-up helper
const fadeUp = (frame: number, start: number, dur = 15) => {
  const p = interpolate(frame, [start, start + dur], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  return {opacity: p, transform: `translateY(${(1 - p) * 24}px)`};
};

const Scene: React.FC<{children: React.ReactNode; pad?: number}> = ({children, pad = 120}) => (
  <AbsoluteFill style={{backgroundColor: C.bg, color: C.text, fontFamily: SANS, padding: pad, justifyContent: 'center'}}>
    {children}
  </AbsoluteFill>
);

// ── Scene 1: Title ───────────────────────────────────────────────────────
const Title: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const pop = spring({frame, fps, config: {damping: 14}});
  return (
    <Scene>
      <div style={{transform: `scale(${0.9 + pop * 0.1})`, opacity: pop}}>
        <div style={{fontSize: 96, fontWeight: 800}}>🤖 PR Review Bot</div>
        <div style={{fontSize: 40, color: C.muted, marginTop: 24}}>
          Automated, structured code review — the moment a PR opens.
        </div>
      </div>
      <div style={{...fadeUp(frame, 40), marginTop: 60, fontSize: 34, color: C.green, fontFamily: MONO}}>
        ⚡ reviews a ~500-line diff in ~3s
      </div>
    </Scene>
  );
};

// ── Scene 2: The buggy PR ────────────────────────────────────────────────
const BuggyPR: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Scene>
      <div style={{...fadeUp(frame, 0), fontSize: 44, fontWeight: 700, marginBottom: 8}}>
        You open a PR with <span style={{color: C.orange}}>subtle bugs</span>…
      </div>
      <div style={{...fadeUp(frame, 12), fontSize: 28, color: C.muted, marginBottom: 32}}>
        bank.py — looks fine at a glance
      </div>
      <div
        style={{
          ...fadeUp(frame, 24),
          backgroundColor: C.card,
          border: `1px solid ${C.border}`,
          borderRadius: 12,
          padding: 40,
          fontFamily: MONO,
          fontSize: 30,
          lineHeight: 1.5,
          whiteSpace: 'pre',
          color: C.text,
        }}
      >
        {BUGGY_CODE}
      </div>
    </Scene>
  );
};

// ── Scene 3: Pipeline ────────────────────────────────────────────────────
const Pipeline: React.FC = () => {
  const frame = useCurrentFrame();
  const steps = ['webhook (verified)', 'fetch the diff', 'LLM review', 'post comment'];
  return (
    <Scene>
      <div style={{...fadeUp(frame, 0), fontSize: 40, color: C.muted, marginBottom: 48}}>
        FastAPI · LiteLLM · instructor · SQLAlchemy
      </div>
      <div style={{display: 'flex', gap: 28, alignItems: 'center', flexWrap: 'wrap'}}>
        {steps.map((s, i) => (
          <div key={s} style={{display: 'flex', alignItems: 'center', gap: 28}}>
            <div
              style={{
                ...fadeUp(frame, 10 + i * 22),
                backgroundColor: C.card,
                border: `1px solid ${C.border}`,
                borderRadius: 10,
                padding: '22px 34px',
                fontSize: 32,
                fontFamily: MONO,
              }}
            >
              {s}
            </div>
            {i < steps.length - 1 && (
              <div style={{...fadeUp(frame, 18 + i * 22), fontSize: 40, color: C.green}}>→</div>
            )}
          </div>
        ))}
      </div>
    </Scene>
  );
};

// ── Scene 4: The review comment ──────────────────────────────────────────
const IssueCard: React.FC<{issue: (typeof ISSUES)[number]; start: number}> = ({issue, start}) => {
  const frame = useCurrentFrame();
  return (
    <div
      style={{
        ...fadeUp(frame, start, 18),
        borderLeft: `6px solid ${issue.color}`,
        backgroundColor: '#0d1117',
        border: `1px solid ${C.border}`,
        borderLeftColor: issue.color,
        borderRadius: 8,
        padding: '24px 30px',
        marginTop: 22,
      }}
    >
      <div style={{fontSize: 30, fontWeight: 700}}>
        <span style={{color: issue.color}}>{issue.dot} {issue.sev}</span>
        <span style={{color: C.text}}> — {issue.title}</span>
      </div>
      <div style={{fontSize: 24, color: C.muted, fontFamily: MONO, marginTop: 6}}>bank.py</div>
      <div style={{fontSize: 26, color: C.text, marginTop: 12, lineHeight: 1.4}}>{issue.why}</div>
    </div>
  );
};

const ReviewCard: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill style={{backgroundColor: C.bg, color: C.text, fontFamily: SANS, padding: 90}}>
      <div style={{...fadeUp(frame, 0), fontSize: 40, fontWeight: 700, marginBottom: 24}}>
        …and the bot reviews it — <span style={{color: C.green}}>structured &amp; validated</span>
      </div>
      <div
        style={{
          backgroundColor: C.card,
          border: `1px solid ${C.border}`,
          borderRadius: 12,
          padding: 44,
          flex: 1,
        }}
      >
        <div style={{...fadeUp(frame, 6), fontSize: 40, fontWeight: 800, marginBottom: 20}}>
          🤖 Automated review
        </div>
        <div style={{...fadeUp(frame, 14), fontSize: 27, color: C.text, lineHeight: 1.45, marginBottom: 10}}>
          {REVIEW_SUMMARY}
        </div>
        {ISSUES.map((iss, i) => (
          <IssueCard key={iss.title} issue={iss} start={40 + i * 60} />
        ))}
      </div>
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
    <Scene>
      <div style={{...fadeUp(frame, 0), fontSize: 76, fontWeight: 800}}>Shipped. 🚀</div>
      <div style={{display: 'flex', gap: 20, flexWrap: 'wrap', marginTop: 40}}>
        {badges.map((b, i) => (
          <div
            key={b.t}
            style={{
              ...fadeUp(frame, 12 + i * 10),
              border: `1px solid ${b.c}`,
              color: b.c,
              borderRadius: 999,
              padding: '16px 30px',
              fontSize: 30,
              fontFamily: MONO,
            }}
          >
            {b.t}
          </div>
        ))}
      </div>
      <div style={{...fadeUp(frame, 60), marginTop: 56, fontSize: 30, color: C.muted, fontFamily: MONO}}>
        github.com/m67uzair/ai-pivot-practice · /pr-review-bot
      </div>
    </Scene>
  );
};

// ── Timeline ─────────────────────────────────────────────────────────────
export const Demo: React.FC = () => {
  return (
    <AbsoluteFill style={{backgroundColor: C.bg}}>
      <Sequence durationInFrames={150}>
        <Title />
      </Sequence>
      <Sequence from={150} durationInFrames={390}>
        <BuggyPR />
      </Sequence>
      <Sequence from={540} durationInFrames={180}>
        <Pipeline />
      </Sequence>
      <Sequence from={720} durationInFrames={1530}>
        <ReviewCard />
      </Sequence>
      <Sequence from={2250} durationInFrames={450}>
        <Outro />
      </Sequence>
    </AbsoluteFill>
  );
};

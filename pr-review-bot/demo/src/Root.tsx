import {Composition} from 'remotion';
import {Demo, FPS, DURATION_IN_FRAMES} from './Demo';

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="Demo"
      component={Demo}
      durationInFrames={DURATION_IN_FRAMES}
      fps={FPS}
      width={1920}
      height={1080}
    />
  );
};

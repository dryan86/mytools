using UnityEngine;
using UnityEngine.Playables;

namespace GfxTimeline
{
    public class GfxAnimatorMixerBehaviour : PlayableBehaviour
    {
        private RD_Visible_Animator visibleAnimator;
        private AnimationName animationName;

        public override void PrepareFrame(Playable playable, FrameData info)
        {
            int inputCount = playable.GetInputCount();

            for (int i = 0; i < inputCount; i++)
            {
                float inputWeight = playable.GetInputWeight(i);
                ScriptPlayable<GfxAnimatorBehaviour> inputPlayable = (ScriptPlayable<GfxAnimatorBehaviour>)playable.GetInput(i);
                GfxAnimatorBehaviour input = inputPlayable.GetBehaviour();

                if (inputWeight == 1.0f && animationName != input.animationName)
                {
                    animationName = input.animationName;
                }
            }

            base.PrepareFrame(playable, info);
        }

        public override void ProcessFrame(Playable playable, FrameData info, object playerData)
        {
            visibleAnimator = playerData as RD_Visible_Animator;
            if (visibleAnimator == null) return;

            if (visibleAnimator.GetCurrentAnimaionName() != animationName) {
                visibleAnimator.PlayAnimation(animationName, true);
            }

            visibleAnimator.UpdateRender();
        }

        public override void OnGraphStop(Playable playable)
        {
            if (visibleAnimator == null) return;

        }
    }
}
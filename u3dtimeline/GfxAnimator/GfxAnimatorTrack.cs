using UnityEngine;
using UnityEngine.Playables;
using UnityEngine.Timeline;


namespace GfxTimeline
{
    [TrackColor(0.9960785f, 0.2509804f, 0.003921569f)]
    [TrackClipType(typeof(GfxAnimatorClip))]
    [TrackBindingType(typeof(RD_Visible_Animator))]
    public class GfxAnimatorTrack : TrackAsset
    {

        internal RD_Visible_Animator GetBinding(PlayableDirector director)
        {
            if (director == null)
                return null;

            UnityEngine.Object key = this;
            if (isSubTrack)
                key = parent;

            UnityEngine.Object binding = null;
            if (director != null)
                binding = director.GetGenericBinding(key);

            RD_Visible_Animator animator = null;
            if (binding != null) // the binding can be an animator or game object
            {
                animator = binding as RD_Visible_Animator;
                var gameObject = binding as GameObject;
                if (animator == null && gameObject != null)
                    animator = gameObject.GetComponent<RD_Visible_Animator>();
            }

            return animator;
        }

        public override Playable CreateTrackMixer(PlayableGraph graph, GameObject go, int inputCount)
        {
            Playable newPlayerable = ScriptPlayable<GfxAnimatorMixerBehaviour>.Create(graph, inputCount);

            RD_Visible_Animator visibleAnimator = GetBinding(go != null ? go.GetComponent<PlayableDirector>() : null);
            visibleAnimator.Init();

            return newPlayerable;
        }
    }
}
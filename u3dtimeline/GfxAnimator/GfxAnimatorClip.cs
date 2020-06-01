using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Playables;
using UnityEngine.Timeline;

namespace GfxTimeline
{
    [Serializable]
    public class GfxAnimatorClip : PlayableAsset, ITimelineClipAsset
    {
        public GfxAnimatorBehaviour template = new GfxAnimatorBehaviour();

        public ClipCaps clipCaps { get { return ClipCaps.Blending | ClipCaps.ClipIn | ClipCaps.SpeedMultiplier; } }

        public override Playable CreatePlayable(PlayableGraph graph, GameObject owner)
        {
            var playable = ScriptPlayable<GfxAnimatorBehaviour>.Create(graph, template);

            return playable;
        }

        public override double duration
        {
            get
            {
                if (template.visibleReference == null || template.animationName == AnimationName.NONE)
                    return 0;
                return template.visibleReference.GetAnimationLength(template.animationName);
            }
        }
    }
}
using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Playables;
using UnityEngine.Timeline;

namespace GfxTimeline
{
    [Serializable]
    public class GfxAnimatorBehaviour : PlayableBehaviour
    {
        public RD_Visible_Animator visibleReference;
        public AnimationName animationName;

        public bool isBullet;
    }
}
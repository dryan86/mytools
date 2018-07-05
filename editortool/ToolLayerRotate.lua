local ToolLayerRotate = class("ToolLayerRotate", function(params)
    local layer = cc.Node:create()

    return layer
end)


function ToolLayerRotate:ctor(params)
	self.targetNode = params.target
	self.oldRotate = self.targetNode:getRotation()

	local tipSize = {width = 80, height = 80}
	self.tipSize = tipSize
	local tipLayer = cc.LayerColor:create(cc.c3b(22, 22, 22))
	self.tipLayer = tipLayer
	tipLayer:setContentSize(tipSize)
    tipLayer:setIgnoreAnchorPointForPosition(false)
	tipLayer:setOpacity(120)
    -- 根据anchor设置位置
    local targetSize = self.targetNode:getContentSize()
    local anchorPoint = self.targetNode:getAnchorPoint()
    local tipPos = cc.p(anchorPoint.x * targetSize.width, anchorPoint.y * targetSize.height)
    tipLayer:setIgnoreAnchorPointForPosition(false)
    tipLayer:setPosition(tipPos)

	local tipSprite = cc.Sprite:create("editor/transform-rotate.png")
	tipSprite:setPosition(tipSize.width/2, tipSize.height/2)
	tipLayer:addChild(tipSprite)

	self:addChild(tipLayer)

	-- registerTouch
	self:registerTouch()
end


function ToolLayerRotate:registerTouch()
	local beginAngle = nil
    local dir = nil
    -- 该layer的世界坐标
    local worldCenter = self.targetNode:getParent():convertToWorldSpace(cc.p(self.targetNode:getPosition()))

    local function getDegree(p)
        local angle = cc.pToAngleSelf(p) * 180 / 3.14

        if angle < 0 then
            angle = angle + 360
        end

        return angle
    end

    local function onTouchBegan(touch, event)
        local location = touch:getLocation()

        local uiPos = self.targetNode:getParent():convertToNodeSpace(location)
        local worldPos = self.targetNode:getParent():convertToWorldSpace(uiPos)
        local diffPos = cc.pSub(worldPos, worldCenter)

        if diffPos.x < self.tipSize.width/2 and diffPos.x > -self.tipSize.width/2 and diffPos.y < self.tipSize.height/2 and diffPos.y > -self.tipSize.height/2 then
        	self.tipLayer:setColor(cc.c3b(52, 52, 52))
            beginAngle = getDegree(diffPos)
            print(beginAngle)
        	return true
        end

        self.tipLayer:setColor(cc.c3b(22, 22, 22))

        return false
    end

    local function onTouchMoved(touch, event)
        local location = touch:getLocation()
        local uiPos = self.targetNode:getParent():convertToNodeSpace(location)
        local worldPos = self.targetNode:getParent():convertToWorldSpace(uiPos)
        local diffPos = cc.pSub(worldPos, worldCenter)

        local newAngle = getDegree(diffPos)
        local diffAngle = newAngle - beginAngle

        if dir == nil then
            dir = diffAngle
        end

        -- 修正角度
        if dir ~= nil and dir < 0 then
            diffAngle = diffAngle - 360

            if diffAngle < -360 then
                diffAngle = diffAngle + 360
            end
        end

        if dir ~= nil and dir > 0 then
            diffAngle = diffAngle + 360

            if diffAngle > 360 then
                diffAngle = diffAngle - 360
            end
        end

        local newRotate = self.oldRotate - diffAngle

        self.targetNode:setRotation(newRotate)
    end

    local function onTouchEnded(touch, event)
    	self.tipLayer:setColor(cc.c3b(22, 22, 22))
        dir = nil

        self.oldRotate = self.targetNode:getRotation()
    end


    local  listenner = cc.EventListenerTouchOneByOne:create()
    listenner:setSwallowTouches(true)
    listenner:registerScriptHandler(onTouchBegan, cc.Handler.EVENT_TOUCH_BEGAN )
    listenner:registerScriptHandler(onTouchMoved, cc.Handler.EVENT_TOUCH_MOVED )
    listenner:registerScriptHandler(onTouchEnded, cc.Handler.EVENT_TOUCH_ENDED )

    local eventDispatcher = self:getEventDispatcher()
    eventDispatcher:addEventListenerWithSceneGraphPriority(listenner, self)
end


return ToolLayerRotate
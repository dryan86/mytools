local ScaleMode = {
	AxisX = 1,
	AxisY = 2,
	AxisBoth = 3,
	AxisNone = -1
}


local ToolLayerScale = class("ToolLayerScale", function(params)
    local layer = cc.Node:create()

    return layer
end)


function ToolLayerScale:ctor(params)
	self.targetNode = params.target
	self.oldScaleX = self.targetNode:getScaleX()
	self.oldScaleY = self.targetNode:getScaleY()
    self.oldScale = self.targetNode:getScale()

	local tipSize = cc.size(80, 80)
	local axisSize = cc.size(20, 20)
	self.tipSize = tipSize
	self.axisSize = axisSize

	local tipLayer = cc.LayerColor:create(cc.c3b(22, 22, 22))
	tipLayer:setOpacity(100)
	tipLayer:setContentSize(tipSize)
    -- 根据anchor设置位置
    local targetSize = self.targetNode:getContentSize()
    local anchorPoint = self.targetNode:getAnchorPoint()
    local tipPos = cc.p(anchorPoint.x * targetSize.width, anchorPoint.y * targetSize.height)
    tipLayer:setIgnoreAnchorPointForPosition(false)
    tipLayer:setPosition(tipPos)
	
	local tipSprite = cc.Sprite:create("editor/transform-scale.png")
	tipSprite:setPosition(tipSize.width/2, tipSize.height/2)
	tipLayer:addChild(tipSprite)

	self:addChild(tipLayer)

	local axisXLayer = cc.LayerColor:create(cc.c3b(22, 200, 22))
	axisXLayer:setOpacity(100)
	axisXLayer:setIgnoreAnchorPointForPosition(false)
	axisXLayer:setContentSize(axisSize)
	local spriteX = cc.Sprite:create("editor/axis-x.png")
	spriteX:setPosition(axisSize.width/2, axisSize.height/2)
	axisXLayer:addChild(spriteX)
	axisXLayer:setPosition(tipSize.width, tipSize.height/2)
	tipLayer:addChild(axisXLayer)

	local axisYLayer = cc.LayerColor:create(cc.c3b(200, 22, 22))
	axisYLayer:setOpacity(100)
	axisYLayer:setIgnoreAnchorPointForPosition(false)
	axisYLayer:setContentSize(axisSize)
	local spriteY = cc.Sprite:create("editor/axis-y.png")
	spriteY:setPosition(axisSize.width/2, axisSize.height/2)
	axisYLayer:addChild(spriteY)
	axisYLayer:setPosition(tipSize.width/2, tipSize.height)
	tipLayer:addChild(axisYLayer)

    local axisXYLayer = cc.LayerColor:create(cc.c3b(200, 22, 22))
    axisXYLayer:setOpacity(100)
    axisXYLayer:setIgnoreAnchorPointForPosition(false)
    axisXYLayer:setContentSize(axisSize)
    local spriteXY = cc.Sprite:create("editor/axis-xy.png")
    spriteXY:setPosition(axisSize.width/2, axisSize.height/2)
    axisXYLayer:addChild(spriteXY)
    axisXYLayer:setPosition(tipSize.width/2, tipSize.height/2)
    tipLayer:addChild(axisXYLayer)

	self.axisXLayer = axisXLayer
	self.axisYLayer = axisYLayer
    self.axisXYLayer = axisXYLayer

	self:registerTouch()
end

function ToolLayerScale:registerTouch()
	local beginPos = nil
	local curMode = ScaleMode.AsixNone

    local function onTouchBegan(touch, event)
    	local location = touch:getLocation()

        local uiPos1 = self.axisXLayer:convertToNodeSpace(location)
        if uiPos1.x < self.axisSize.width and uiPos1.x > 0 and uiPos1.y < self.axisSize.height and uiPos1.y > 0 then
        	self.axisXLayer:setColor(cc.c3b(52, 52, 52))
        	beginPos = location

        	curMode = ScaleMode.AxisX

        	return true
        end

        local uiPos2 = self.axisYLayer:convertToNodeSpace(location)
        if uiPos2.x < self.axisSize.width and uiPos2.x > 0 and uiPos2.y < self.axisSize.height and uiPos2.y > 0 then
        	self.axisYLayer:setColor(cc.c3b(52, 52, 52))
        	beginPos = location

        	curMode = ScaleMode.AxisY

        	return true
        end

        local uiPos3 = self.axisXYLayer:convertToNodeSpace(location)
        if uiPos3.x < self.axisSize.width and uiPos3.x > 0 and uiPos3.y < self.axisSize.height and uiPos3.y > 0 then
            self.axisXYLayer:setColor(cc.c3b(52, 52, 52))
            beginPos = location

            curMode = ScaleMode.AxisBoth

            return true
        end

        return false
    end

    local function onTouchMoved(touch, event)
    	local location = touch:getLocation()

    	if curMode == ScaleMode.AxisX then
    		local diffx = location.x - beginPos.x
    		local scaleRatio = diffx / self.tipSize.width + 1
    		local newScaleX = self.oldScaleX * scaleRatio
    		self.targetNode:setScaleX(newScaleX)
    	elseif curMode == ScaleMode.AxisY then
    		local diffy = location.y - beginPos.y
    		local scaleRatio = diffy / self.tipSize.height + 1
    		local newScaleY = self.oldScaleY * scaleRatio
    		self.targetNode:setScaleY(newScaleY)
    	elseif curMode == ScaleMode.AxisBoth then
            local diffy = location.y - beginPos.y
            local diffx = location.x - beginPos.x
            local diff = math.max(diffx, diffy)
            local scaleRatio = diff / self.tipSize.height + 1
            local newScale = self.oldScale * scaleRatio
            self.targetNode:setScale(newScale)
    	end
    end

    local function onTouchEnded(touch, event)
    	self.axisXLayer:setColor(cc.c3b(22, 200, 22))
    	self.axisYLayer:setColor(cc.c3b(200, 22, 22))

		self.oldScaleX = self.targetNode:getScaleX()
		self.oldScaleY = self.targetNode:getScaleY()
        self.oldScale = self.targetNode:getScale()
    end


    local  listenner = cc.EventListenerTouchOneByOne:create()
    listenner:setSwallowTouches(true)
    listenner:registerScriptHandler(onTouchBegan, cc.Handler.EVENT_TOUCH_BEGAN )
    listenner:registerScriptHandler(onTouchMoved, cc.Handler.EVENT_TOUCH_MOVED )
    listenner:registerScriptHandler(onTouchEnded, cc.Handler.EVENT_TOUCH_ENDED )

    local eventDispatcher = self:getEventDispatcher()
    eventDispatcher:addEventListenerWithSceneGraphPriority(listenner, self)
end


return ToolLayerScale
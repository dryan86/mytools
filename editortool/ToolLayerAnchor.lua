local ToolLayerAnchor = class("ToolLayerAnchor", function(params)
    local layer = cc.Node:create()
    -- local layer = cc.LayerColor:create(cc.c3b(22, 22, 22))

    return layer
end)


function ToolLayerAnchor:ctor(params)
	self.targetNode = params.target
	self.oldAnchor = self.targetNode:getAnchorPoint()
	local targetSize = self.targetNode:getContentSize()
	self.oldAnchorPos = cc.p(self.oldAnchor.x * targetSize.width, self.oldAnchor.y * targetSize.height)
    self:setPosition(self.oldAnchorPos)

	local tipSize = {width = 80, height = 80}
	self.tipSize = tipSize
	local anchorSize = cc.size(5, 5)
	self.anchorSize = anchorSize

	local tipLayer = cc.LayerColor:create(cc.c3b(22, 22, 22))
	self.tipLayer = tipLayer
	tipLayer:setContentSize(tipSize)
	tipLayer:setOpacity(120)
	tipLayer:setIgnoreAnchorPointForPosition(false)
	self:addChild(tipLayer)

	local anchorLayer = cc.LayerColor:create(cc.c3b(255, 0, 0))
	anchorLayer:setContentSize(anchorSize)
	anchorLayer:setIgnoreAnchorPointForPosition(false)
	anchorLayer:setPosition(tipSize.width/2, tipSize.height/2)
	tipLayer:addChild(anchorLayer)

	-- registerTouch
	self:registerTouch()
end

function ToolLayerAnchor:convertPosToAnchor(pos)
	local targetSize = self.targetNode:getContentSize()

	local anchorPoint = cc.p(pos.x / targetSize.width, pos.y / targetSize.height)
	return anchorPoint
end

function ToolLayerAnchor:registerTouch()
	local beginPos = nil

    local function onTouchBegan(touch, event)
        local location = touch:getLocation()
        local uiPos = self.tipLayer:convertToNodeSpace(location)

        if uiPos.x < self.tipSize.width and uiPos.x > 0 and uiPos.y < self.tipSize.height and uiPos.y > 0 then
        	self.tipLayer:setColor(cc.c3b(52, 52, 52))
            beginPos = self:convertToNodeSpace(location)

        	return true
        end

        self.tipLayer:setColor(cc.c3b(22, 22, 22))

        return false
    end

    local function onTouchMoved(touch, event)
        local location = touch:getLocation()

        local newPos = self:convertToNodeSpace(location)
        local diffpos = cc.pSub(newPos, beginPos)

        local newPos = cc.pAdd(diffpos, self.oldAnchorPos)
        self:setPosition(newPos)
        self.oldAnchorPos = newPos
    end

    local function onTouchEnded(touch, event)
    	self.tipLayer:setColor(cc.c3b(22, 22, 22))

        local anchor = self:convertPosToAnchor(self.oldAnchorPos)
        dump(anchor)
        self.targetNode:setAnchorPoint(anchor)
    end

    local  listenner = cc.EventListenerTouchOneByOne:create()
    listenner:setSwallowTouches(true)
    listenner:registerScriptHandler(onTouchBegan, cc.Handler.EVENT_TOUCH_BEGAN )
    listenner:registerScriptHandler(onTouchMoved, cc.Handler.EVENT_TOUCH_MOVED )
    listenner:registerScriptHandler(onTouchEnded, cc.Handler.EVENT_TOUCH_ENDED )

    local eventDispatcher = self:getEventDispatcher()
    eventDispatcher:addEventListenerWithSceneGraphPriority(listenner, self)
end


return ToolLayerAnchor
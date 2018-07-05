local ToolLayerMove = class("ToolLayerMove", function(params)
    local layer = cc.Node:create()
	-- local layer = cc.LayerColor:create(cc.c3b(22, 22, 22))
    return layer
end)


function ToolLayerMove:ctor(params)
	-- 操作的目标
	self.targetNode = params.target
	local tmpx, tmpy = params.target:getPosition()
	self.oldPos = cc.p(tmpx, tmpy)

	local tipSize = {width = 80, height = 80}
	self.tipSize = tipSize
	local tipLayer = cc.LayerColor:create(cc.c3b(22, 22, 22))
	self.tipLayer = tipLayer
	tipLayer:setContentSize(tipSize)
    tipLayer:setIgnoreAnchorPointForPosition(false)
	tipLayer:setOpacity(120)
    self:setRotation(-self.targetNode:getRotation())
    -- 根据anchor设置位置
    local targetSize = self.targetNode:getContentSize()
    local anchorPoint = self.targetNode:getAnchorPoint()
    local tipPos = cc.p(anchorPoint.x * targetSize.width, anchorPoint.y * targetSize.height)
    self:setPosition(tipPos)

	local tipSprite = cc.Sprite:create("editor/transform-move.png")
	tipSprite:setPosition(tipSize.width/2, tipSize.height/2)
	tipLayer:addChild(tipSprite)

	self:addChild(tipLayer)

	-- registerTouch
	self:registerTouch()
end

function ToolLayerMove:registerTouch()
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

        local newPos = cc.pAdd(diffpos, self.oldPos)
        self.targetNode:setPosition(newPos)
        self.oldPos = newPos
    end

    local function onTouchEnded(touch, event)
    	self.tipLayer:setColor(cc.c3b(22, 22, 22))

		local tmpx, tmpy = self.targetNode:getPosition()
		self.oldPos = cc.p(tmpx, tmpy)
    end


    local  listenner = cc.EventListenerTouchOneByOne:create()
    listenner:setSwallowTouches(true)
    listenner:registerScriptHandler(onTouchBegan, cc.Handler.EVENT_TOUCH_BEGAN )
    listenner:registerScriptHandler(onTouchMoved, cc.Handler.EVENT_TOUCH_MOVED )
    listenner:registerScriptHandler(onTouchEnded, cc.Handler.EVENT_TOUCH_ENDED )

    local eventDispatcher = self:getEventDispatcher()
    eventDispatcher:addEventListenerWithSceneGraphPriority(listenner, self)
end



return ToolLayerMove
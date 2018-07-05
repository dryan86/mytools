local EditMode = {
    None = 0,
    Move = 1,
    Scale = 2,
    Rotate = 3,
    Anchor = 4
}


local EditLayer = class("EditLayer", function(params)
    local layer = cc.Layer:create()

    if params.target then
        params.target:addChild(layer)
    end

    return layer
end)

-- params:
--  parent 编辑工具附着的层
-- 	target 编辑的目标
--  callback 退出编辑状态的回调
--  toolPos 工具栏的显示位置
function EditLayer:ctor(params)
	-- body
    self.parent = params.parent
	self.targetNode = params.target
    self.callback = params.callback
    self.toolPos = params.toolPos

	-- drawNode
	self.drawNode = cc.DrawNode:create()
	self:addChild(self.drawNode)


	self:performWithDelay(function()
		self:refreshBoundingBox()

        local bbox = self.targetNode:getContentSize()
        local anchor = self.targetNode:getAnchorPoint()

        self:setPosition(bbox.width * anchor.x, bbox.height * anchor.y)

		-- toolbar Node
		self.toolbarNode = cc.Node:create()
		self.toolbarNode:setPosition(self.toolPos)
		self.parent:addChild(self.toolbarNode)
		self:showToolbar()
	end, 0.01)
end

function EditLayer:performWithDelay(callback, delay)
    local delay = cc.DelayTime:create(delay)
    local sequence = cc.Sequence:create(delay, cc.CallFunc:create(callback))
    self:runAction(sequence)
    return sequence
end

function EditLayer:showToolbar()
	local pitch = 60
    self.toolbarNode.pitch = pitch

    local modeBgSprite = cc.Sprite:create("editor/transform-bg.png")
    self.toolbarNode.modeBgSprite = modeBgSprite
    modeBgSprite:setScale(1.2)
    self.toolbarNode:addChild(modeBgSprite)

	-- moveTool
    local moveTool = ccui.Button:create("editor/transform-move.png", "editor/transform-move.png")
    moveTool:setScale(1.2)
    moveTool:setPosition(cc.p(0, pitch * 0))
    moveTool:addClickEventListener(function(sender)
        modeBgSprite:setPosition(cc.p(0, pitch * 0))
        self:changeMode(EditMode.Move)
    end)
    self.toolbarNode:addChild(moveTool)

    -- scaleTool
    local scaleTool = ccui.Button:create("editor/transform-scale.png", "editor/transform-scale.png")
    scaleTool:setScale(1.2)
    scaleTool:setPosition(cc.p(0, -pitch * 1))
    scaleTool:addClickEventListener(function(sender)
        modeBgSprite:setPosition(cc.p(0, -pitch * 1))
        self:changeMode(EditMode.Scale)
    end)
    self.toolbarNode:addChild(scaleTool)

    -- rotateTool
    local rotateTool = ccui.Button:create("editor/transform-rotate.png", "editor/transform-rotate.png")
    rotateTool:setScale(1.2)
    rotateTool:setPosition(cc.p(0, -pitch * 2))
    rotateTool:addClickEventListener(function(sender)
        modeBgSprite:setPosition(cc.p(0, -pitch * 2))
        self:changeMode(EditMode.Rotate)
    end)
    self.toolbarNode:addChild(rotateTool)

    -- anchorTool
    local anchorTool = ccui.Button:create("editor/transform-anchor.png", "editor/transform-anchor.png")
    anchorTool:setScale(1.2)
    anchorTool:setPosition(cc.p(0, -pitch * 3))
    anchorTool:addClickEventListener(function(sender)
        modeBgSprite:setPosition(cc.p(0, -pitch * 3))
        self:changeMode(EditMode.Anchor)
    end)
    self.toolbarNode:addChild(anchorTool)

    -- exitTool
    -- local exitTool = ccui.Button:create("editor/transform-move.png", "editor/transform-move.png")
    -- exitTool:setScale(1.2)
    -- exitTool:setPosition(cc.p(0, -pitch * 4))
    -- exitTool:addClickEventListener(function(sender)
    --     if self.callback ~= nil then
    --         self.callback()
    --     end

    --     modeBgSprite:setPosition(cc.p(0, -pitch * 4))

    --     self:exit()
    -- end)
    -- self.toolbarNode:addChild(exitTool)

    -- 默认为移动模式
    self:changeMode(EditMode.Move)
end

function EditLayer:changeMode(newMode)
    if self.toolLayer ~= nil then
        self.toolLayer:removeFromParent()
        self.toolLayer = nil
    end

    if newMode == EditMode.Move then
        self.toolbarNode.modeBgSprite:setPosition(cc.p(0, self.toolbarNode.pitch * 0))
        self.toolLayer = require("tools.ToolLayerMove"):create({target = self.targetNode})
        self.targetNode:addChild(self.toolLayer)
    elseif newMode == EditMode.Scale then
        self.toolbarNode.modeBgSprite:setPosition(cc.p(0, -self.toolbarNode.pitch * 1))
        self.toolLayer = require("tools.ToolLayerScale"):create({target = self.targetNode})
        self.targetNode:addChild(self.toolLayer)
    elseif newMode == EditMode.Rotate then
        self.toolbarNode.modeBgSprite:setPosition(cc.p(0, -self.toolbarNode.pitch * 2))
        self.toolLayer = require("tools.ToolLayerRotate"):create({target = self.targetNode})
        self.targetNode:addChild(self.toolLayer)
    elseif newMode == EditMode.Anchor then
        self.toolbarNode.modeBgSprite:setPosition(cc.p(0, -self.toolbarNode.pitch * 3))
        self.toolLayer = require("tools.ToolLayerAnchor"):create({target = self.targetNode})
        self.targetNode:addChild(self.toolLayer)
    end
end

function EditLayer:exit()
    self.toolLayer:removeFromParent()
    self.toolLayer = nil

    self.toolbarNode:removeFromParent()
    self:removeFromParent()
end

function EditLayer:refreshBoundingBox()
	-- body
	local bbox = self.targetNode:getContentSize()
    dump(bbox)
    --draw a rectangle
    local anchorPoint = self.targetNode:getAnchorPoint()
    local x = -bbox.width * anchorPoint.x 
    local y = -bbox.height * anchorPoint.y
    local w = bbox.width * (1 - anchorPoint.x)
    local h = bbox.height * (1 - anchorPoint.y)
    self.drawNode:clear()
    self.drawNode:drawRect(cc.p(x, y), cc.p(w, h), cc.c4f(1,1,0,1))
end

return EditLayer
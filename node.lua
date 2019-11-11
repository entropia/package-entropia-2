gl.setup(NATIVE_WIDTH, NATIVE_HEIGHT)
local json = require "json"
local st = util.screen_transform(0)

local on = true

--
-- watch the json files
--
util.json_watch("config.json", function(cfg)
    metadata = cfg.__metadata
    st = util.screen_transform(cfg.rotation)
    font = resource.load_font(cfg.font)
    bg_color = cfg.bg_color
end)


util.data_mapper{
    push = function(data)
        local payload = json.decode(data)
        text = payload.text
        buttons = payload.buttons
    end;

    toggle = function(status)
        on = status == "on"
    end;
}

function content()
  font:write(20, 20, "Hello World", 100, 1,1,1,1)
end

function node.render()
  gl.clear(bg_color.r, bg_color.g, bg_color.b, bg_color.a)
  st()
  if on then
    content()
  end
end

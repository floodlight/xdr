function MockReader(data)
    local i = 1
    local self = {}

    function self.int()
        assert(type(data[i]) == "number")
        x = data[i]
        i = i + 1
        return x
    end

    self.uint = self.int

    function self.fstring()
        assert(type(data[i]) == "string")
        x = data[i]
        i = i + 1
        return x
    end

    return self
end

function MockWriter(data)
    local i = 1
    local self = {}

    local function check(x)
        assert(data[i] == x, string.format("i=%d: expected %s %q, got %s %q", i, type(data[i]), tostring(data[i]), type(x), tostring(x)))
        i = i + 1
    end

    self.int = check
    self.uint = check
    self.fstring = check

    return self
end

function runtest()
    xdr = require("xdr/xdr")
    local raw = require("raw")
    local x = require("expected")
    xdr.write_root(MockWriter(raw), x)
    local y = xdr.read_root(MockReader(raw))
    xdr.write_root(MockWriter(raw), y)
end

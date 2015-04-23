local public = {}

local function read_int(reader)
    return reader.int()
end

local function write_int(writer, x)
    writer.int(x)
end

local function read_uint(reader)
    return reader.uint()
end

local function write_uint(writer, x)
    writer.uint(x)
end

local function read_bool(reader)
    return reader.uint() ~= 0
end

local function write_bool(writer, x)
    writer.uint(x and 1 or 0)
end

local function read_optional(reader, fn)
    if read_bool(reader) then
        return fn(reader)
    else
        return nil
    end
end

local function write_optional(writer, x, fn)
    if x ~= nil then
        writer.int(1)
        fn(writer, x)
    else
        writer.int(0)
    end
end

local function read_array(reader, fn, count)
    local t = {}
    for i = 1, count do
        table.insert(t, fn(reader))
    end
    return t
end

local function write_array(writer, x, fn, count)
    assert(#x == count)
    for i, v in ipairs(x) do
        fn(writer, v)
    end
end

local function read_list(reader, fn, max)
    local count = reader.uint()
    assert(max == nil or count <= max)
    return read_array(reader, fn, count)
end

local function write_list(writer, x, fn, max)
    local count = #x
    assert(max == nil or count <= max)
    writer.uint(count)
    write_array(writer, x, fn, count)
end

local function read_fstring(reader, count)
    return reader.fstring(count)
end

local function write_fstring(writer, x, count)
    assert(#x == count)
    writer.fstring(x)
end

local function read_string(reader, max)
    local count = reader.uint()
    assert(max == nil or count <= max)
    return reader.fstring(count)
end

local function write_string(writer, x, max)
    local count = #x
    assert(max == nil or count <= max)
    writer.uint(count)
    writer.fstring(x)
end

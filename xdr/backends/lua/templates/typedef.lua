function public.read_${typedef.declaration.name}(reader)
    local obj
:: include("_unpack.lua", m=typedef.declaration, dst="obj")
    return obj
end

function public.write_${typedef.declaration.name}(writer, obj)
:: include("_pack.lua", m=typedef.declaration, src="obj")
end

function public.read_${struct.name}(reader)
    local obj = {}
:: for m in struct.members:
:: include("_unpack.lua", m=m, dst="obj." + m.name)
:: #endfor
    return obj
end

function public.write_${struct.name}(writer, obj)
:: for m in struct.members:
:: include("_pack.lua", m=m, src="obj." + m.name)
:: #endfor
end

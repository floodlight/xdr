:: from xdr.backends.lua.pack import literal
function public.read_${union.name}(reader)
    local discriminant = reader.int()
:: for m in union.members:
    if discriminant == ${literal(m.case, constants)} then
        return public.read_${union.name}_${m.declaration.name}(reader)
    end
:: #endfor
end

function public.write_${union.name}(writer, obj)
    local discriminant = obj.${union.discriminant.name}
:: for m in union.members:
    if discriminant == ${literal(m.case, constants)} then
        return public.write_${union.name}_${m.declaration.name}(writer, obj)
    end
:: #endfor
end

:: for m in union.members:
function public.read_${union.name}_${m.declaration.name}(reader)
    local obj = { ${union.discriminant.name}=${literal(m.case, constants)} }
:: include("_unpack.lua", m=m.declaration, dst="obj.value")
    return obj
end
:: #endfor

:: for m in union.members:
function public.write_${union.name}_${m.declaration.name}(writer, obj)
    writer.int(obj.${union.discriminant.name})
:: include("_pack.lua", m=m.declaration, src="obj.value")
    return obj
end
:: #endfor

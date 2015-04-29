public.${enum.name} = {}
:: for m in enum.members:
public.${enum.name}.${m.name} = ${m.value}
:: #endfor
public.read_${enum.name} = read_int
public.write_${enum.name} = write_int

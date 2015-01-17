class ${enum.name}(XDREnum):
    members = {}

:: for m in enum.members:
${enum.name}.${m.name} = ${enum.name}(${repr(enum.name + '.' + m.name)}, ${m.value})
${enum.name}.members[${m.value}] = ${enum.name}.${m.name}
:: #endfor

from pathlib import Path

p=Path("configs/building_forms.toml")

print(p,type(p))
sting=str(p)
print(sting,type(sting))
print(sting.split(".",1))
k,v=sting.split(".",1)
print(k,v)
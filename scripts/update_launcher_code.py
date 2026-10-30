import os

launcher_dir = r"c:\Users\ZETICUZ\Documents\artcraft\repos\craft-launcher"

# 1. Update Cargo.toml
root_cargo = os.path.join(launcher_dir, "Cargo.toml")
with open(root_cargo, "r", encoding="utf-8") as f:
    c = f.read()
c = c.replace('repository = "https://github.com/storytold/craft-launcher"', 'repository = "https://github.com/ZETIC7Z/craft-launcher"')
with open(root_cargo, "w", encoding="utf-8") as f:
    f.write(c)

# 2. Update catalog.rs
cat_path = os.path.join(launcher_dir, "crates", "core", "src", "catalog.rs")
with open(cat_path, "r", encoding="utf-8") as f:
    cat = f.read()
cat = cat.replace('publisher: "ArtCraft"', 'publisher: "ZETICA"')
cat = cat.replace('"https://getartcraft.com/apps/{}"', '"https://zetica.xyz/apps/{}"')
cat = cat.replace('"storytold/effectcraft"', '"ZETIC7Z/effectcraft"')
with open(cat_path, "w", encoding="utf-8") as f:
    f.write(cat)

# 3. Update apps/artcraft-launcher/Cargo.toml
app_cargo = os.path.join(launcher_dir, "apps", "artcraft-launcher", "Cargo.toml")
with open(app_cargo, "r", encoding="utf-8") as f:
    ac = f.read()
ac = ac.replace('description = "ArtCraft Launcher: install, update and open the Craft App Suite"', 'description = "Zetica Hub: install, update and open the Zetica Creative Suite"')
with open(app_cargo, "w", encoding="utf-8") as f:
    f.write(ac)

print("Launcher code and cargo configuration updated successfully!")

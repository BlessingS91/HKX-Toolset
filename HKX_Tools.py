import os


def duplicate_attacks(file_path, log):

    folder_path = os.path.dirname(file_path)
    file_name = os.path.basename(file_path)

    files_to_duplicate = [file_path]

    # Automatically include matching power attack
    if "attack" in file_name.lower() and "powerattack" not in file_name.lower():

        power_name = file_name.replace("Attack", "PowerAttack")

        power_path = os.path.join(folder_path, power_name)

        if os.path.exists(power_path):

            files_to_duplicate.append(power_path)

            log(f"Found matching power attack: {power_name}")

    created = 0

    for current_file in files_to_duplicate:

        with open(current_file, "rb") as original:

            data = original.read()

        name = os.path.basename(current_file)

        base_name, ext = os.path.splitext(name)

        base_name = base_name.rstrip("0123456789")

        for i in range(1, 11):

            new_name = f"{base_name}{i}{ext}"

            new_path = os.path.join(folder_path, new_name)

            with open(new_path, "wb") as new_file:

                new_file.write(data)

            created += 1

            log(f"Created: {new_name}")

    return {"success": True, "message": f"Duplicated {created} file(s)."}


def rename_attack_to_power(folder_path, log):

    renamed = 0

    log(f"Scanning folder: {folder_path}")

    for file_name in os.listdir(folder_path):

        if not file_name.lower().endswith(".hkx"):
            continue

        lower = file_name.lower()

        if "powerattack" in lower:
            continue

        new_name = None

        if lower.startswith("mco_attack"):

            new_name = "mco_powerattack" + file_name[len("mco_attack") :]

        elif lower.startswith("bfco_attack"):

            new_name = "bfco_powerattack" + file_name[len("bfco_attack") :]

        if new_name:

            old_path = os.path.join(folder_path, file_name)

            new_path = os.path.join(folder_path, new_name)

            if not os.path.exists(new_path):

                os.rename(old_path, new_path)

                renamed += 1

                log(f"Renamed: {file_name} -> {new_name}")

    return {
        "success": True,
        "message": f"Renamed {renamed} attack file(s) to power attacks.",
    }


def rename_power_to_attack(folder_path, log):

    renamed = 0

    log(f"Scanning folder: {folder_path}")

    for file_name in os.listdir(folder_path):

        if not file_name.lower().endswith(".hkx"):
            continue

        lower = file_name.lower()

        if "powerattack" not in lower:
            continue

        new_name = None

        if lower.startswith("mco_powerattack"):

            new_name = "mco_attack" + file_name[len("mco_powerattack") :]

        elif lower.startswith("bfco_powerattack"):

            new_name = "bfco_attack" + file_name[len("bfco_powerattack") :]

        if new_name:

            old_path = os.path.join(folder_path, file_name)

            new_path = os.path.join(folder_path, new_name)

            if not os.path.exists(new_path):

                os.rename(old_path, new_path)

                renamed += 1

                log(f"Renamed: {file_name} -> {new_name}")

    return {
        "success": True,
        "message": f"Renamed {renamed} power attack file(s) to normal attacks.",
    }

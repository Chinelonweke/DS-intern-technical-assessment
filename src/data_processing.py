# create function extract_data

import re
from datetime import datetime
from classes import OwnerInfo, Inventory

def extract_data(aligned_content):
    # Extract owner information
    owner_name = ""
    owner_address = ""
    owner_telephone = ""
    inventory_items = []
    owner_found = False

    for idx, line in enumerate(aligned_content):
        # Look for owner name
        if "HOME INVENTORY" in line and idx + 1 < len(aligned_content):
            owner_name = aligned_content[idx + 1]
            owner_address = aligned_content[idx + 2]
            # City, Zip and Address combined
            city_zip = aligned_content[idx + 3]
            if city_zip:
                owner_address += ", " + city_zip
            owner_telephone = aligned_content[idx + 4]
            owner_found = True
            break

    # After owner found, go back to parse inventory
    for line in aligned_content:
        # Look for lines that match inventory pattern
        match = re.match(r'^\d+\s+([A-Za-z\s]+)\s+([A-Za-z\s]+)\s+([A-Za-z\s]+)\s+([A-Za-z\s]+)\s+(\d{2}/\d{2}/\d{4})\s+([A-Za-z]+)\s+(\w+)\s+([\d,]+\.\d{2})\$', line)
        if match:
            area = match.group(1).strip()
            item = match.group(2).strip()
            description = match.group(3).strip()
            source = match.group(4).strip()
            purchase_date_raw = match.group(5).strip()
            style = match.group(6).strip()
            serial_number = match.group(7).strip()
            value_raw = match.group(8).strip()

            # Process date into ISO format
            purchase_date_obj = datetime.strptime(purchase_date_raw, "%d/%m/%Y")
            purchase_date_iso = purchase_date_obj.strftime("%Y-%m-%dT%H:%M:%S")

            # Process value into float
            value_clean = float(value_raw.replace(",", ""))

            # Create source_style_area field
            source_style_area = f"{area} - {source} - {style}"

            inventory = Inventory(
                purchase_date=purchase_date_iso,
                serial_number=serial_number,
                description=item,
                source_style_area=source_style_area,
                value=value_clean
            )

            inventory_items.append(inventory)

    # Create OwnerInfo object
    owner = OwnerInfo(
        owner_name=owner_name,
        owner_address=owner_address,
        owner_telephone=owner_telephone
    )

    # Build final response
    response = {
        "owner_name": owner.owner_name,
        "owner_address": owner.owner_address,
        "owner_telephone": owner.owner_telephone,
        "data": []
    }

    for inv in inventory_items:
        response["data"].append({
            "purchase_date": inv.purchase_date,
            "serial_number": inv.serial_number,
            "description": inv.description,
            "source_style_area": inv.source_style_area,
            "value": inv.value
        })

    return response
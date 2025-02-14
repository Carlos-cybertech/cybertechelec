from flask import request


def objects_to_dict(the_object):
    return {
        "id": the_object.id,
        "p_type": the_object.p_type,
        "po_number": the_object.po_number,
        "address": the_object.address,
        "num_chargers": the_object.num_chargers,
        "project_status": the_object.project_status,
        "invoice": the_object.invoice,
        "datto": the_object.datto
    }


def extract_form_data():
    return {
        # Related to Project table
        "p_type": request.form.get("p_type"),
        "po_number": request.form.get("po_number"),
        "address": request.form.get("address"),
        "num_chargers": request.form.get("num_chargers"),
        "permit_num1": request.form.get("permit_num1"),
        "permit_num2": request.form.get("permit_num2"),
        "project_status": request.form.get("project_status"),
        "start_date": request.form.get("start_date"),
        "invoice": request.form.get("invoice"),
        "datto": request.form.get("datto"),
        "notes": request.form.get("notes"),
        "equipment_notes": request.form.get("equipment_notes"),
        # Related to Inspection table
        "i_type1": request.form.get("i_type1"),
        "inspection_date1": request.form.get("inspection_date1"),
        "inspection_status1": request.form.get("inspection_status1"),
        "i_type2": request.form.get("i_type2"),
        "inspection_date2": request.form.get("inspection_date2"),
        "inspection_status2": request.form.get("inspection_status2"),
        "i_type3": request.form.get("i_type3"),
        "inspection_date3": request.form.get("inspection_date3"),
        "inspection_status3": request.form.get("inspection_status3")
    }


def validate_form_data(form_data):
    if not form_data["po_number"]:
        return "Purchase order number is required"
    if not form_data["address"]:
        return "Address is required"
    if not form_data["num_chargers"]:
        return "Number of chargers is required"
    if not form_data["project_status"]:
        return "Project status is required"
    if not form_data["start_date"]:
        return "Project Start Date is required"
    if not form_data["p_type"]:
        return "Project type is required"
    if not form_data["invoice"]:
        return "Invoice is required"
    if not form_data["datto"]:
        return "Uploaded to datto is required"
    return None


def clean_form_data(form_data):
    form_data["po_number"] = form_data["po_number"].strip() if form_data["po_number"] else None
    form_data["address"] = form_data["address"].strip() if form_data["address"] else None
    form_data["notes"] = form_data["notes"].strip() if form_data["notes"] else None
    form_data["equipment_notes"] = form_data["equipment_notes"].strip() if form_data["equipment_notes"] else None
    form_data["permit_num1"] = form_data["permit_num1"].strip() if form_data["permit_num1"] else None
    form_data["permit_num2"] = form_data["permit_num2"].strip() if form_data["permit_num2"] else None
    form_data["i_type1"] = form_data["i_type1"] if form_data["i_type1"] else None
    form_data["inspection_status1"] = form_data["inspection_status1"] if form_data["inspection_status1"] else None
    form_data["inspection_date1"] = form_data["inspection_date1"] if form_data["inspection_date1"] else None
    form_data["i_type2"] = form_data["i_type2"] if form_data["i_type2"] else None
    form_data["inspection_status2"] = form_data["inspection_status2"] if form_data["inspection_status2"] else None
    form_data["inspection_date2"] = form_data["inspection_date2"] if form_data["inspection_date2"] else None
    form_data["i_type3"] = form_data["i_type3"] if form_data["i_type3"] else None
    form_data["inspection_status3"] = form_data["inspection_status3"] if form_data["inspection_status3"] else None
    form_data["inspection_date3"] = form_data["inspection_date3"] if form_data["inspection_date3"] else None
    return form_data

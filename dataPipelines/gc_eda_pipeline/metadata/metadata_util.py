

def format_supplementary_data(json_info, date_fields_l):
    if isinstance(json_info, dict):
        for key in list(json_info.keys()):
            result_date = json_info[key]
            if isinstance(json_info[key], list):
                append = "_eda_ext_n"
            elif isinstance(json_info[key], dict):
                append = "_eda_ext_n"
            else:
                key_lower = key.lower()
                val = json_info[key]
                if key_lower in date_fields_l and val is not None:
                    append = "_eda_ext_dt"
                    result_date = val
                else:
                    append = "_eda_ext"
                    result_date = val
                    if key_lower in date_fields_l and val is not None:
                        append = "_eda_ext_dt"
                        result_date = val
            key_lower = key.lower() + append
            json_info[key_lower] = result_date
            del json_info[key]
            format_supplementary_data(json_info[key_lower], date_fields_l)

    elif isinstance(json_info, list):
        for item in json_info:
            format_supplementary_data(item, date_fields_l)


def mod_identifier(filename: str) -> str:
    acomod = None
    pcomod = None
    parsed = filename.split('-')
    if (len(parsed) - 1) == 9:
        contract = parsed[2]
        ordernum = parsed[3]
        acomod = parsed[4]
        pcomod = parsed[5]
    elif (len(parsed) - 1) == 10:
        contract = parsed[3]
        ordernum = parsed[4]
        acomod = parsed[5]
        pcomod = parsed[6]
    elif (len(parsed) - 1) == 11:
        contract = parsed[4]
        ordernum = parsed[5]
        acomod = parsed[6]
        pcomod = parsed[7]
    elif (len(parsed) - 1) == 12:
        contract = parsed[5]
        ordernum = parsed[6]
        acomod = parsed[7]
        pcomod = parsed[8]
    elif (len(parsed) - 1) == 13:
        contract = parsed[6]
        ordernum = parsed[7]
        acomod = parsed[8]
        pcomod = parsed[9]

    if acomod == "empty" and pcomod == "empty":
        return "base_award"
    else:
        return ""


def title(filename: str) -> str:
    parsed = filename.split('-')

    if (len(parsed) - 1) == 9:
        contract = parsed[2]
        ordernum = parsed[3]
        acomod = parsed[4]
        pcomod = parsed[5]
        if pcomod == 'empty':
            modification = acomod
        else:
            modification = pcomod
    elif (len(parsed) - 1) == 10:
        contract = parsed[3]
        ordernum = parsed[4]
        acomod = parsed[5]
        pcomod = parsed[6]
        if pcomod == 'empty':
            modification = acomod
        else:
            modification = pcomod
    elif (len(parsed) - 1) == 11:
        contract = parsed[4]
        ordernum = parsed[5]
        acomod = parsed[6]
        pcomod = parsed[7]
        if pcomod == 'empty':
            modification = acomod
        else:
            modification = pcomod
    elif (len(parsed) - 1) == 12:
        contract = parsed[5]
        ordernum = parsed[6]
        acomod = parsed[7]
        pcomod = parsed[8]
        if pcomod == 'empty':
            modification = acomod
        else:
            modification = pcomod
    elif (len(parsed) - 1) == 13:
        contract = parsed[6]
        ordernum = parsed[7]
        acomod = parsed[8]
        pcomod = parsed[9]
        if pcomod == 'empty':
            modification = acomod
        else:
            modification = pcomod
    else:
        return "NA"

    return contract + "-" + ordernum + "-" + modification


def extract_fpds_ng_quey_values(filename: str) -> (str, str, str):
    parsed = filename.split('-')
    if (len(parsed) - 1) == 9:
        contract = parsed[2]
        ordernum = parsed[3]
        acomod = parsed[4]
        pcomod = parsed[5]
        if pcomod == 'empty':
            modification = acomod
        else:
            modification = pcomod
    elif (len(parsed) - 1) == 10:
        contract = parsed[3]
        ordernum = parsed[4]
        acomod = parsed[5]
        pcomod = parsed[6]
        if pcomod == 'empty':
            modification = acomod
        else:
            modification = pcomod
    elif (len(parsed) - 1) == 11:
        contract = parsed[4]
        ordernum = parsed[5]
        acomod = parsed[6]
        pcomod = parsed[7]
        if pcomod == 'empty':
            modification = acomod
        else:
            modification = pcomod
    elif (len(parsed) - 1) == 12:
        contract = parsed[5]
        ordernum = parsed[6]
        acomod = parsed[7]
        pcomod = parsed[8]
        if pcomod == 'empty':
            modification = acomod
        else:
            modification = pcomod
    elif (len(parsed) - 1) == 13:
        contract = parsed[6]
        ordernum = parsed[7]
        acomod = parsed[8]
        pcomod = parsed[9]
        if pcomod == 'empty':
            modification = acomod
        else:
            modification = pcomod
    else:
        return None, None, None

    # idv_piid <-- contract
    # piid <-- ordernum
    # modification_number <--modification
    idv_piid = contract
    piid = ordernum
    modification_number = modification
    return idv_piid, piid, modification_number


if __name__ == "__main__":
    test = "EDAPDF-057e78b7-8285-4171-8863-0172862d2db1-GS21F0015X-47QDCC21M6TLZ-empty-empty-PDS-2021-03-08.pdf"
    # test = "EDAPDF-5A1008FA3B0B148EE05400215A9BA3BA-HQ003414D0003-HQ003417F0296-empty-P00001-PDS-2017-09-25.pdf"
    (idv_piid, piid, modification_number) = extract_fpds_ng_quey_values(test)

    print(f"idv_piid: {idv_piid}, piid: {piid} modification_number: {modification_number}" )

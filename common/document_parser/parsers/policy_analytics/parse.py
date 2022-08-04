import os
from common.document_parser.lib import (
    pages,
    paragraphs,
    entities,
    topics,
    ref_list,
    abbreviations,
    summary,
    keywords,
    text_length,
    read_meta,
    pdf_reader,
    write_doc_dict_to_json,
    ocr,
    file_utils,
)
from . import init_doc
from common.document_parser.lib.ml_features import (
    add_pagerank_r, add_popscore_r)
from gamechangerml.src.utilities.text_utils import utf8_pass, clean_text


def parse(
    f_name,
    meta_data=None,
    ocr_missing_doc=False,
    num_ocr_threads=2,
    force_ocr=False,
    out_dir="./",
):
    print("running policy_analyics.parse on", f_name)
    try:
        meta_dict = read_meta.read_metadata(meta_data)
        doc_dict = init_doc.create_doc_dict_with_meta(meta_dict)

        init_doc.assign_f_name_fields(f_name, doc_dict)
        init_doc.assign_other_fields(doc_dict)
        should_delete = False
        if ocr_missing_doc or force_ocr:
            f_name = ocr.get_ocr_filename(f_name, num_ocr_threads, force_ocr)
        if not str(f_name).endswith(".pdf"):
            f_name = file_utils.coerce_file_to_pdf(f_name)
            should_delete = True
        funcs = [ref_list.add_ref_list, entities.extract_entities, topics.extract_topics, keywords.add_keyw_5, abbreviations.add_abbreviations_n, summary.add_summary, add_pagerank_r, add_popscore_r,
                 text_length.add_word_count]

        doc_obj = pdf_reader.get_fitz_doc_obj(f_name)
        pages.handle_pages(doc_obj, doc_dict)
        doc_obj.close()

        paragraphs.handle_paragraphs(doc_dict)

        for func in funcs:
            try:
                func(doc_dict)
            except Exception as e:
                print(e)
                print("Could not run %s on document dict" % func)
        # TODO: ADD DATES ?
        # doc_dict = dates.process(doc_dict)

        # TODO: post process is mostly unnecessary renaming etc that can be refactored into prior steps
        doc_dict = post_process(doc_dict)

        write_doc_dict_to_json.write(out_dir=out_dir, ex_dict=doc_dict)
    except Exception as e:
        print("ERROR in policy_analytics.parse:", e)
    finally:
        if should_delete:
            os.remove(f_name)


def post_process(doc_dict):
    doc_dict["raw_text"] = utf8_pass(doc_dict["text"])
    doc_dict["text"] = clean_text(doc_dict["text"])

    if doc_dict["meta_data"]:
        doc_dict["file_ext_s"] = doc_dict["meta_data"]["file_ext"]
        doc_dict["display_doc_type_s"] = doc_dict["meta_data"]["display_doc_type"]
        doc_dict["display_title_s"] = doc_dict["meta_data"]["display_title"]
        doc_dict["display_org_s"] = doc_dict["meta_data"]["display_org"]
        doc_dict["data_source_s"] = doc_dict["meta_data"]["data_source"]
        doc_dict["source_title_s"] = doc_dict["meta_data"]["source_title"]
        doc_dict["display_source_s"] = doc_dict["meta_data"]["display_source"]
        doc_dict["access_timestamp_dt"] = doc_dict["meta_data"]["access_timestamp"]
        doc_dict["publication_date_dt"] = doc_dict["meta_data"]["publication_date"]
        doc_dict["is_revoked_b"] = doc_dict["meta_data"]["is_revoked"]
    else:
        doc_dict["is_revoked_b"] = False

    to_rename = [
        ("txt_length", "text_length_r"),
        ("crawler_used", "crawler_used_s"),
        ("source_fqdn", "source_fqdn_s"),
        ("source_page_url", "source_page_url_s"),
        ("cac_login_required", "cac_login_required_b"),
        ("download_url", "download_url_s"),
        ("version_hash", "version_hash_s"),
    ]

    for current, needed in to_rename:
        try:
            doc_dict[needed] = doc_dict[current]
            del doc_dict[current]
        except KeyError:
            pass

    if doc_dict["meta_data"]:
        if "extensions" in doc_dict["meta_data"]:
            extensions = doc_dict["meta_data"]["extensions"]
            for key in extensions:
                doc_dict[key] = extensions[key]

    to_delete = [
        "meta_data",
        "access_timestamp",
        "publication_date",
        "crawler_used",
        "source_fqdn",
        "source_page_url",
        "cac_login_required",
        "download_url",
        "version_hash",
        "ingest_date",
        "orgs",
        "f_name"
    ]

    for key in to_delete:
        try:
            del doc_dict[key]
        except KeyError:
            pass

    return doc_dict
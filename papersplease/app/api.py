from flask import Blueprint, jsonify, request
from papersplease.app.common import DataSourceEnum, possible_data_source_values
from papersplease.app.fetch_data import XrxivDataSource

xrxiv_client_map = {
    DataSourceEnum.BIORXIV: XrxivDataSource(DataSourceEnum.BIORXIV),
    DataSourceEnum.MEDRXIV: XrxivDataSource(DataSourceEnum.MEDRXIV),
    DataSourceEnum.CHEMRXIV: XrxivDataSource(DataSourceEnum.CHEMRXIV),
}

paperscraper_bp = Blueprint('paperscraper', __name__)


@paperscraper_bp.route('/xrxiv_meta/<source>', methods=["POST"])
def get_scrapers(source: str):
    if not (source in possible_data_source_values):
        raise Exception("impossible source!")
    request_data = request.get_json()

    fetch_amount = request_data.get("fetch_amount", None)
    keywords = request_data.get("keywords", None)

    if (fetch_amount is None):
        raise Exception("expected fetch_amount:int parameter")
    if (keywords is None):
        raise Exception("expected keywords:str[] parameter")
    
    try:
        fetch_amount = int(fetch_amount)
    except Exception as e:
        raise Exception("expected fetch_amount:int parameter to be integer!")
    
    if not isinstance(keywords, list):
        raise Exception("expected keywords:str[] parameter to be string array!")
    if (len(keywords) == 0):
        raise Exception("expected keywords:str[] parameter to be contain at least one entry!")
    for keyword in keywords:
        if not isinstance(keyword, str):
            raise Exception("expected keywords:str[] parameter to be contain only string values!")
    
    data = xrxiv_client_map[source].get_documents_metadata(
        keywords=keywords,
        fetch_amount=fetch_amount
    )

    return jsonify([element.to_dict() for element in data])
from paperscraper.xrxiv.xrxiv_query import XRXivQuery
from papersplease.app.dump_manager import get_xrxiv_dump_path
from papersplease.app.common import DataSourceEnum

class XrxivMeta:
  def __init__(self, title: str, retrieval_url: str):
    self.title = title
    self.retrieval_url = retrieval_url

  def to_dict(self):
    return {
      'title': self.title,
      "retrieval_url": self.retrieval_url,
    }

class XrxivDataSource:
  def __init__(self, source: str):
    self.xrxiv_query_client = XRXivQuery(get_xrxiv_dump_path(source))
    self.source = source

  def get_retrieval_url(self, doi: str):
    return f"https://www.{self.source}.org/content/{doi}.full.pdf"
  
  def deserialize_meta(self, meta: dict):
    return XrxivMeta(
      title=meta['title'],
      retrieval_url=self.get_retrieval_url(doi=meta['doi'])
    )

  def get_documents_metadata(self, keywords: list[str], fetch_amount: int):
    xrxiv_articles_meta = self.xrxiv_query_client.search_keywords(keywords=keywords)

    parsed_xrxiv_articles_meta = xrxiv_articles_meta[['title', 'doi']]\
      .head(fetch_amount)\
      .to_dict(orient='records')
    
    return [self.deserialize_meta(meta=meta) for meta in parsed_xrxiv_articles_meta]


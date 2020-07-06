import cfscrape


class CfScraper(object):
    """ CloudFare Scraper """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scraper = cfscrape.create_scraper()

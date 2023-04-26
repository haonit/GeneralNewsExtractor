import re
from gne.utils import config
from lxml.html import HtmlElement
from gne.defaults import AUTHOR_PATTERN, AUTHOR_META


class AuthorExtractor:
    def __init__(self):
        self.author_pattern = AUTHOR_PATTERN

    def extract_from_user_xpath(self, author_xpath: str, element: HtmlElement) -> str:
        if author_xpath:
            publish_time = ''.join(element.xpath(author_xpath))
            return publish_time
        return ''

    def extract_from_meta(self, element: HtmlElement) -> str:
        """
        一些很规范的新闻网站，会把新闻的发布时间放在 META 中，因此应该优先检查 META 数据
        :param element: 网页源代码对应的Dom 树
        :return: str
        """
        for xpath in AUTHOR_META:
            author = element.xpath(xpath)
            if author:
                return ''.join(author)
        return ''

    def extract_from_text(self, element: HtmlElement) -> str:
        text = ''.join(element.xpath('.//text()'))
        for pattern in self.author_pattern:
            author_obj = re.search(pattern, text)
            if author_obj:
                return author_obj.group(1)
        return ''

    def extractor(self, element: HtmlElement, author_xpath=''):
        author_xpath = author_xpath or config.get('author', {}).get('xpath')
        author = (self.extract_from_user_xpath(author_xpath, element)  # 用户指定的 Xpath 是第一优先级
                  or self.extract_from_meta(element)  # 第二优先级从 Meta 中提取
                  or self.extract_from_text(element))  # 最坏的情况从正文中提取
        return author

from wiley_tdm import TDMClient
from collections import deque
import feedparser


# annotations = deque(maxlen=140)

# url = [
#     "https://onlinelibrary.wiley.com/feed/15213773/most-recent",
#     "https://pubs.acs.org/action/showFeed?type=axatoc&feed=rss&jc=chreay",
# ]

# keywords_annotation = [
#     "parahydrogen",
#     "PHIP",
#     "SABRE",
#     "hyperpolarization",
#     "hyperpolarized",
#     "para-hydrogen",
#     "hyperpolarized NMR",
#     "PHIP-SAH",
#     "LLS",
#     "NMR",
#     "p-H2",
#     "long-lived",
# ]

# keywords_title = [
#     "parahydrogen",
#     "PHIP",
#     "SABRE",
#     "hyperpolarization",
#     "hyperpolarized",
#     "p-H2",
# ]

# Angewandte_feed = feedparser.parse(url[1])


# def filter(text):
#     match_counter = 0
#     for keyword in keywords:
#         if keyword in text:
#             match_counter += 1
#     if match_counter > 1:
#         return True
#     return False


# # for entry in Angewandte_feed.entries:
# #     annotation = {}
# #     for content in entry.content:
# #         content_type = content.type
# #         content_value = content.value
# #         if content_type == "text/plain":
# #             if filter(content.value):
# #                 annotation["doi"] = entry.link
# #                 annotation["abstract"] = content_value
# #                 annotations.append(annotation)

# for entry in Angewandte_feed.entries:
#     print(entry.description)


# annotation["doi"] = entry.link
# annotation["abstract"] = content_value
# for annotation in annotations:
#     print(annotation["abstract"])
# st = annotation["doi"]
# sub = "doi/"
# ind = st.find(sub)
# print(st[ind + 4 :])

# tdm = TDMClient()


# def download_article(doi: str):
#     tdm.download_pdf(doi)


# if __name__ == "__main__":
#     main()

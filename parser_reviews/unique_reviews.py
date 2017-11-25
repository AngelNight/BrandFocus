# import binascii
# import string


# def unique_reviews(reviews):
#     values = set()
#     result = []
#     for d in reviews:
#         if unique_text(d['text'], values):
#             result.append(d)

#     return result


# def unique_text(text, set_text):
#     for t in set_text:
#         if compaire(text, t) > 80:
#             return False

#     set_text.add(text)
#     return True


# def canonize(text):
#         stop_words = (u'это', u'как', u'так',
#                       u'и', u'в', u'над',
#                       u'к', u'до', u'не',
#                       u'на', u'но', u'за',
#                       u'то', u'с', u'ли',
#                       u'а', u'во', u'от',
#                       u'со', u'для', u'о',
#                       u'же', u'ну', u'вы',
#                       u'бы', u'что', u'кто',
#                       u'он', u'она')

#         result = text.lower().split()
#         x = [x.strip(string.punctuation) for x in result]
#         y = [y for y in x if x and (x not in stop_words)]
#         return y
#         # return ([x for x in [y.strip(stop_words) for y in text.lower().split()] if x and (x not in stop_words)])


# def gen_shingle(text):
#     shingleLen = 10 if (len(text) > 10) else len(text) - 1  # длина шингла
#     out = []
#     for i in range(len(text) - (shingleLen - 1)):
#         out.append(binascii.crc32(
#             ' '.join([x for x in text[i:i + shingleLen]]).encode('utf-8')))

#     return out


# def compaire(text_1, text_2):
#     cmp_1 = gen_shingle(canonize(text_1))
#     cmp_2 = gen_shingle(canonize(text_2))

#     # if len(cmp_1) + len(cmp_2) == 0:
#     #     return 0

#     same = 0
#     for i in range(len(cmp_1)):
#         if cmp_1[i] in cmp_2:
#             same = same + 1

#     try:
#         return same * 2 / float(len(cmp_1) + len(cmp_2)) * 100
#     except ZeroDivisionError:
#         return 0

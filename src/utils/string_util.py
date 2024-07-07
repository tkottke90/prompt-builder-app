import urllib.parse

def caseInsensitiveMatch(strA: str, strB: str):
  return strA.lower() == strB.lower()

def urlQueryDecode(search: str):
  return urllib.parse.unquote(search)
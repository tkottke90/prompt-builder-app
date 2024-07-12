import urllib.parse
import hashlib

def caseInsensitiveMatch(strA: str, strB: str):
  return strA.lower() == strB.lower()

def urlQueryDecode(search: str):
  return urllib.parse.unquote(search)

def checksum(input: str) -> str:
  return hashlib.md5(input.encode()).hexdigest()
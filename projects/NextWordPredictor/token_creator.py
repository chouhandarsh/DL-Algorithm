from pathlib import Path
import tokenize
from io import StringIO
input_file = Path("/mnt/d/DL-Algorithm/projects/NextWordPredictor/all_code.txt")
output_file = Path("/mnt/d/DL-Algorithm/projects/NextWordPredictor/tokens.txt")
def tokenize_code(code):
    tokens=[]
    try:
        tokens_stream=tokenize.generate_tokens(
            StringIO(code).readline
        )
        for token in tokens_stream:
            token_type = token.type
            token_string = token.string
            if token_type in(
                
                tokenize.ENCODING,
                tokenize.ENDMARKER
            ):
                print(token)
                continue
            elif token_type==tokenize.COMMENT:
                print(token)
                continue
            elif token_type in (
                tokenize.NEWLINE,
                tokenize.NL
            ):
                tokens.append("<EOL>")
            elif token_type == tokenize.INDENT:
                tokens.append("<INDENT>")
            elif token_type==tokenize.DEDENT:
                tokens.append("<DEDENT>")
            else:
                tokens.append(token_string)
    except(tokenize.TokenError,IndentationError,SyntaxError):
        return []
    return tokens
with open(input_file, "r", encoding="utf-8") as source, \
     open(output_file, "w", encoding="utf-8") as output:

    current_code = []

    for line in source:

        if line.strip() == "<EOS>":

            code = "".join(current_code)

            tokens = tokenize_code(code)

            if tokens:
                output.write(" ".join(tokens))
                output.write(" <EOS>\n")

            current_code = []

        else:
            current_code.append(line)
print("Completed ")
print("Total tokens",len(tokens))
print("Saved to:",output_file)


                
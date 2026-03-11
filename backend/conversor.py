KEYWORDS = {
    'inicio': None,
    'fim': None,
    'se': 'if',
    'senao se': 'elif',
    'senao': 'else',
    'fim se': None,
    'repita': 'for',
    'fim repita': None,
    'enquanto': 'while',
    'fim enquanto': None,
    'mostre': 'print'
}

BOOLEANS = {
    'verdadeiro': 'True',
    'falso': 'False'
}

INDENT_STEP = 4


def toPython(pseudocodigo):
    python_lines = []
    indent_stack = [0]
    linhas = pseudocodigo.split('\n')

    for linha in linhas:
        linha = linha.strip()
        if not linha:
            continue

        tokens = linha.split()
        first_token = tokens[0]

        if first_token in KEYWORDS:
            kw = KEYWORDS[first_token]

            if kw is None:
                if first_token in {'fim se', 'fim repita', 'fim enquanto'}:
                    indent_stack.pop()
                continue

            if kw in {'if', 'elif', 'while'}:
                cond = ' '.join(tokens[1:]) if len(tokens) > 1 else ''
                cond = exprToPython(cond)

                python_lines.append(
                    ' ' * (indent_stack[-1] * INDENT_STEP) + f'{kw} {cond}:'
                )

                if kw in {'if', 'while'}:
                    indent_stack.append(indent_stack[-1] + 1)

                continue

            if kw == 'for':
                expr = ' '.join(tokens[1:]) if len(tokens) > 1 else ''
                expr = exprToPython(expr)

                python_lines.append(
                    ' ' * (indent_stack[-1] * INDENT_STEP) +
                    f'for _ in range({expr}):'
                )

                indent_stack.append(indent_stack[-1] + 1)
                continue

            if kw == 'else':
                python_lines.append(
                    ' ' * (indent_stack[-2] * INDENT_STEP) + 'else:'
                )
                indent_stack[-1] = indent_stack[-2] + 1
                continue

            if kw == 'print':
                conteudo = ' '.join(tokens[1:]) if len(tokens) > 1 else ''
                conteudo = exprToPython(conteudo)

                python_lines.append(
                    ' ' * (indent_stack[-1] * INDENT_STEP) +
                    f'print({conteudo})'
                )

                continue

        if 'vale' in linha:
            var, valor = linha.split('vale', 1)
            var = var.strip()
            valor = exprToPython(valor.strip())

            python_lines.append(
                ' ' * (indent_stack[-1] * INDENT_STEP) +
                f'{var} = {valor}'
            )

            continue

        python_lines.append(
            ' ' * (indent_stack[-1] * INDENT_STEP) +
            exprToPython(linha)
        )

    return '\n'.join(python_lines)

def exprToPython(expr):
    tokens = expr.split()
    result = []

    for t in tokens:
        if t in BOOLEANS:
            result.append(BOOLEANS[t])
        else:
            result.append(t)

    return ' '.join(result)
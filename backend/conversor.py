KEYWORDS = {
    'inicio': None,
    'fim': None,
    'mostre': 'print',
    'se': 'if',
    'senao se': 'elif',
    'senao': 'else',
    'fim se': None,
    'repita': 'for',
    'fim repita': None,
    'enquanto': 'while',
    'fim enquanto': None
}

BOOLEANS = {
    'verdadeiro': 'True',
    'falso': 'False'
}

INDENT_STEP = 2


def getKeyword(tokens):
    if len(tokens) >= 2 and tokens[0] == 'senao' and tokens[1] == 'se':
        return 'senao se', tokens[2:]

    if len(tokens) >= 2 and tokens[0] == 'fim':
        return ' '.join(tokens[:2]), tokens[2:]

    return tokens[0], tokens[1:]


def indentLevels(linhas):
    nivel = 0
    niveis = []

    for linha in linhas:
        tokens = linha.split()
        kw, _ = getKeyword(tokens)

        if kw in {'fim se', 'fim repita', 'fim enquanto', 'fim'}:
            nivel -= 1

        niveis.append(max(nivel, 0))

        if kw in {'se', 'repita', 'enquanto'}:
            nivel += 1

    return niveis


def indentPseudo(pseudocodigo):
    linhas = [l.strip() for l in pseudocodigo.split('\n') if l.strip()]
    niveis = indentLevels(linhas)

    resultado = []

    for linha, nivel in zip(linhas, niveis):
        resultado.append(' ' * (nivel * INDENT_STEP) + linha)

    return '\n'.join(resultado)


def exprToPython(expr):
    tokens = expr.split()
    result = []

    for t in tokens:
        if t in BOOLEANS:
            result.append(BOOLEANS[t])
        else:
            result.append(t)

    return ' '.join(result)


def toPython(pseudocodigo):
    linhas = [l.strip() for l in pseudocodigo.split('\n') if l.strip()]
    niveis = indentLevels(linhas)

    python_lines = []

    for linha, nivel in zip(linhas, niveis):
        tokens = linha.split()
        kw, rest = getKeyword(tokens)

        if kw not in KEYWORDS:
            if 'vale' in linha:
                var, valor = linha.split('vale', 1)
                valor = exprToPython(valor.strip())

                python_lines.append(
                    ' ' * (nivel * INDENT_STEP) +
                    f'{var.strip()} = {valor}'
                )
            continue

        py = KEYWORDS[kw]

        if py is None:
            continue

        if py in {'if', 'elif', 'while'}:
            cond = exprToPython(' '.join(rest))
            python_lines.append(
                ' ' * (nivel * INDENT_STEP) +
                f'{py} {cond}:'
            )

        elif py == 'for':
            expr = exprToPython(' '.join(rest))
            python_lines.append(
                ' ' * (nivel * INDENT_STEP) +
                f'for _ in range({expr}):'
            )

        elif py == 'else':
            python_lines.append(
                ' ' * (nivel * INDENT_STEP) +
                'else:'
            )

        elif py == 'print':
            conteudo = exprToPython(' '.join(rest))
            python_lines.append(
                ' ' * (nivel * INDENT_STEP) +
                f'print({conteudo})'
            )

    return '\n'.join(python_lines)
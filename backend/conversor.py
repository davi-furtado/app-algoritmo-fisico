from re import sub

PSEUDO_INDENT_STEP = 2
PYTHON_INDENT_STEP = 4

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

        if kw in {'inicio', 'se', 'repita', 'enquanto'}:
            nivel += 1

    return niveis


def indentPseudo(pseudocodigo):
    linhas = pseudocodigo.split('\n')
    niveis = indentLevels(linhas)

    resultado = []

    for linha, nivel in zip(linhas, niveis):
        resultado.append(' ' * (nivel * PSEUDO_INDENT_STEP) + linha)

    return '\n'.join(resultado)


def exprToPython(expr):
    expr = sub(r'\bverdadeiro\b', 'True', expr)
    expr = sub(r'\bfalso\b', 'False', expr)
    return expr


def toPython(pseudocodigo):
    linhas = [l.strip() for l in pseudocodigo.split('\n') if l.strip()]
    niveis = [max(n-1, 0) for n in indentLevels(linhas)]

    linhas = linhas[1:-1]
    niveis = niveis[1:-1]

    python_lines = []

    for linha, nivel in zip(linhas, niveis):
        tokens = linha.split()
        kw, rest = getKeyword(tokens)

        indent = ' ' * (nivel * PYTHON_INDENT_STEP)

        if 'vale' in linha:
            var, valor = linha.split('vale', 1)
            python_lines.append(
                f'{indent}{var.strip()} = {exprToPython(valor.strip())}'
            )

        elif kw == 'mostre':
            python_lines.append(
                f'{indent}print({exprToPython(' '.join(rest))})'
            )

        elif kw == 'se':
            python_lines.append(
                f'{indent}if {exprToPython(' '.join(rest))}:'
            )

        elif kw == 'senao se':
            python_lines.append(
                f'{indent}elif {exprToPython(' '.join(rest))}:'
            )

        elif kw == 'senao':
            python_lines.append(f'{indent}else:')

        elif kw == 'enquanto':
            python_lines.append(
                f'{indent}while {exprToPython(' '.join(rest))}:'
            )

        elif kw == 'repita':
            python_lines.append(
                f'{indent}for _ in range({exprToPython(' '.join(rest))}):'
            )

    return '\n'.join(python_lines)
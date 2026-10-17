# DCGames

Catálogo público de jogos e executáveis para o Beako Presence (Linux e Windows).

## Arquitetura
- `scripts/update_catalog.py`: consulta o endpoint de aplicações detectáveis do Discord e normaliza os dados.
- `data/catalog.json`: catálogo publicado para os clientes.
- `data/confirmed.json`: executáveis verificados manualmente; não são substituídos pela atualização automática.
- GitHub Actions executa o coletor diariamente e permite execução manual.

## URLs para os aplicativos
- Catálogo: https://raw.githubusercontent.com/Niltonjuniornzx/dcgames/main/data/catalog.json
- Confirmados: https://raw.githubusercontent.com/Niltonjuniornzx/dcgames/main/data/confirmed.json

O cliente deve fazer cache local, usar o último catálogo válido em caso de erro e nunca considerar `detected` equivalente a `confirmed`.

## Atualização local
```bash
python3 scripts/update_catalog.py
```

Requer Python 3.9+ e conexão com a internet. O endpoint do Discord não é uma API pública estável: ele pode mudar ou bloquear consultas. Nesse caso, o script encerra com erro e **preserva o último catálogo válido**.

## Formato
`catalog.json` contém `schema_version`, `generated_at`, `source`, `count` e `games`. Cada jogo contém `id`, `name` e `executables`, com entradas `name`, `os` e `source`. Os dados em `confirmed.json` são mantidos separadamente.

O DCGames é um projeto independente e não é afiliado ao Discord.

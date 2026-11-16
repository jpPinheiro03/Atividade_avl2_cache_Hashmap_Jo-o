# Cache de Conteúdo com HashMap — Spring Boot

Atividade AVL2 — API que serve conteúdos (artigos) usando um **cache próprio
construído com `ConcurrentHashMap`**, sem `@Cacheable`, Caffeine ou Redis.

## Como rodar

Requisitos: JDK 21+ e Maven.

```bash
mvn spring-boot:run
```

A API sobe em `http://localhost:8080` com banco H2 em memória.
Console H2 (opcional): http://localhost:8080/h2-console

## Configuração (`src/main/resources/application.properties`)

```properties
app.cache.max-itens=5        # limite de itens no cache (LRU ao encher)
app.cache.ttl-segundos=60    # tempo de vida de cada entrada
app.fonte.atraso-ms=2000     # atraso artificial da "fonte lenta" (banco simulado)
```

## Como o cache funciona

- `ConteudoCache` (`@Component`) guarda `Map<Long, EntradaCache>` em um
  `ConcurrentHashMap`. Cada `EntradaCache` tem o conteúdo, o instante em que
  foi armazenado (`armazenadoEm`) e o último acesso (`ultimoAcesso`).
- **HIT**: entrada existe e não expirou → retorna na hora, atualiza
  `ultimoAcesso` e incrementa `hits`.
- **MISS**: entrada não existe ou expirou (TTL) → chama a fonte
  (`repository.findById` com `Thread.sleep(2000)`), armazena no cache e
  incrementa `misses`.
- **LRU**: ao inserir com o cache cheio, remove a entrada com o
  `ultimoAcesso` mais antigo e incrementa `evictions`.
- **Invalidação**: `PUT` e `DELETE` chamam `cache.remover(id)`.
- **Estatísticas**: contadores `AtomicLong` (hits, misses, evictions) +
  tamanho atual, limite e hit ratio.
- Cada busca gera log SLF4J: `Cache HIT|MISS - id=X - Y ms`.

## Endpoints

| Método | Rota                  | Comportamento                              |
|--------|-----------------------|--------------------------------------------|
| GET    | /conteudos/{id}       | Cache HIT/MISS, header `X-Cache`           |
| POST   | /conteudos            | Cadastra conteúdo                          |
| PUT    | /conteudos/{id}       | Atualiza e invalida o cache                |
| DELETE | /conteudos/{id}       | Exclui e invalida o cache                  |
| GET    | /cache/estatisticas   | Tamanho, limite, hits, misses, evictions, hit ratio |
| DELETE | /cache                | Limpa todo o cache                         |

Exemplo:

```bash
curl -X POST localhost:8080/conteudos -H "Content-Type: application/json" \
  -d '{"titulo":"Artigo 1","corpo":"Corpo","autor":"Autor"}'

curl -i localhost:8080/conteudos/1   # 1ª vez: X-Cache: MISS (~2s)
curl -i localhost:8080/conteudos/1   # 2ª vez: X-Cache: HIT  (~ms)

curl localhost:8080/cache/estatisticas
```

## Estrutura

```
src/main/java/school/sptech/
├── CacheMapApplication.java
├── entity/Conteudo.java
├── repository/ConteudoRepository.java
├── cache/ConteudoCache.java        # cache próprio (ConcurrentHashMap + LRU + TTL)
├── service/ConteudoService.java    # usa o cache e o repositório, atraso artificial
├── controller/ConteudoController.java
├── controller/CacheController.java
├── dto/ConteudoRequest.java, ConteudoResponse.java
└── mapper/ConteudoMapper.java
```

## Demonstração (resultados reais)

- `GET /conteudos/1` → `X-Cache: MISS`, ~2,02 s; repetição → `X-Cache: HIT`, ~0,007 s
- Com limite 5, o 6º item provocou `evictions=1` (remoção LRU)
- Após ~62 s (TTL=60), `GET /conteudos/3` voltou a ser `MISS`
- `PUT /conteudos/3` invalidou a entrada → próxima busca foi `MISS`
- `DELETE /conteudos/2` → 204; busca seguinte → 404
- Estatísticas finais: `{"tamanho":4,"limite":5,"hits":13,"misses":12,"evictions":1,"hitRatio":0.52}`

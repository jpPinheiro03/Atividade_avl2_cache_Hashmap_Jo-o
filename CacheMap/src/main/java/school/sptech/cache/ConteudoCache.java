package school.sptech.cache;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import java.time.Duration;
import java.time.Instant;
import java.util.Comparator;
import java.util.Map;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;
import java.util.function.Supplier;

@Component
public class ConteudoCache {

    private static final Logger log = LoggerFactory.getLogger(ConteudoCache.class);

    private final Map<Long, EntradaCache> cache = new ConcurrentHashMap<>();
    private final int maxItens;
    private final Duration ttl;

    private final AtomicLong hits = new AtomicLong();
    private final AtomicLong misses = new AtomicLong();
    private final AtomicLong evictions = new AtomicLong();

    public ConteudoCache(
            @Value("${app.cache.max-itens:5}") int maxItens,
            @Value("${app.cache.ttl-segundos:60}") long ttlSegundos) {
        this.maxItens = maxItens;
        this.ttl = Duration.ofSeconds(ttlSegundos);
    }

    public record Resultado<T>(T valor, boolean hit) {
    }

    public record Estatisticas(long tamanho, int limite, long hits, long misses,
                               long evictions, double hitRatio) {
    }

    /**
     * Busca o conteudo no cache; em caso de miss ou expiracao, chama a fonte
     * (lenta), armazena o resultado e devolve o conteudo com a flag de hit.
     */
    public Resultado<school.sptech.entity.Conteudo> obter(Long id,
            Supplier<school.sptech.entity.Conteudo> fonte) {
        long inicio = System.nanoTime();

        EntradaCache entrada = cache.get(id);
        if (entrada != null && !expirado(entrada)) {
            entrada.registrarAcesso();
            hits.incrementAndGet();
            long ms = elapsedMs(inicio);
            log.info("Cache HIT  - id={} - {} ms", id, ms);
            return new Resultado<>(entrada.conteudo, true);
        }

        if (entrada != null) {
            cache.remove(id, entrada);
        }
        misses.incrementAndGet();

        school.sptech.entity.Conteudo conteudo = fonte.get();
        if (conteudo != null) {
            armazenar(id, conteudo);
        }

        long ms = elapsedMs(inicio);
        log.info("Cache MISS - id={} - {} ms", id, ms);
        return new Resultado<>(conteudo, false);
    }

    public void armazenar(Long id, school.sptech.entity.Conteudo conteudo) {
        if (cache.containsKey(id)) {
            return;
        }
        if (cache.size() >= maxItens) {
            removerExpirados();
            if (cache.size() >= maxItens) {
                evictarLru();
            }
        }
        cache.put(id, new EntradaCache(conteudo));
    }

    public void remover(Long id) {
        cache.remove(id);
    }

    public void limpar() {
        cache.clear();
    }

    public Estatisticas estatisticas() {
        long h = hits.get();
        long m = misses.get();
        long total = h + m;
        double ratio = total == 0 ? 0.0 : (double) h / total;
        return new Estatisticas(cache.size(), maxItens, h, m, evictions.get(), ratio);
    }

    private boolean expirado(EntradaCache entrada) {
        return Duration.between(entrada.armazenadoEm, Instant.now()).compareTo(ttl) > 0;
    }

    private void removerExpirados() {
        cache.values().removeIf(this::expirado);
    }

    private void evictarLru() {
        cache.entrySet().stream()
                .min(Comparator.comparing(e -> e.getValue().ultimoAcesso.get()))
                .ifPresent(e -> {
                    cache.remove(e.getKey(), e.getValue());
                    evictions.incrementAndGet();
                    log.info("Cache EVICT - id={} (LRU, cache cheio)", e.getKey());
                });
    }

    private long elapsedMs(long inicioNanos) {
        return (System.nanoTime() - inicioNanos) / 1_000_000;
    }

    private static class EntradaCache {
        private final school.sptech.entity.Conteudo conteudo;
        private final Instant armazenadoEm = Instant.now();
        private final AtomicLong ultimoAcesso = new AtomicLong(System.nanoTime());

        EntradaCache(school.sptech.entity.Conteudo conteudo) {
            this.conteudo = conteudo;
        }

        void registrarAcesso() {
            ultimoAcesso.set(System.nanoTime());
        }
    }
}

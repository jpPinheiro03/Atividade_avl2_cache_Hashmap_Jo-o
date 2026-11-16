package school.sptech.service;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;
import school.sptech.cache.ConteudoCache;
import school.sptech.dto.ConteudoRequest;
import school.sptech.entity.Conteudo;
import school.sptech.mapper.ConteudoMapper;
import school.sptech.repository.ConteudoRepository;

@Service
public class ConteudoService {

    private final ConteudoRepository repository;
    private final ConteudoCache cache;
    private final ConteudoMapper mapper;
    private final long atrasoFonteMs;

    public ConteudoService(ConteudoRepository repository,
                           ConteudoCache cache,
                           ConteudoMapper mapper,
                           @Value("${app.fonte.atraso-ms:2000}") long atrasoFonteMs) {
        this.repository = repository;
        this.cache = cache;
        this.mapper = mapper;
        this.atrasoFonteMs = atrasoFonteMs;
    }

    public ConteudoCache.Resultado<Conteudo> buscarPorId(Long id) {
        return cache.obter(id, () -> buscarNaFonte(id));
    }

    private Conteudo buscarNaFonte(Long id) {
        try {
            Thread.sleep(atrasoFonteMs);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        return repository.findById(id).orElse(null);
    }

    public Conteudo criar(ConteudoRequest request) {
        return repository.save(mapper.toEntity(request));
    }

    public Conteudo atualizar(Long id, ConteudoRequest request) {
        Conteudo conteudo = repository.findById(id)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND));
        conteudo.setTitulo(request.titulo());
        conteudo.setCorpo(request.corpo());
        conteudo.setAutor(request.autor());
        Conteudo salvo = repository.save(conteudo);
        cache.remover(id);
        return salvo;
    }

    public void excluir(Long id) {
        if (!repository.existsById(id)) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND);
        }
        repository.deleteById(id);
        cache.remover(id);
    }

    public ConteudoCache.Estatisticas estatisticas() {
        return cache.estatisticas();
    }

    public void limparCache() {
        cache.limpar();
    }
}
